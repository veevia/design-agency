/**
 * templates/Root.tsx — the composition registry.
 * Copy into your project's src/Root.tsx and adjust ids/sizes/durations.
 *
 * Duration, fps, and dimensions are declared HERE, never inside the component.
 * Two variants shown: a static composition and a data-driven one (calculateMetadata).
 */
import { Composition, CalculateMetadataFunction } from "remotion";
import { Scene } from "./Scene";
// import { CaptionedScene } from "./CaptionedScene";

// --- Variant A: static composition ---------------------------------------
export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MyScene"
        component={Scene}
        durationInFrames={120}   // 4s @ 30fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{ title: "Hello World" }}
      />

      {/* --- Variant B: data-driven duration/size via calculateMetadata ---
      <Composition
        id="DataDriven"
        component={Scene}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{ videoId: "abc123", title: "" }}
        calculateMetadata={calculateMetadata}
      />
      */}
    </>
  );
};

// Example calculateMetadata: fetch data, then size the video to it.
// eslint-disable-next-line @typescript-eslint/no-unused-vars
const calculateMetadata: CalculateMetadataFunction<{
  videoId: string;
  title: string;
}> = async ({ props, abortSignal }) => {
  const data = await fetch(`https://api.example.com/video/${props.videoId}`, {
    signal: abortSignal,
  }).then((res) => res.json());

  return {
    durationInFrames: Math.ceil(data.duration * 30),
    props: { ...props, title: data.title },
    width: 1920,
    height: 1080,
  };
};
