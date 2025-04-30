import cv2
import sqlite3
from ultralytics import YOLO

# Load the YOLO model
model = YOLO("yolov8n.pt")  # Replace with 'best.pt' if you have your trained model

# Connect to the database
conn = sqlite3.connect("plates.db")
cursor = conn.cursor()

# Start webcam
cap = cv2.VideoCapture(0)  # Use 0 for default camera

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO detection on the frame
    results = model(frame)

    # Draw results and check if any plate is detected
    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Simulated class check: assume class 0 is a license plate
            if conf > 0.5:
                # Crop the region
                plate_crop = frame[y1:y2, x1:x2]

                # For now we simulate reading the plate
                fake_plate = "ABC123"

                # Check against DB
                cursor.execute("SELECT * FROM authorized_vehicles WHERE plate=?", (fake_plate,))
                result = cursor.fetchone()

                color = (0, 255, 0) if result else (0, 0, 255)
                status = "ACCESS GRANTED" if result else "ACCESS DENIED"

                # Draw box and label
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, status, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Live Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# detect_and_check.py

print("Garage Gate Plate Detection System Starting...")

# Future steps:
# - Load YOLO model
# - Capture image or stream from camera
# - Detect license plates
# - Check against plates.db SQLite database
# - Allow or deny access

print("This is a test run. Everything is working!")
