import cv2

cap = cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

cap.set(3, 640)  # adjust width
cap.set(4, 480)  # adjust height

while True:
    success, img = cap.read()
    
    if not success:
        print("Failed to capture image")
        break
    
    cv2.imshow("Live Feed", img)  # Changed window name to "Live Feed"

    if cv2.waitKey(1) & 0xFF == ord('q'):  # quit when 'q' is pressed
        break

cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)
