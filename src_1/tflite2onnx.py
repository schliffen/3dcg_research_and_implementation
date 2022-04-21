#
#
#
import tflite2onnx


tflite_path = '../models/object_detection_3d_camera.tflite'
onnx_path = '../models/object_detection_3d_camera.onnx'

if __name__=='__main__':
    tflite2onnx.convert(tflite_path, onnx_path)




