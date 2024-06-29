# Image Sequence to Video Converter

This script converts a sequence of images into an MP4 video file using user-defined settings for frame delay, hold durations for the first and last frames, and video quality.

## Installation Guide

### Step 1: Install Python Packages

Open your terminal or command prompt and run the following command to install the required Python packages:

```bash
pip install opencv-python Pillow
```

### Step 2: Download the script
download the `make_frame_animation.py` to a directory of your choosings.

### Step 2.1: Download and Setup FFmpeg
1. Go to [FFmpeg official downloads](https://ffmpeg.org/download.html).
2. Under "Get packages & executable files", download the zip file for your operating system.
3. Extract the contents of the downloaded zip/7z file.
4. Inside the extracted folder, navigate to the bin folder.
5. Locate the `ffmpeg.exe` file and move it to the same directory as the script.

### Step 3: Run the Script
open your terminal inside the directory you download the files to/moved them to.

now run the following command to start the script:
```bash
python make_frame_animation.py
```

----------

## How the Script Works

### Collect Images
The script looks for all image files (PNG, JPG, JPEG) in the directory where it is located.
Ensure that the images are named in a way that reflects their order, as they will be sorted alphabetically.

### User Input
- Frame Delay: Enter the delay between frames in milliseconds. This value controls the speed of the animation.
- Hold Frames: You can choose to hold the first and last frames for a longer duration. If you select this option, you will be prompted to enter the durations (in milliseconds) for holding the first and last frames.
- Quality Option: You will be prompted to select the quality of the output video. The options are:
  - low (1000k)
  - medium (2000k)
  - high (3000k)
  - very_high (4000k)
  - ultra_high (5000k)
>If no valid quality option is selected, the default quality (low) will be used.

### Video Creation
The script uses OpenCV to read the images and convert them into frames.
FFmpeg is then used to encode these frames into an MP4 video file with the specified quality.

### Output
The output video file is saved in the same directory with a name based on the first image’s name, appended with _output.

### Things to Keep in Mind
- Image Order: Ensure your images are named sequentially or in an order that will be correctly sorted alphabetically.
- FFmpeg Setup: Make sure ffmpeg.exe is in the same directory as your script.
- Frame Delay: A lower delay results in faster animation and vice versa.
- Quality Settings: Higher quality settings result in larger file sizes. (low is mostly enough for image squenz animations)
- Directory: The script processes images and saves the video in the directory where it is located.
- Image size: The script is made to process images for a sequnce, please do not add imgs to it that differe in size,
  the script will try to resize images that don't match the size of the first image, but it might cause errors or problems.


# Info

This project needs `ffmpeg.exe` for creating videos from frame sequences using a Python script. FFmpeg is licensed under the LGPL/GPL. 

The `ffmpeg.exe` binary was obtained from [FFmpeg official downloads](https://ffmpeg.org/download.html).

For more details on FFmpeg's license, please refer to the [LICENSE-FFmpeg](LICENSE-FFmpeg) file or visit the [FFmpeg legal page](https://ffmpeg.org/legal.html).

You can download the source code for FFmpeg from their [official source](https://ffmpeg.org/download.html).

This script was made with the Help of AI.
