import cv2
from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.pt")  # load an official model

# Load an image
image = cv2.imread('intersection.png')

# Predict with the model
results = model(image)  # predict on an image
"""======================================================================="""
# img = results[0].plot()  
# cv2.namedWindow('Detection Results', cv2.WINDOW_NORMAL)
# cv2.imshow('Detection Results', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
"""======================================================================="""