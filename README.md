# Vehicle Counting, Classification & Detection using OpenCV & Python

- [Overview](#overview)
- [Steps for Vehicle Detection and Classification using OpenCV](#steps-for-vehicle-detection-and-classification-using-opencv)
- [Notes and Precautions](#notes-and-precautions)
- [Prerequisites](#prerequisites)
- [Description](#description)
  - [Main](#main)
  - [Tracker](#tracker)
  - [Dependency](#dependency)
  - [Count Vehicle](#count-vehicle)
  - [Video Processing](#video-processing)
  - [Data Preparation](#data-preparation)
  - [Image Processing](#image-processing)
  - [DataFrame Creation](#dataframe-creation)
- [Summary](#summary)

## Overview

This project involves vehicle detection and classification using OpenCV and the YOLOv3 model on the dataset prepared by scraping google images.

## Steps for Vehicle Detection and Classification using OpenCV

1. **Download the project folder in your system.**
2. **Adjust the local paths wherever necessary.**
3. **You can webscrape to create dataset by running data_preparation.py or use the already present dataset.**
4. **Use one of realTime() or process_images_in_folder() function in Main.py at a time.**
5. **There is only one video for dynamic frames processing.**
6. **After all images processed dataframe will be created in same directory if program is not killed prematurely.**

## Notes and Precautions

1. Ensure you have the required libraries and dependencies installed.
2. Download the YOLOv3 model weights and configuration files.
3. Use caution when setting the number of images for data preparation.
4. To terminate the processing press 'q' to avoid unexpected results.
5. Results obtained in csv files for both image and video are cumulative.
6. For actual results, dataframe is created using dataframe.py file.

### Prerequisites

```bash
- Python – 3.9
- OpenCV – 4.4.0
- Numpy – 1.20.3
- Pandas - 1.5.3
- requests: 2.25.1
- beautifulsoup4 (bs4): 4.9.3
- YOLOv3 Pre-trained model weights and Config Files
```

## Description

### Main

1. Initializes video and image capture objects, allowing either real-time video processing or batch image processing.
2. It handles exceptions during execution and ensures the creation of a DataFrame even if manually terminated.

### Tracker

1. Uses the Euclidean_distance concept to keep track of an object. It calculates the difference between two center points of an object in the current frame vs the previous frame, and if the distance is less than the threshold distance, it confirms that the object is the same object of the previous frame.
2. Assigns unique IDs to newly detected objects.
3. The find_center function computes the center of a rectangle.

### Dependency

1. This script initializes a YOLOv3-based object detection model using OpenCV, with a tracker for object tracking.
2. It sets up parameters such as confidence thresholds, line positions, and class indices.
3. Uses a pre-trained YOLOv3 model to detect vehicles, and it maintains counters for vehicles crossing specified lines.

### Count Vehicle

1. The postProcess function takes YOLOv3 model outputs, extracts relevant information about detected objects, applies Non-Maximum Suppression, and draws bounding boxes with class names and confidence scores on the input image.
2. It then updates a tracker, identifies and counts vehicles based on their movement across specified lines, and displays real-time count statistics for different vehicle classes.

### Video Processing

1. The realTime function processes frames from a video stream, updating vehicle counts in real-time and displaying the processed frame.
2. Detected vehicle frequencies are also saved to a CSV file. The function uses OpenCV for video handling, vehicle counting, and frame display.

### Data Preparation

1. The script downloads images related to traffic from Google using BeautifulSoup and requests, then saves them to a specified folder. 2. It dynamically creates a directory for the images and allows the user to specify the number of images to download.

### Image Processing

1. The script processes static images in a specified folder, detecting vehicles and counting their occurrences.
2. It uses OpenCV to read and analyze each image, displaying the results and saving them to a CSV file.
3. The image processing function is applied to each image in the folder, providing a comprehensive analysis.

### DataFrame Creation

1. Creates a pandas DataFrame from cumulative image processing results, calculates the difference between consecutive rows, and saves the final results to a CSV file named "results_final.csv".

## Summary

In this project, we've built an advanced vehicle detection and classification system using OpenCV. We've used the YOLOv3 algorithm along with OpenCV to detect and classify objects, incorporating deep neural networks, file handling systems, and advanced computer vision techniques.
