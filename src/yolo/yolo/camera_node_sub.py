#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from ultralytics import YOLO
from std_msgs.msg import String
import json


class YoloNode(Node):
    def __init__(self):
        super().__init__('yolo_sub')

        self.bridge = CvBridge()

        self.rgb_sub = self.create_subscription(
            Image,
            '/camera/camera/color/image_raw',
            self.rgb_callback,
            10
        )
        self.depth_sub = self.create_subscription(
            Image,
            '/camera/camera/aligned_depth_to_color/image_raw',
            self.depth_callback,
            10
        ) 

        self.depth_image =None
        self.model = YOLO('src/yolo/best.pt')
        self.publisher = self.create_publisher(String, 'yolo_detections', 10)

    def depth_callback(self, msg):
        self.depth_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")


    def rgb_callback(self, msg):
        

        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        results = self.model(image,conf=0.6)

        # Extract bounding boxes and other details
        # Extract bounding boxes and other details
        detections = []
        annotated_image = results[0].plot()
        for result in results[0].boxes:
            confidence = result.conf[0].item()  # Confidence score

            bbox = result.xyxy[0].tolist()  # Bounding box coordinates [x_min, y_min, x_max, y_max]
            class_id = result.cls[0].item()  # Class ID
            

            x_min, y_min, x_max, y_max = map(int,bbox)
            roi = image[y_min:y_max, x_min:x_max]
            if roi.size != 0:
                gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                _, thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                if len(contours) > 0:
                    largest_contour = max(contours, key=cv2.contourArea)
                    rect = cv2.minAreaRect(largest_contour)
                    (center_x, center_y), (w, h), angle = rect

                    u = int(center_x + x_min)
                    v = int(center_y + y_min)

                    drpth_raw=None
                    depth_m=None

                    if self.depth_image is not None:
                        drpth_raw=self.depth_image[v,u]
                        depth_m=drpth_raw*0.001

                        fx=909.77309
                        fy=909.173606
                        cx=645.06746
                        cy=366.54143

                        X = (u - cx) * depth_m / fx
                        Y = (v - cy) * depth_m / fy
                        Z = depth_m


                        # 如果你想換成 mm
                        X_mm = X * 1000
                        Y_mm = Y * 1000
                        Z_mm = Z * 1000


                        cv2.circle(annotated_image, (u, v), 5, (0, 0, 255), -1)
                        # cv2.putText(annotated_image, f"angle={angle:.2f},depth={depth_m:.2f}",(u + 10, v),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                        cv2.putText(annotated_image, f"x={X_mm:.2f},y={Y_mm:.2f},z={Z_mm:.2f}",(u + 10, v),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

                        detections.append({
                            "bbox": bbox,
                            "confidence": confidence,
                            "class_id": class_id,
                            "angle": angle,
                            "camera_xyz":[X_mm, Y_mm,Z_mm]

                        })
                    

        


        # Send detections to another node or save to a file
        # with open("./detections.json", "w") as f:
        #     json.dump(detections, f)
        # print("Detections saved to detections.json")
        j_detections=json.dumps(detections)

        # Render predictions on the image
    


        msg = String()
        msg.data = j_detections
        self.publisher.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)

        cv2.imshow("Detection Results", annotated_image)
        cv2.waitKey(1)


def main():
    rclpy.init()
    node = YoloNode()
    rclpy.spin(node)


    cv2.destroyAllWindows()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
