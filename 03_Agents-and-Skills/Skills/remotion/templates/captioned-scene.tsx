/**
 * templates/captioned-scene.tsx — a scene that renders synced captions (demo-master CC parity).
 * Minimal bottom-center caption bar driven by a Caption[] (no audio needed) — the direct
 * graduation of demo-master's CC bar. For TikTok-style pages + word highlighting, use
 * @remotion/captions' createTikTokStyleCaptions() instead (see references/captions.md).
 *
 * A Caption is { text, startMs, endMs, timestampMs, confidence } from @remotion/captions.
 */
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import type { Caption } from "@remotion/captions";

// Convert demo-master beats (one line per beat, click-advanced) into TIMED captions.
// Default read-time per beat: max(2s, words * 0.35s). Lay them back-to-back.
export function captionsFromBeats(lines: string[]): Caption[] {
  let cursorMs = 0;
  return lines.map((text) => {
    const words = text.trim().split(/\s+/).length;
    const durMs = Math.max(2000, words * 350);
    const cap: Caption = {
      text,
      startMs: cursorMs,
      endMs: cursorMs + durMs,
      timestampMs: null,
      confidence: null,
    };
    cursorMs += durMs;
    return cap;
  });
}

export const CaptionedScene: React.FC<{ captions: Caption[] }> = ({ captions }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const nowMs = (frame / fps) * 1000;

  const active = captions.find((c) => c.startMs <= nowMs && c.endMs > nowMs);

  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center" }}>
      {active ? (
        <div
          style={{
            marginBottom: 80,
            maxWidth: "80%",
            textAlign: "center",
            fontSize: 44,
            fontWeight: 600,
            color: "white",
            background: "rgba(0,0,0,0.55)",
            padding: "12px 28px",
            borderRadius: 12,
            whiteSpace: "pre-wrap",
          }}
        >
          {active.text}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
