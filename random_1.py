import pytesseract
import cv2

myconfig=r"--psm 6 --oem 3"

image = cv2.imread('image.png')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
text = pytesseract.image_to_string(gray)
print(text)