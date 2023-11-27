#main script file to be run

from video_processing import *
from image_processing import *
from dependency import *
from dataframe import *
import sys

# Initialize the video(dynamic frames) and image(static) capture object
video_path = "dataset_scrape/video/video.mp4"
image_folder_path = "dataset_scrape/imgs/traffic_images_hds"

if __name__ == '__main__':
    try:
        # Uncomment below function for a single video processing
        #realTime(video_path)
        
        # Or uncomment the line below to run the image processing function for images in a folder 
        process_images_in_folder(image_folder_path)

    except Exception as e:
        print(f"An error occurred during image processing: {e}")

    finally:

        # Call the create_dataframe function, even if terminated manually
        sys.exit(0)


