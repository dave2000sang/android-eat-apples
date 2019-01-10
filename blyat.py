import cv2
import sys
import collections


def rescale_frame(frame, factor=1.75):
    width = int(frame.shape[1] * factor)
    height = int(frame.shape[0] * factor)
    return cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)


# Get user supplied values
# imagePath = sys.argv[1]
# cascPath = "haarcascade_frontalface_default.xml"
cascPath = "fml.xml"

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

# Initiate video capturing
videoCapture = cv2.VideoCapture(0)
videoCapture.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
videoCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

# Declare center-position queue
cpQueue = collections.deque()

# Record last face position
lastFace = (800 / 2, 600 / 2, 30, 30)
lastVelocity = 0


def process_frame():
    global lastFace
    global lastVelocity

    # Read the frame:
    ret, frame = videoCapture.read()

    frame = cv2.flip(frame, 1)

    # frame = rescale_frame(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    # Detect faces in frame
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=6,
        minSize=(30, 30)
        # flags = cv2.CV_HAAR_SCALE_IMAGE
    )

    # Show faces recognized on picture
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Update position queue
    if len(faces):
        lastFace = faces[0]
    else:
        faces = []
        faces.append(lastFace)

    cpQueue.append((faces[0][0] + faces[0][2] / 2, faces[0][1] + faces[0][3] / 2))

    if len(cpQueue) > 20:
        cpQueue.popleft()
    cnt = 0
    for (x, y) in cpQueue:
        cv2.circle(frame, (int(x), int(y)), 2, (0, 0, cnt), 5)
        cnt += 10

    # write frame to image
    global face_img
    face_img = cv2.resize(frame, None, fx=0.25, fy=0.25)

    # calculate velocity
    if len(cpQueue) > 1:
        lastVelocity = (cpQueue[len(cpQueue) - 1][0] - cpQueue[len(cpQueue) - 2][0])

    return faces, lastVelocity

def destroy():
    videoCapture.release()
    cv2.destroyAllWindows()
