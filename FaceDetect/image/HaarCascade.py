import numpy as np
import cv2, matplotlib
import matplotlib.pyplot as plt

def read_img(name_i):
    img = cv2.imread(name_i)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def Hear_Cascade(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('/Users/takahashisusumunari/src/opencv3/data/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('/Users/takahashisusumunari/src/opencv3/data/haarcascades/haarcascade_eye.xml')

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    return img


# 画像の表示
def plot():
    # 画像の読み込み
    img = read_img('./lenna.jpg')
    img=HearCascade(img)
    cv2.imshow('img',img)
    cv2.waitKey(0)

    cv2.destroyAllWindows()
