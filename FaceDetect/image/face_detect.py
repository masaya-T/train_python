import cv2
import sys
import HaarCascade

def output_image(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imshow('img',img)
    cv2.waitKey(0)
    

camera_id = 0
delay = 0
window_name = 'frame'

cap = cv2.VideoCapture(camera_id)
path = "sdf.jpg"

if not cap.isOpened():
    sys.exit()


while True:
    # 最新の画像の読み込み
    ret, frame = cap.read()

     # Reload on error 
    if ret == False:
        continue

    # 
    frame = HaarCascade.Hear_Cascade(frame)

    
    output_image(frame)

    # 何らかのキーが押されたら終了 
    key = cv2.waitKey(1)
    if key != -1:
        break

