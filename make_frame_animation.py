import cv2
import os
import subprocess
from PIL import Image
import re

def natural_sort_key(s):
    """
    Split the string `s` into list of strings and integers, and return it as a tuple.
    This allows for natural sorting (i.e., "image2" before "image10").
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def images_to_video(delay_ms, hold_first, hold_last, hold_first_ms, hold_last_ms, quality_option, custom_bitrate=None, sort_by='name'):
    # Get the current folder path
    folder_path = os.path.dirname(os.path.abspath(__file__))

    # Get list of all files in the folder
    files = [f for f in os.listdir(folder_path) if f.endswith(('png', 'jpg', 'jpeg'))]

    if sort_by == 'date':
        files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))
    else:
        # Use the custom natural_sort_key for natural sorting
        files = sorted(files, key=natural_sort_key)

    if not files:
        print("No images found in the folder.")
        return

    # Read the first image to get the dimensions and the base name
    first_image_name = files[0]
    first_image_path = os.path.join(folder_path, first_image_name)
    first_image = Image.open(first_image_path)
    width, height = first_image.size

    # Base name for the output video
    base_name = os.path.splitext(first_image_name)[0] + "_output"

    # Find a unique file name
    extension = 'mp4'
    output_file = os.path.join(folder_path, f"{base_name}_0.{extension}")
    i = 0
    while os.path.exists(output_file):
        i += 1
        output_file = os.path.join(folder_path, f"{base_name}_{i}.{extension}")

    # Create a list to hold the frames
    frames = []

    # Calculate the number of frames to hold the first and last images
    hold_first_frames = int(hold_first_ms / delay_ms) if hold_first else 0
    hold_last_frames = int(hold_last_ms / delay_ms) if hold_last else 0

    # Append the first frame multiple times if needed
    first_frame = cv2.imread(first_image_path)
    first_frame = cv2.resize(first_frame, (width, height))  # Rescale to match the size of the first image
    for _ in range(hold_first_frames):
        frames.append(first_frame)

    # Append the main frames
    for file in files:
        img_path = os.path.join(folder_path, file)
        img = cv2.imread(img_path)
        img = cv2.resize(img, (width, height))  # Rescale to match the size of the first image
        frames.append(img)

    # Append the last frame multiple times if needed
    last_image_path = os.path.join(folder_path, files[-1])
    last_frame = cv2.imread(last_image_path)
    last_frame = cv2.resize(last_frame, (width, height))  # Rescale to match the size of the first image
    for _ in range(hold_last_frames):
        frames.append(last_frame)

    # Find ffmpeg.exe in the current script's directory
    ffmpeg_path = None
    for file in os.listdir(folder_path):
        if file.lower() == 'ffmpeg.exe':
            ffmpeg_path = os.path.join(folder_path, file)
            break

    if not ffmpeg_path:
        print("Error: ffmpeg.exe not found in the script's directory.")
        return
    
    # Quality options mapping to bitrates
    bitrate_options = {
        'low': '1000k',
        'medium': '2000k',
        'high': '3000k',
        'very_high': '4000k',
        'ultra_high': '5000k',
        'custom': custom_bitrate
    }

    # Set default quality option if not provided or invalid
    if quality_option not in bitrate_options:
        print(f"Invalid quality option. Using default bitrate ('low').")
        quality_option = 'low'

    bitrate = bitrate_options[quality_option]

    # Write the frames to a video file using FFmpeg
    fourcc = 'libx264'
    
    process = subprocess.Popen([
        ffmpeg_path,
        '-y',
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-s', f'{width}x{height}',
        '-pix_fmt', 'bgr24',
        '-r', f'{1000 / delay_ms}',
        '-i', '-',
        '-c:v', fourcc,
        '-b:v', bitrate,  # Set bitrate here
        '-pix_fmt', 'yuv420p',
        output_file
    ], stdin=subprocess.PIPE)

    for frame in frames:
        process.stdin.write(frame.tobytes())

    process.stdin.close()
    process.wait()

    print(f"Video saved as {output_file}")

# Prompt user for delay in milliseconds
while True:
    try:
        delay_ms = int(input("Enter the delay between frames in milliseconds (must be at least 10ms): "))
        if delay_ms < 10:
            raise ValueError("The delay must be at least 10 milliseconds.")
        break
    except ValueError as e:
        print(f"Invalid input: {e}")

# Prompt user for sorting option
while True:
    try:
        print("Sort images by:")
        print("1. Name")
        print("2. Date")
        sort_choice = int(input("Enter your choice (1-2): "))
        if sort_choice == 1:
            sort_by = 'name'
            break
        elif sort_choice == 2:
            sort_by = 'date'
            break
        else:
            raise ValueError("Invalid choice.")
    except ValueError as e:
        print(f"Invalid input: {e}")

# Prompt user for holding start and end frames
hold_start_end = input("Do you want to hold the first and last frames for a different duration? (y/n): ").strip().lower()

if hold_start_end == 'y':
    try:
        hold_first_ms = int(input("Enter the duration to hold the first frame in milliseconds: "))
        hold_last_ms = int(input("Enter the duration to hold the last frame in milliseconds: "))
        if hold_first_ms <= 0 or hold_last_ms <= 0:
            raise ValueError("The duration must be a positive integer.")
    except ValueError as e:
        print(f"Invalid input: {e}")
    else:
        # Prompt user for quality option
        try:
            print("Select the quality option:")
            print("1. Low (1000k)")
            print("2. Medium (2000k)")
            print("3. High (3000k)")
            print("4. Very High (4000k)")
            print("5. Ultra High (5000k)")
            print("6. Custom")
            choice = int(input("Enter your choice (1-6): "))
            custom_bitrate = None
            if choice == 1:
                quality_option = 'low'
            elif choice == 2:
                quality_option = 'medium'
            elif choice == 3:
                quality_option = 'high'
            elif choice == 4:
                quality_option = 'very_high'
            elif choice == 5:
                quality_option = 'ultra_high'
            elif choice == 6:
                quality_option = 'custom'
                while True:
                    try:
                        custom_bitrate = input("Enter custom bitrate (e.g., 6000k or 6000): ").strip()
                        if custom_bitrate.endswith('k'):
                            custom_bitrate = custom_bitrate
                        else:
                            custom_bitrate = custom_bitrate + 'k'
                        break
                    except ValueError as e:
                        print(f"Invalid input: {e}")
            else:
                raise ValueError("Invalid choice.")
        except ValueError as e:
            print(f"Invalid input: {e}")
        else:
            images_to_video(delay_ms, True, True, hold_first_ms, hold_last_ms, quality_option, custom_bitrate, sort_by)
else:
    # Prompt user for quality option
    try:
        print("Select the quality option:")
        print("1. Low (1000k)")
        print("2. Medium (2000k)")
        print("3. High (3000k)")
        print("4. Very High (4000k)")
        print("5. Ultra High (5000k)")
        print("6. Custom")
        choice = int(input("Enter your choice (1-6): "))
        custom_bitrate = None
        if choice == 1:
            quality_option = 'low'
        elif choice == 2:
            quality_option = 'medium'
        elif choice == 3:
            quality_option = 'high'
        elif choice == 4:
            quality_option = 'very_high'
        elif choice == 5:
            quality_option = 'ultra_high'
        elif choice == 6:
            quality_option = 'custom'
            while True:
                try:
                    custom_bitrate = input("Enter custom bitrate (e.g., 6000k or 6000): ").strip()
                    if custom_bitrate.endswith('k'):
                        custom_bitrate = custom_bitrate
                    else:
                        custom_bitrate = custom_bitrate + 'k'
                    break
                except ValueError as e:
                    print(f"Invalid input: {e}")
        else:
            raise ValueError("Invalid choice.")
    except ValueError as e:
        print(f"Invalid input: {e}")
    else:
        images_to_video(delay_ms, False, False, delay_ms, delay_ms, quality_option, custom_bitrate, sort_by)
