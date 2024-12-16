import cv2
import requests
from datetime import datetime
import time

# Backend API endpoint
API_URL = 'http://abstrakxyz.pythonanywhere.com/api/detect_qr_code/'

# Initialize webcam
cap = cv2.VideoCapture(0)
qr_code_detector = cv2.QRCodeDetector()

# Create a named window for OpenCV and set it to fullscreen
cv2.namedWindow("QR Code Scanner", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("QR Code Scanner", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    # Detect QR code
    qr_data, bbox, _ = qr_code_detector.detectAndDecode(frame)

    # Draw a rectangle around detected QR code (if any)
    if bbox is not None:
        bbox = bbox.astype(int)  

        # Check if bbox has 4 points (quadrilateral)
        if len(bbox) == 4:
            # Draw rectangle using the first and third points of bbox
            pt1 = tuple(bbox[0][0])  
            pt2 = tuple(bbox[2][0])  
            cv2.rectangle(frame, pt1, pt2, (0, 255, 0), 3)  

    if qr_data:
        print(f"QR Code detected: {qr_data}")

        # Save screenshot
        screenshot_path = "screenshot.png"
        cv2.imwrite(screenshot_path, frame)
        print("Screenshot saved!")

        # Prepare payload with QR code data and timestamp
        payload = {
            'qr_code': qr_data,
            'timestamp': datetime.now().isoformat(),  
        }

        # Open screenshot file
        with open(screenshot_path, 'rb') as screenshot_file:
            files = {
                'screenshot': screenshot_file, 
            }

            # Send data to server
            try:
                response = requests.post(API_URL, data=payload, files=files)
                if response.status_code == 200:
                    print("Data sent successfully:", response.json())
                    time.sleep(3)
                else:
                    print("Failed to send data:", response.json())
            except Exception as e:
                print(f"Error sending data to server: {e}")

    # Add text to frame
    cv2.putText(frame, "SISTEM PRESENSI DESA TRANGSAN", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the frame in the fullscreen window
    cv2.imshow("QR Code Scanner", frame)

    # Press 'q' to exit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release webcam and destroy all windows
cap.release()
cv2.destroyAllWindows()
