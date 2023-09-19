import argparse
import math
import os

import cv2
import numpy as np
import soundfile as sf
from moviepy.editor import VideoFileClip
from tqdm import tqdm


def extract_audio(video_path: str):
    """Extract audio from video.

    Args:
        video_path (str): path to video

    Returns:
        y: audio samples
        sr: sample rate
    """
    # Load the video using moviepy
    clip = VideoFileClip(video_path)
    # Save the audio segment to a temporary audio file
    output_path = "temp_audio.wav"
    clip.audio.write_audiofile(
        output_path, codec="pcm_s16le", logger=None
    )  # Save as WAV with pcm_s16le codec for lossless extraction

    # Now, you can load the audio samples using librosa
    y, sr = sf.read(output_path)

    # Remove the temporary file
    os.remove(output_path)

    return y, sr


def get_audio_visual_frames(video_path: str, output_path: str = "data"):
    """Extract audio frames from video.

    Args:
        video_path (str): path to video
        output_path (str): path to save audio frames
    """
    # Load video and get its frames per second (FPS)
    cap = cv2.VideoCapture(video_path)
    # Load audio and get its sample rate
    y, sr = extract_audio(video_path)
    # Calculate cumulative samples for each frame
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # Round up the number of frames to the nearest second
    fps = int(math.ceil(cap.get(cv2.CAP_PROP_FPS)))
    cumulative_samples = np.round(
        np.linspace(0, len(y), total_frames + 1)
    ).astype(int)

    # Extract audio samples corresponding to each frame
    frames = []
    audio_frames = []
    for i in tqdm(range(total_frames), desc="Extracting video / audio frames"):
        ret, frame = cap.read()
        if not ret:
            break
        start_sample = cumulative_samples[i]
        end_sample = cumulative_samples[i + 1]
        audio_frame = y[start_sample:end_sample]

        frames.append(frame)
        audio_frames.append(audio_frame)

    cap.release()

    os.makedirs(output_path, exist_ok=True)
    os.makedirs(os.path.join(output_path, "audio"), exist_ok=True)
    os.makedirs(os.path.join(output_path, "frames"), exist_ok=True)

    for index, (audio_frame, frame) in enumerate(
        tqdm(
            zip(audio_frames, frames), desc="Saving frames", total=len(frames)
        )
    ):
        cv2.imwrite(
            os.path.join(output_path, f"frames/frame_{index:05d}.jpg"), frame
        )
        # Save audio frames as WAV files
        sf.write(
            os.path.join(output_path, f"audio/frame_{index:05d}.wav"),
            audio_frame,
            sr,
        )

    assert len(frames) == len(audio_frames)
    return frames, fps, audio_frames, sr


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_path", type=str, required=True)
    parser.add_argument("--output_path", type=str, default="data")
    args = parser.parse_args()

    get_audio_visual_frames(args.video_path, args.output_path)
