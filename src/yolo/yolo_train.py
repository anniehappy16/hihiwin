"""
YOLOv8 模型訓練腳本
"""

from ultralytics import YOLO
import os
from pathlib import Path

def train_yolov8():
    """訓練YOLOv8模型"""
    
    # 資料集配置檔案路徑
    model = YOLO('yolov8n.pt')  
    # 開始訓練
    results = model.train(
        data="dataset/data.yaml",# 資料集配置
        epochs=50,                   # 訓練輪數
        imgsz=640,                  # 圖片尺寸
        project="runs/train",
        name="best",
    )
    
    return results



if __name__ == "__main__":
    train_yolov8()
