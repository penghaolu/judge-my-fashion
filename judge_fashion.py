import cv2
import numpy as np
import argparse
import tensorflow as tf

class JudgeFashion():
    def __init__(self, img_size=640, model_path="./trained_modelv1.tflite", use_gpu=False, w="./yolov3.weights", cfg="./yolo.cfg"):
        self.w = w
        self.cfg = cfg

        self.IMG_SIZE = img_size
        self.tflite_interpreter = tf.lite.Interpreter(model_path=model_path)
    
        self.tflite_interpreter.allocate_tensors()
        self.input_details = self.tflite_interpreter.get_input_details()
        self.output_details = self.tflite_interpreter.get_output_details()
        self.input_shape = self.input_details[0]['shape']
        self.net = cv2.dnn.readNet(self.w, self.cfg)

        if use_gpu:
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)


        
    def get_output_layers(self, net):
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        return output_layers


    def fix_img_size(self, im, desired_size=640):
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

    def getYoloPredictions(self, frame, YOLO_NET):
        class_ids = []
        confidences = []
        boxes = []
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0,0,0), True, crop=False)
        YOLO_NET.setInput(blob)
        outs = YOLO_NET.forward(self.get_output_layers(YOLO_NET))
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

    def crop_out_person(self, img, YOLO_NET=None):

        if YOLO_NET == None:
            YOLO_NET = self.net

        img = self.fix_img_size(img, self.IMG_SIZE)
        predictions, boxes, labels = self.getYoloPredictions(img, YOLO_NET)
        person_bboxes = []
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
            person_bboxes.append([x,y,w,h])
        
        return person_bboxes



    def get_fashion_results(self, image):
        bboxes = self.crop_out_person(image)

        for bbox in bboxes:

            try:
                x,y,w,h = bbox

                x2 = int(x+w)
                y2 = int(y+h)

                x = np.clip(int(x), 0, image.shape[1])
                y = np.clip(int(y), 0, image.shape[0])
                x2 = np.clip(int(x2), 0, image.shape[1])
                y2 = np.clip(int(y2), 0, image.shape[0])

                person_croped = image[int(y):y2, int(x):x2,:]
                
                if x == x2 or y == y2:
                    person_croped = image
                
                fix_sized_img = np.array([self.fix_img_size(person_croped, 160)]).astype(np.float32)
                # print(fix_sized_img.shape)
                self.tflite_interpreter.set_tensor(self.input_details[0]['index'], fix_sized_img)
                self.tflite_interpreter.invoke()

                results = np.squeeze(self.tflite_interpreter.get_tensor(self.output_details[0]['index']))
                return results
            except:
                print(bbox, 'failed')

        return None

import matplotlib.pyplot as plt

def main():
    img = plt.imread('techwear.jpg')
    jf = JudgeFashion(model_path="./trained_modelv2_final.tflite", use_gpu=False, w="./person_detection/yolov3.weights", cfg="./person_detection/yolo.cfg")
    res = jf.get_fashion_results(img)

    print(res)

if __name__ == '__main__':
    main()
