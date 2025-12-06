import cv2
from PIL import Image
import pytesseract as pt

class ExtractText:
    def __init__(self):
        self.ref_point = []
        self.frame = ''
        self.clone = ''
        self.Window1 = 'Live Video'
        self.Window2 = 'Snap'

    def initiate(self):
        cam = cv2.VideoCapture(0)

        while True:
            ret, self.frame = cam.read()
            cv2.rectangle(self.frame, (0, 0), (250, 20), (0, 0, 0), -1)
            cv2.putText(self.frame, 'X:for Snap;     Q: for quit', (10, 15), 2, 0.5, (255, 255, 255))
            cv2.imshow(self.Window1, self.frame)

            key = cv2.waitKey(1) & 0xFF

            # X: for Pic
            if key == ord('x'):
                cv2.destroyWindow(self.Window1)
                break
            if key == ord('q'):
                break

        self.clone = self.frame.copy()

        if key == ord('x'):  # if user took snap
            while True:
                cv2.rectangle(self.frame, (0, 0), (300, 20), (0, 0, 0), -1)
                cv2.putText(self.frame, 'X:for Extract Text;    R: for Reset', (10, 15), 2, 0.5, (255, 255, 255))

                if (len(self.ref_point) == 2):
                    cv2.rectangle(self.frame, self.ref_point[0], self.ref_point[1], (0, 255, 0), 2)
                    cv2.imshow(self.Window2, self.frame)
                else:
                    cv2.imshow(self.Window2, self.frame)

                # Select Shape
                cv2.setMouseCallback(self.Window2, self.shape_selection)

                key = cv2.waitKey(1) & 0xFF

                # Reset
                if len(self.ref_point) > 2 or key == ord('r'):
                    self.frame = self.clone.copy()
                    self.ref_point = []

                # Break Loop
                if key == ord('x'):
                    cv2.destroyWindow(self.Window2)
                    break

            if len(self.ref_point) == 2:
                crop_img = self.clone[self.ref_point[0][1]: self.ref_point[1][1],
                           self.ref_point[0][0]: self.ref_point[1][0]]
                data = cv2.imwrite('temp.png', crop_img)
                while True:
                    if data == True:
                        break
                print('Extracted Text: \n', pt.image_to_string(Image.open('temp.png')))
                cv2.imshow('crop_img', crop_img)
                cv2.waitKey(0)

        cv2.destroyAllWindows()

    def shape_selection(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:  # Mark Coordinates where Left Mouse Button Clicked (Indicating start of Crop)
            self.ref_point = [(x, y)]
        elif event == cv2.EVENT_LBUTTONUP:  # Mark Coordinates where Left Mouse Button Released (Indicating End of Crop)
            self.ref_point.append((x, y))

        if len(self.ref_point) == 2:
            self.frame = self.clone.copy()
            # Draw Rectangle around Reference Points
            cv2.rectangle(self.frame, self.ref_point[0], self.ref_point[1], (0, 255, 0), 2)
            cv2.imshow(self.Window2, self.frame)

if __name__ == '__main__':

    FrameObj = ExtractText()
    FrameObj.initiate()

