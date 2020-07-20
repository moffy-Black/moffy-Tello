import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while (True):
    # フレームを一枚ずつキャプチャー
    ret, frame = cap.read()

    # グレースケールに変更する
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # ディスプレイ表示
    cv2.imshow('original_ver', frame)
    cv2.imshow('gray_ver', gray)
    print(ret)
    if cv2.waitKey(1) & 0xff == ord('q'):  # q-keyを押したらwhileを抜ける
        break

# whileを抜けたら実行
cap.release()  # 読み込み終了
cv2.destroyAllWindows()  # windowを閉じる
