import cv2
import numpy as np
import pyrebase
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()


def load_parking_positions(file_path):
    posList = []
    with open(file_path, "r") as f:
        for line in f:
            x, y = line.split(",")
            posList.append((int(x), int(y)))
    return posList


def update_firebase_batch(updates):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    batch_data = {}

    for slot_number, status in updates.items():
        batch_data[f"slot_{slot_number}"] = {"slot": status, "update": now}

    db.update(batch_data)


def test():
    rect_width, rect_height = 40, 80
    carp_park_positions_path = "data/source/Sample_3"
    video_path = "data/source/sample_3.mp4"
    posList = load_parking_positions(carp_park_positions_path)

    cap = cv2.VideoCapture(video_path)
    # Increase the frame rate to 60 frames per second (adjust as needed)
    cap.set(cv2.CAP_PROP_FPS, 10)
    cv2.namedWindow("Parking Lot", cv2.WINDOW_NORMAL)

    def checkParkingSpace(imgPro):
        spaceCounter = 0
        update_batch = {}  # Collect updates in a batch

        for index, pos in enumerate(posList, start=1):
            x, y = pos

            imgCrop = imgPro[y : y + rect_height, x : x + rect_width]
            count = cv2.countNonZero(imgCrop)

            if count < 800:
                color = (0, 255, 0)
                thickness = 2
                status = "Free"
                spaceCounter += 1

            else:
                color = (0, 0, 255)
                thickness = 1
                status = "Occupied"

            cv2.rectangle(
                img, pos, (pos[0] + rect_width, pos[1] + rect_height), color, thickness
            )
            cv2.putText(
                img, str(count), (x + 5, y + 15), cv2.FONT_HERSHEY_PLAIN, 1, color, 1
            )

            update_batch[index] = status

        update_firebase_batch(update_batch)  # Send batched updates

        cv2.putText(
            img,
            f"Free: {spaceCounter}/{len(posList)}",
            (10, 50),
            cv2.FONT_HERSHEY_PLAIN,
            2,
            (0, 200, 0),
            3,
        )

    while True:
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 10)
        success, img = cap.read()
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
        imgThreshold = cv2.adaptiveThreshold(
            imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16
        )
        imgMedian = cv2.medianBlur(imgThreshold, 5)
        kernel = np.ones((3, 3), np.uint8)
        imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

        checkParkingSpace(imgDilate)

        cv2.imshow("Parking Lot", img)
        cv2.imshow("ImageBlur", imgBlur)
        cv2.imshow("ImageThres", imgMedian)
        k = cv2.waitKey(50)
        if k & 0xFF == ord("q"):
            break
        if k & 0xFF == ord("s"):
            cv2.imwrite("output.jpg", img)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    test()
