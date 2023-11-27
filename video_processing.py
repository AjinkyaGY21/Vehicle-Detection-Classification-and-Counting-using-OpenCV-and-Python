from dependency import *
from count_vehicle import *

def from_video_frame(frame):

    # Print the shape of the original frame
    # print(f"Frame Shape: {frame.shape}")

    # Resize the frame
    frame = cv2.resize(frame, (0, 0), None, 0.5, 0.5)

    ih, iw, _ = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 1 / 255, (input_size, input_size), [0, 0, 0], 1, crop=False)

    # Set the input of the network
    net.setInput(blob)
    layersNames = net.getLayerNames()
    unconnected_out_layers = net.getUnconnectedOutLayers()

    # Check if unconnected_out_layers is not empty
    if not unconnected_out_layers.any():
        print("Error: Unconnected Out Layers is empty.")
        return

    # Ensure that unconnected_out_layers is a list of lists
    if not isinstance(unconnected_out_layers[0], list):
        unconnected_out_layers = [unconnected_out_layers]

    outputNames = [layersNames[i - 1] for i in unconnected_out_layers[0]]

    # Feed data to the network
    outputs = net.forward(outputNames)

    # Find the objects from the network output
    postProcess(outputs, frame)

    # Count the frequency of detected classes
    frequency = collections.Counter(detected_classNames)
    #print(frequency)

    # Draw counting texts in the frame
    cv2.putText(frame, "Car:        " + str(frequency['car']), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, font_size,
                font_color, font_thickness)
    cv2.putText(frame, "Motorbike:  " + str(frequency['motorbike']), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size,
                font_color, font_thickness)
    cv2.putText(frame, "Bus:        " + str(frequency['bus']), (20, 80), cv2.FONT_HERSHEY_SIMPLEX, font_size,
                font_color, font_thickness)
    cv2.putText(frame, "Truck:      " + str(frequency['truck']), (20, 100), cv2.FONT_HERSHEY_SIMPLEX, font_size,
                font_color, font_thickness)

    cv2.imshow("Video Frame", frame)

    if cv2.waitKey(1) == ord('q'):
        return True  # Indicate to stop processing frames
    
    # Save the data to a CSV file for the current frame
    with open("results_video.csv", 'a') as f1:
        cwriter = csv.writer(f1)
        cwriter.writerow([frame, frequency['car'], frequency['motorbike'], frequency['bus'], frequency['truck']])
    f1.close()
    
    return False  # Continue processing frames



# For vehicle detection in a moving streams of images (video)
def realTime(video_path):
    cap = cv2.VideoCapture(video_path)

    while True:
        success, frame = cap.read()

        if not success:
            print("Error: Failed to read frame from the video capture.")
            break

        # Process the current frame
        stop_processing = from_video_frame(frame)

        if stop_processing:
            break

    # Release the capture object and destroy all active windows
    cap.release()
    cv2.destroyAllWindows()