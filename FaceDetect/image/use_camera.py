import cv2
import sys
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt


def output_image(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.pause(0.00000001)
    

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

    # 白黒化
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # ぼかし処理
    blur = cv2.GaussianBlur(gray, (0, 0), 5)
    
    output_image(gray)

    if 0xFF == ord('q'):
        break

