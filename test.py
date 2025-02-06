import cv2

# Replace with your IP camera's URL
ip_camera_url = "rtsp://192.168.0.104:554/user=admin_password=tlJwpbo6_channel=0_stream=0&onvif=0.sdp?real_stream"  # Example: "http://192.168.1.100:8080/video"

# Connect to the IP camera
cap = cv2.VideoCapture(ip_camera_url)

if not cap.isOpened():
    print("Error: Unable to connect to the IP camera.")
else:
    # Capture a frame
    ret, frame = cap.read()
    if ret:
        # Save the frame as an image
        cv2.imwrite("captured_image.jpg", frame)
        print("Photo saved as 'captured_image.jpg'")
    else:
        print("Error: Unable to capture a frame.")

# Release the connection
cap.release()
