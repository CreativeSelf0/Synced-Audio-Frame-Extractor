import argparse
import os

import numpy as np
from moviepy.audio.AudioClip import AudioArrayClip
from moviepy.editor import ImageSequenceClip
from tqdm import tqdm

from extract_synced_frames import get_audio_visual_frames


def group_by_seconds(frames, audio_frames, fps, sr, seconds=1):
    grouped_frames = []
    grouped_audio = []
    num_frames = fps * seconds
    # RGB to BGR conversion as ImageSequenceClip expects BGR
    frames = [frame[:, :, ::-1] for frame in frames]
    for i in tqdm(
        range(0, len(frames), num_frames), desc="Grouping video / audio frames"
    ):
        end_idx = min(i + num_frames, len(frames))
        grouped_frames.append(frames[i:end_idx])
        start_sample = i * sr // fps
        end_sample = start_sample + sr * seconds
        # Concatenate audio for these frames
        concatenated_audio = np.concatenate(audio_frames[i:end_idx])
        grouped_audio.append(concatenated_audio[: end_sample - start_sample])

    return grouped_frames, grouped_audio


def reconstruct_videos(output_path, grouped_frames, grouped_audio, sr, fps):
    for idx, (frames, audio) in tqdm(
        enumerate(zip(grouped_frames, grouped_audio)),
        desc="Reconstructing videos",
        total=len(grouped_frames),
    ):
        clip = ImageSequenceClip(frames, fps=fps)
        audio_clip = AudioArrayClip(audio, fps=sr)
        video = clip.set_audio(audio_clip)
        video.write_videofile(
            os.path.join(output_path, f"sample_{idx: 05d}.mp4"),
            fps=fps,
            logger=None,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--video_path", type=str, required=True, help="Path to video"
    )
    args = parser.parse_args()

    frames, fps, audio_frames, sr = get_audio_visual_frames(args.video_path)
    grouped_frames, grouped_audio = group_by_seconds(
        frames, audio_frames, fps, sr, seconds=3
    )

    os.makedirs("sample_videos", exist_ok=True)
    reconstruct_videos("sample_videos", grouped_frames, grouped_audio, sr, fps)
