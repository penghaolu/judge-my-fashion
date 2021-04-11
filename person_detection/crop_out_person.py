import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--use_gpu', default=False, action='store_true', help='Use GPU')

args = parser.parse_args()

w = "./yolov3.weights"
cfg = "./yolo.cfg"


net = cv2.dnn.readNet(w,cfg)
if args.use_gpu:
    print('Using GPU')
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)


def get_output_layers(net):
	layer_names = net.getLayerNames()
	output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
	return output_layers


def fix_img_size(im, desired_size=460):
    old_size = im.shape[:2] # old_size is in (height, width) format

    ratio = float(desired_size)/max(old_size)
    new_size = tuple([int(x*ratio) for x in old_size])

    # new_size should be in (width, height) format

    im = cv2.resize(im, (new_size[1], new_size[0]))

    delta_w = desired_size - new_size[1]
    delta_h = desired_size - new_size[0]
    top, bottom = delta_h//2, delta_h-(delta_h//2)
    left, right = delta_w//2, delta_w-(delta_w//2)

    color = [0, 0, 0]
    new_im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT,
        value=color)

    return new_im

def getYoloPredictions(frame, YOLO_NET):
    class_ids = []
    confidences = []
    boxes = []
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0,0,0), True, crop=False)
    YOLO_NET.setInput(blob)
    outs = YOLO_NET.forward(get_output_layers(YOLO_NET))
    width = frame.shape[1]
    height = frame.shape[0]

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x,y,w,h])
        
        indices =  cv2.dnn.NMSBoxes(boxes, confidences,  0.5,  0.4)
        return indices, boxes, class_ids


def crop_out_person(img, YOLO_NET=net):
    img = fix_img_size(img, 640)
    predictions, boxes, labels = getYoloPredictions(img, YOLO_NET)
    for currentPrediction in predictions:
        currentPrediction = currentPrediction[0]
        if labels[currentPrediction] != 0:
            continue

        box = boxes[currentPrediction]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        label = str(labels[currentPrediction])
        return ([x,y,w,h])
