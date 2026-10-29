#!/usr/bin/env node
/**
 * sync-figma-icons.mjs
 * --------------------
 * Pull SVG icons from Figma and drop them into a local folder.
 *
 *   node scripts/sync-figma-icons.mjs           # uses ./figma-icons.json
 *   node scripts/sync-figma-icons.mjs custom.json
 *
 * Requires:
 *   FIGMA_TOKEN   personal access token with file_read scope
 *                 (set in .env.local — gitignored — or your shell)
 *
 * Manifest schema (figma-icons.json):
 *   {
 *     "outDir": "public/icons",
 *     "defaultFileKey": "REPLACE_WITH_FIGMA_FILE_KEY",
 *     "icons": [
 *       { "name": "example-icon", "nodeId": "1:2" },
 *       { "name": "other-icon",   "nodeId": "3:4", "fileKey": "OTHER_FILE_KEY" }
 *     ]
 *   }
 *
 * Each entry produces `<outDir>/<name>.svg`. Existing files are overwritten.
 * Per-icon `fileKey` overrides the default. Re-run after editing the manifest
 * or when icons change in Figma — this is the single source of truth.
 */

import { mkdir, readFile, writeFile, access } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const projectRoot = resolve(__dirname, '..');

// ---- 1. Load env (.env.local) -------------------------------------------------
async function loadDotEnvLocal() {
  const envPath = join(projectRoot, '.env.local');
  try {
    await access(envPath);
  } catch {
    return;
  }
  const text = await readFile(envPath, 'utf8');
  for (const line of text.split('\n')) {
    const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*?)\s*$/);
    if (!m) continue;
    const [, key, raw] = m;
    if (process.env[key]) continue; // shell wins
    process.env[key] = raw.replace(/^['"]|['"]$/g, '');
  }
}

// ---- 2. Load manifest ---------------------------------------------------------
async function loadManifest(path) {
  const text = await readFile(path, 'utf8');
  const json = JSON.parse(text);
  if (!Array.isArray(json.icons) || json.icons.length === 0) {
    throw new Error(`Manifest ${path} has no icons[]`);
  }
  return json;
}

// ---- 3. Figma API helpers -----------------------------------------------------
const FIGMA = 'https://api.figma.com/v1';

async function figmaGet(url, token) {
  const res = await fetch(url, { headers: { 'X-Figma-Token': token } });
  if (!res.ok) {
    const body = await res.text().catch(() => '');
    throw new Error(`Figma ${res.status} ${res.statusText} on ${url}\n${body}`);
  }
  return res.json();
}

async function fetchImageUrls(fileKey, nodeIds, token) {
  // Figma node IDs in API calls accept either "12:345" or "12-345" — normalise.
  const ids = nodeIds.map((n) => n.replace(/-/g, ':')).join(',');
  const url = `${FIGMA}/images/${fileKey}?ids=${encodeURIComponent(ids)}&format=svg`;
  const data = await figmaGet(url, token);
  if (data.err) throw new Error(`Figma image API error for ${fileKey}: ${data.err}`);
  return data.images || {};
}

async function downloadSvg(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Download failed: ${res.status} ${res.statusText} ${url}`);
  return res.text();
}

// ---- 4. Main ------------------------------------------------------------------
async function main() {
  await loadDotEnvLocal();

  const token = process.env.FIGMA_TOKEN || process.env.FIGMA_PERSONAL_ACCESS_TOKEN;
  if (!token) {
    console.error('✗ FIGMA_TOKEN is not set.');
    console.error('  Add to .env.local:  FIGMA_TOKEN=figd_…');
    console.error('  Or export in shell: export FIGMA_TOKEN=figd_…');
    process.exit(1);
  }

  const manifestArg = process.argv[2] || 'figma-icons.json';
  const manifestPath = resolve(projectRoot, manifestArg);
  const manifest = await loadManifest(manifestPath);

  const outDir = resolve(projectRoot, manifest.outDir || 'public/icons');
  await mkdir(outDir, { recursive: true });

  // Group icons by fileKey to minimise API round-trips
  const byFile = new Map();
  for (const icon of manifest.icons) {
    const fileKey = icon.fileKey || manifest.defaultFileKey;
    if (!fileKey) {
      console.error(`✗ icon "${icon.name}" has no fileKey and no defaultFileKey`);
      process.exit(1);
    }
    if (!byFile.has(fileKey)) byFile.set(fileKey, []);
    byFile.get(fileKey).push(icon);
  }

  console.log(`→ Syncing ${manifest.icons.length} icons → ${outDir}`);
  let ok = 0;
  let fail = 0;

  for (const [fileKey, icons] of byFile) {
    console.log(`  Figma file ${fileKey}  (${icons.length} icons)`);
    const urls = await fetchImageUrls(fileKey, icons.map((i) => i.nodeId), token);

    await Promise.all(
      icons.map(async (icon) => {
        const normalised = icon.nodeId.replace(/-/g, ':');
        const url = urls[normalised];
        if (!url) {
          console.warn(`    ✗ ${icon.name}  (node ${icon.nodeId}: no URL returned)`);
          fail++;
          return;
        }
        try {
          const svg = await downloadSvg(url);
          const target = join(outDir, `${icon.name}.svg`);
          await writeFile(target, svg, 'utf8');
          console.log(`    ✓ ${icon.name}.svg`);
          ok++;
        } catch (err) {
          console.warn(`    ✗ ${icon.name}: ${err.message}`);
          fail++;
        }
      }),
    );
  }

  console.log(`\nDone. ${ok} written, ${fail} failed.`);
  process.exit(fail > 0 ? 1 : 0);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
