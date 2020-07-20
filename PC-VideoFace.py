import cv2
import os
# 検出器の読み込み
cascades_dir = os.path.join('OpenCV', 'data', 'haarcascades')
cascade_f = cv2.CascadeClassifier(os.path.join(
    cascades_dir, 'haarcascade_frontalface_alt2.xml'))
# ESCキー番号
esc = 27
# webカメラ起動
cap = cv2.cv2.VideoCapture(0)
# ちゃんと起動できたかチェック
if not cap.isOpened():
    raise Exception('Web camera is not detected')

while True:
    # フレームの取得
    ret, frame = cap.read()

    # グレイスケールに変換
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 顔の検出
    faces = cascade_f.detectMultiScale(gray)

    for (x, y, w, h) in faces:
        # 四角で囲む
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 2)

    # 動画の表示
    cv2.imshow('video', frame)

    # escキーで終了
    if cv2.waitKey(1) & 0xFF == esc:
        break
# webカメラのリリース
cap.release()
cv2.destroyAllWindows()
