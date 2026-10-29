/**
 * templates/Scene.tsx — a content-driven scene (the canonical interpolate patterns).
 * Copy into src/Scene.tsx and replace the body with your beat's visual.
 *
 * THE RULE: every animated value comes from interpolate(frame, ...).
 * NEVER use CSS transition / @keyframes / animation, or Tailwind animate-* — they don't render.
 */
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, Easing } from "remotion";

export const Scene: React.FC<{ title?: string }> = ({ title = "Hello World" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Fade + rise in over the first 0.7s, clamped so it holds after.
  const opacity = interpolate(frame, [0, 0.7 * fps], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  const translateY = interpolate(frame, [0, 0.7 * fps], [24, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  // Example content-driven number count-up (demo-master "a number counts" → interpolate).
  const count = Math.round(
    interpolate(frame, [0.3 * fps, 1.6 * fps], [0, 1287], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }),
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0b1220",
        color: "white",
        justifyContent: "center",
        alignItems: "center",
        fontFamily: "Inter, system-ui, sans-serif",
        // Individual transform props (NOT a composed transform string) → editable in Studio.
        opacity,
        translate: `0px ${translateY}px`,
      }}
    >
      <div style={{ fontSize: 96, fontWeight: 700 }}>{title}</div>
      <div style={{ fontSize: 140, fontWeight: 800, marginTop: 16 }}>
        {count.toLocaleString()}
      </div>
    </AbsoluteFill>
  );
};
