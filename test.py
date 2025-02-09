import cv2

cap = cv2.VideoCapture(
    "rtsp://192.168.0.104:554/user=admin_password=tlJwpbo6_channel=0_stream=0&onvif=0.sdp?real_stream"
)

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.resize(frame, (960, 540))
    cv2.imshow("frame", frame)
    if cv2.waitKey(20) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
