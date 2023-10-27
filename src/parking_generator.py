import cv2
import pickle


def generator():
    width, height = 40, 80

    try:
        with open("data/source/Sample_3", "rb") as f:
            posList = pickle.load(f)
    except:
        posList = []

    def mouseClick(events, x, y, flags, params):
        if events == cv2.EVENT_LBUTTONDOWN:
            posList.append((x, y))
        if events == cv2.EVENT_RBUTTONDOWN:
            for i, pos in enumerate(posList):
                x1, y1 = pos
                if x1 < x < x1 + width and y1 < y < y1 + height:
                    posList.pop(i)

        with open("data/source/Sample_3", "wb") as f:
            pickle.dump(posList, f)

    while True:
        img = cv2.imread("data/source/output_2.jpg")
        for pos in posList:
            cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

        cv2.imshow("Image", img)
        cv2.setMouseCallback("Image", mouseClick)
        # exit condition
        if cv2.waitKey(1) == ord("q"):
            break
        if cv2.waitKey(1) == ord("s"):
            cv2.imwrite("output.jpg", img)


    cv2.destroyAllWindows()


if __name__ == "__main__":
    generator()
