# Whiteboard storyboard — image-gen prompt template

Fill the slots in `<…>`, then paste the result into an image-generation tool. Target aspect ratio **3:2** (1536×1024 or 1920×1280).

---

A hand-drawn whiteboard storyboard, slightly wobbly ink lines, off-white paper background (#FAF7F2), in a casual handwritten style like Bradley Hand. Five panels separated by dashed black lines, arranged in two rows: top row of three equal-width panels, bottom row of two panels with the left one about 55% width.

**Title bar across the top in large bold hand-printed black caps:**
"<TITLE — ≤9 WORDS, ALL CAPS>"
"<SUBTITLE — definitions or one-line setup>"

**Panel 1 (top-left, label "(1) BEFORE (<MINUTES> min)"):**
A stick figure named <CHARACTER NAME> labeled "<CHARACTER ROLE>" at a desk with a laptop, frowning, with a thought bubble that reads "<PAIN QUESTION IN ONE LINE>". Around the desk, draw <N> small browser-window icons labeled <SYSTEM 1>, <SYSTEM 2>, <SYSTEM 3>, <SYSTEM 4>. Below: a red clock icon with "<MINUTES> MIN" and a small frowning face.

**Panel 2 (top-middle, label "(2) <CENTRAL CONCEPT NAME>"):**
<DRAW THE CENTRAL DIAGRAM — flywheel / agent / pipeline / model. Be specific about node names, arrows, and any centre element. Example: "A circular flywheel with 6 arrows pointing clockwise between 6 boxes labelled S1 INTAKE, S2 ASSESS, S3 MATCH, S4 SCHEDULE, S5 FIX, S6 LEARN, with S3 MATCH outlined in amber. In the centre, a small service vehicle with a wrench on its side.">

**Panel 3 (top-right, label "(3) WORKED EXAMPLE (with receipts)"):**
<A CONCRETE EXAMPLE WITH NAMED ENTITIES — table, list, or trace. Example: "A hand-drawn table with header row '<COL1> | <COL2> | <COL3>' and three rows showing concrete values, with green checkmarks, red Xs, and yellow REVIEW labels in cells."> Caption below in italic: "every cell → <PROOF FORMAT>"

**Panel 4 (bottom-left, ~55% width, label "(4) <SECRET SAUCE NAME> (the secret sauce)"):**
A node-and-edge graph in blue ink. Central node labelled "<CENTRAL ENTITY>". Around it, ~8 satellite nodes labelled "<TYPE>: <NAME>" (e.g., "CUSTOMER: C-1042", "LOCATION: L-2207", "ASSET: Unit U-200", "CONTRACT: SC-88"). Edges labelled with relation verbs ("located_at", "installed_at", "covered_by", "serviced_by"). Caption below in italic blue: "One model. <ONE-SENTENCE EXPLANATION OF THE GRAPH>."

**Panel 5 (bottom-right, ~45% width, label "(5) IMPACT + VALUE"):**
On the left, a red-bordered box that reads "<TRIGGERING EVENT — one line>". An arrow labelled "look up <STRUCTURE>" pointing right to four stacked red-bordered boxes, each containing one impact bullet: "<BULLET 1>", "<BULLET 2>", "<BULLET 3>", "<BULLET 4>". Below, a green-bordered box that reads "<BEFORE> → <AFTER>, WITH <PROOF> AND <NEW CAPABILITY>". Bottom-right corner: the same stick figure from Panel 1, this time smiling and giving a thumbs-up, labelled "<CHARACTER NAME>" in green.

**Style enforcement:**
- All text hand-printed, varying line weight, slight wobble.
- Use only these colours: black ink for outlines and titles, blue for Panel 4 graph, green for the positive metric and the closing character, red for the triggering event and impact bullets, amber/yellow for any "REVIEW" warning state.
- No photorealism, no glossy gradients, no UI mockups. Pure whiteboard sketch.
- Dashed lines between panels and one solid horizontal line between the top and bottom rows.

---

## Mode B usage notes

- Chat-based image tools: paste verbatim; specify "3:2 aspect ratio" if asked.
- Other image tools: paste verbatim; pick a 3:2 or 16:9 canvas and accept the crop.
- Tools with style presets: paste verbatim; choose an "infographic / illustration" preset.
- For corrections, regenerate one panel at a time by re-prompting only that section with the same opening "hand-drawn whiteboard..." stanza.
