"""
train_model.py
----------------
Trains a YOLOv8 object-detection model to detect potholes.
This is the "our trained model of images" part of the project.

STEP 1 - Get a dataset
-----------------------
Use a public pothole dataset, e.g. (search on Kaggle/Roboflow):
    - "Pothole Detection Dataset" (Roboflow Universe)
    - "Annotated Potholes Dataset" (Kaggle)

Download it in YOLOv8 format. Roboflow lets you export directly in
YOLOv8 format with a data.yaml file already generated - easiest option
for an MSc project.

Your folder should look like:
    backend/model/dataset/
        data.yaml
        train/images, train/labels
        valid/images, valid/labels
        test/images,  test/labels

STEP 2 - Train
--------------
Run this script:
    python train_model.py

It fine-tunes a small pretrained YOLOv8 model (yolov8n.pt) on your
pothole dataset, which is fast enough to run on a laptop CPU for a
class project (a GPU / Google Colab will be much faster).

STEP 3 - Use the result
------------------------
After training, copy the best weights to where app.py expects them:
    runs/detect/train/weights/best.pt  ->  backend/model/pothole_best.pt
"""

from ultralytics import YOLO

DATASET_YAML = "dataset/data.yaml"   # path to your downloaded dataset config
EPOCHS = 50
IMAGE_SIZE = 640


def main():
    # Start from a small pretrained model (transfer learning) instead of
    # training from scratch - much faster and needs less data.
    model = YOLO("yolov8n.pt")

    model.train(
        data=DATASET_YAML,
        epochs=EPOCHS,
        imgsz=IMAGE_SIZE,
        batch=8,
        name="pothole_train",
    )

    # Validate on the held-out validation set
    metrics = model.val()
    print(metrics)

    print("\nTraining complete.")
    print("Copy 'runs/detect/pothole_train/weights/best.pt' to "
          "'backend/model/pothole_best.pt' and restart app.py")


if __name__ == "__main__":
    main()
