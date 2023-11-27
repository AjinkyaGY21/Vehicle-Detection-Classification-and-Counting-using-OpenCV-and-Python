import os
from dependency import *
from count_vehicle import *

# For vehicle detection in an image
def from_static_image(image):
    global detected_classNames  # Add this line

    detected_classNames = []  # Clear the list for each image

    img = cv2.imread(image)

    if img is None:
        print(f"Error: Unable to load image at path: {image}")
        return

    print(f"Image loaded successfully: {img.shape}")

    blob = cv2.dnn.blobFromImage(img, 1 / 255, (input_size, input_size), [0, 0, 0], 1, crop=False)

    # Set the input of the network
    net.setInput(blob)
    layersNames = net.getLayerNames()
    unconnected_out_layers = net.getUnconnectedOutLayers()

    #print("Unconnected Out Layers:", unconnected_out_layers)

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
    postProcess(outputs, img)

    # Count the frequency of detected classes
    frequency = collections.Counter(detected_classNames)
    print(frequency)

    # Draw counting texts in the frame
    cv2.putText(img, "Car:        " + str(frequency['car']), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, font_size,
                font_color, font_thickness)
    cv2.putText(img, "Motorbike:  " + str(frequency['motorbike']), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size,
                font_color, font_thickness)
    cv2.putText(img, "Bus:        " + str(frequency['bus']), (20, 80), cv2.FONT_HERSHEY_SIMPLEX, font_size,
                font_color, font_thickness)
    cv2.putText(img, "Truck:      " + str(frequency['truck']), (20, 100), cv2.FONT_HERSHEY_SIMPLEX, font_size,
                font_color, font_thickness)

    cv2.imshow("image", img)

    cv2.waitKey(0)

    # Save the data to a CSV file
    with open("results_image.csv", 'a') as f1:
        cwriter = csv.writer(f1)
        cwriter.writerow([image, frequency['car'], frequency['motorbike'], frequency['bus'], frequency['truck']])
    f1.close()


def process_images_in_folder(folder_path):
    # List all files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]

    # Loop through each image file
    for image_file in image_files:
        # Construct the full path to the image
        image_path = os.path.join(folder_path, image_file)

        from_static_image(image_path)

    cv2.destroyAllWindows()