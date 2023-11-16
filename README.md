# Synced Audio Frame Extractor
![image](./assets/synced.png)
![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)

Welcome to Synced Audio Frame Extractor, a tool designed to generate synchronized audio frames from video files. This tool is perfect for professionals and hobbyists who need precise audio and frame synchronization for their video editing and analysis projects.

## Features

- **Frame-Audio Synchronization:** Extract frames from videos with perfect sync to the audio.
- **Optional Testing Mode:** Preview your synchronized frames before final extraction.

## Getting Started

Follow these simple steps to start using Synced Audio Frame Extractor:

### Prerequisites

Ensure you have Python installed on your system. If not, download and install it from [Python's official website](https://www.python.org/downloads/).

### Installation

1. **Clone the Repository**  
   Clone this repository to your local machine to get started.

   ```bash
   git clone https://github.com/your-repository/synced-audio-frame-extractor.git
   cd synced-audio-frame-extractor
   ```

2. **Install Dependencies**  
   Run the following command to install the required libraries.
    ```bash
   conda create -n synced-audio-frame-extractor python=3.8
   ```

   ```bash
   conda activate synced-audio-frame-extractor
   ```

   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. **Extract Synced Frames**  
   Use this command to extract frames synchronized with the audio from your video file.

   ```bash
   python extract_synced_frames.py --video_path <path to your video file>
   ```

2. **Optional Testing**  
   Preview group of concatenated seconds of frames with their audios reconstructed.

   ```bash
   python group_video.py --video_path <path to your video file>
   ```

## Contributing

Contributions to improve Synced Audio Frame Extractor are welcome. 

## To Do:

- **Efficiency**: Improve the efficiency of the code to reduce the time taken for extraction.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.