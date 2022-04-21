#
#
#
import numpy as np
import onnxruntime as ort
import cv2


if __name__== '__main__':
    model_path = '../models/object_detection_3d_camera.onnx'


    # x = np.random.random((1,3,224,224)).astype(np.float32)
    # ort_sess = ort.InferenceSession( model_path )
    # outputs = ort_sess.run(None, {'input_1': x})


    net = cv2.dnn.readNetFromONNX(model_path)

    # textGraph = ""
    # modelWeights = ""
    # net = cv2.dnn.readNetFromTensorflow(modelWeights, textGraph);