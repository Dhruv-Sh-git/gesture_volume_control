import cv2 as cv
import mediapipe as mp

# Initialize mediapipe pose class and drawing utilities
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

# Start video capture
cap = cv.VideoCapture(0)

while True:
    success, img = cap.read()
   ## if not success:
     ##  break  # Exit the loop if video capture fails

    # Convert the image from BGR to RGB
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    # Process the RGB image to detect pose landmarks
    results = pose.process(imgRGB)
    
    # If landmarks are detected, draw them on the original BGR image
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id,lm in enumerate(results.pose_landmarks.landmark):
            h,w,c=img.shape
            cx,cy=int(lm.x*w),int(lm.y*h)
            if id==21:
                cv.circle(img,(cx,cy),10,(0,0,255),cv.FILLED)
            if id==22:
                cv.circle(img,(cx,cy),10,(0,0,255),cv.FILLED)
    
    # Display the processed video frame
    cv.imshow("Capture", img)

    # Break the loop if the 'q' key is pressed
    if cv.waitKey(1) & 0xFF == ord('d'):
        break

# Release the video capture and close all OpenCV windows
cap.release()
cv.destroyAllWindows()
