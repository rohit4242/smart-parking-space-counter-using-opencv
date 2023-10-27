import cv2
import pickle
import numpy as np
import cvzone
def test():
    rect_width, rect_height = 40,  80
    carp_park_positions_path = "data/source/Sample_3"
    video_path = "data/source/sample_3.mp4"
    with open(carp_park_positions_path, 'rb') as f:
        posList = pickle.load(f)

    cap = cv2.VideoCapture(video_path)

    cv2.namedWindow("Parking Lot", cv2.WINDOW_NORMAL)
    
    def checkParkingSpace(imgPro):
        spaceCounter = 0

        for pos in posList:
            x, y = pos

            imgCrop = imgPro[y:y + rect_height, x:x + rect_width]
            count = cv2.countNonZero(imgCrop)


            if count < 800:
                color = (0, 255, 0)
                thickness = 2
                spaceCounter += 1
            else:
                color = (0, 0, 255)
                thickness = 1

            cv2.rectangle(img, pos, (pos[0] + rect_width, pos[1] + rect_height), color, thickness)
            cvzone.putTextRect(img, str(count), (x, y + rect_height - 3), scale=1,
                            thickness=1, offset=0, colorR=color)

        cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (10, 50), scale=2,
                            thickness=3, offset=20, colorR=(0,200,0))
    while True:

        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        success, img = cap.read()
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
        imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY_INV, 25, 16)
        imgMedian = cv2.medianBlur(imgThreshold, 5)
        kernel = np.ones((3, 3), np.uint8)
        imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)


        checkParkingSpace(imgDilate)

        cv2.imshow("Parking Lot", img)
        cv2.imshow("ImageBlur", imgBlur)
        cv2.imshow("ImageThres", imgMedian)
        k = cv2.waitKey(50)
        if k & 0xFF == ord('q'):
            break
        if k & 0xFF == ord('s'):
            cv2.imwrite("output.jpg", img)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    test()
