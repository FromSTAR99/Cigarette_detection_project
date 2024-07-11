import cv2
from ultralytics import YOLO
import serial
import torch
  
comment=1
if(comment==0):
    ser = serial.Serial('COM6', 9600)
counter=0
# Load the YOLOv8 model
model = YOLO('C:\\Users\\gameh\\OneDrive\\Masaüstü\\Documents\\Mimari Sigara Tespit Projesi\\Mimari Sigara Tespit Projesi\\sigara1_best.pt')
# Use the model to detect object

# Open the video file
video_path = 0
cap = cv2.VideoCapture(video_path)

# Loop through the video frames
while cap.isOpened():
    if torch.cuda.is_available():
        print ("true")
    else :
        print("False")  
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = model.predict(frame,conf=0.5)
        

        # Visualize the results on the frame
        annotated_frame = results[0].plot()
        print(len(results[0]))
        if(len(results[0])>=1):
            counter+=1
        else:
            counter=0
            if(comment==0):
                ser.write(b'0')
        if(counter>5 and counter<10): # 5 frame saw
            if(comment==0):
                ser.write(b'1') # half alarm
        elif(counter>10): # full alarm
            if(comment==0):
                ser.write(b'2')
        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()