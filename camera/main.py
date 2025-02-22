import cv2

camera = cv2.VideoCapture(0)
print("Got Camera")

camera.set(3, 1280)
print("Set Width")
camera.set(4, 720)
print("Set Height")

while True:
    _, image = camera.read()

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cv2.imshow("Live Camera Input", image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

