# Function for count vehicle
from dependency import *
from tracker import *

def count_vehicle(box_id, img):
    global detected_classNames, up_list, down_list
    x, y, w, h, id, index = box_id

    # Find the center of the rectangle for detection
    center = find_center(x, y, w, h)
    ix, iy = center

    # Find the current position of the vehicle
    if (iy > up_line_position) and (iy < middle_line_position):
        if id not in temp_up_list:
            temp_up_list.append(id)
    elif iy < down_line_position and iy > middle_line_position:
        if id not in temp_down_list:
            temp_down_list.append(id)
    elif iy < up_line_position:
        if id in temp_down_list:
            temp_down_list.remove(id)
            down_list[index] = down_list[index] + 1
            # Directly update the legend text
            legend_text = f'{classNames[required_class_index[index]]} Up: {up_list[index]}, Down: {down_list[index]}'
            cv2.putText(img, legend_text, (20, 40 + index * 20), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                        font_thickness)
    elif iy > down_line_position:
        if id in temp_up_list:
            temp_up_list.remove(id)
            up_list[index] = up_list[index] + 1
            # Directly update the legend text
            legend_text = f'{classNames[required_class_index[index]]} Up: {up_list[index]}, Down: {down_list[index]}'
            cv2.putText(img, legend_text, (20, 40 + index * 20), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                        font_thickness)
            
    print(f'{classNames[required_class_index[index]]} Up: {up_list[index]}, Down: {down_list[index]}')
    # Draw circle in the middle of the rectangle
    cv2.circle(img, center, 2, (0, 0, 255), -1)

    cv2.putText(img, "Car:        " + str(up_list[0]) + "     " + str(down_list[0]), (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
    cv2.putText(img, "Motorbike:  " + str(up_list[1]) + "     " + str(down_list[1]), (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
    cv2.putText(img, "Bus:        " + str(up_list[2]) + "     " + str(down_list[2]), (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
    cv2.putText(img, "Truck:      " + str(up_list[3]) + "     " + str(down_list[3]), (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)


def postProcess(outputs, img):
    global detected_classNames
    height, width = img.shape[:2]
    boxes = []
    classIds = []
    confidence_scores = []
    detection = []

    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]

            if classId in required_class_index and confidence > confidenceThreshold:
                w, h = int(det[2] * width), int(det[3] * height)
                x, y = int((det[0] * width) - w / 2), int((det[1] * height) - h / 2)
                boxes.append([x, y, w, h])
                classIds.append(classId)
                confidence_scores.append(float(confidence))

    # Apply Non-Max Suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidence_scores, confidenceThreshold, nmsThreshold)

    # Check if indices is not empty and is a NumPy array with any elements
    if indices is not None and len(indices) > 0:
        # Ensure indices is a NumPy array
        indices = indices.flatten()

        for i in indices:
            x, y, w, h = boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3]

            color = [int(c) for c in colors[classIds[i]]]

            # Draw confidence score and class name
            class_name = classNames[classIds[i]]
            confidence_text = f'CONFIDENCE: {int(confidence_scores[i] * 100)}%'
            cv2.putText(img, f'{class_name}: {confidence_text}', (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

            # Draw bounding rectangle
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
            detection.append([x, y, w, h, required_class_index.index(classIds[i])])

            # Store the detected class name for further processing if needed
            detected_classNames.append(class_name)

        # Update the tracker for each object
        boxes_ids = tracker.update(detection)
        for box_id in boxes_ids:
            count_vehicle(box_id, img)

    else:
        print("No objects detected.")
