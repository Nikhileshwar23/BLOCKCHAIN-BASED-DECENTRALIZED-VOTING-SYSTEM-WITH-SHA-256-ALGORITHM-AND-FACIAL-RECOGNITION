import sys
import numpy as np
import face_recognition
import cv2
import mysql.connector
import time
import urllib

var = 0
p = ''

# Connect to the database
mydb = mysql.connector.connect(
    host="localhost", user="root", password="2312", database="voter_db")
mycursor = mydb.cursor()

# Retrieve user data from the database
mycursor.execute(
    "SELECT firstname, photos FROM user WHERE username = %s", (sys.argv[1],))
result = mycursor.fetchone()

if result:
    n, p = result  # Extract firstname and photos from the result
    print("Username:", sys.argv[1])
else:
    print("User not found in the database")
    sys.exit(1)

print(p)

# Load the user's image and encode the face
path = "user-photos\\" + sys.argv[1] + "\\" + p
sou_image = cv2.imread(path)
sou_image = cv2.cvtColor(sou_image, cv2.COLOR_BGR2RGB)
sou_face_locations = face_recognition.face_locations(sou_image)
sou_face_encodings = face_recognition.face_encodings(sou_image, sou_face_locations)

known_face_encodings = sou_face_encodings
known_face_names = [n]

name1 = ''

video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    #print("Face locations:", face_locations)
    #print("Face encodings:", face_encodings)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        name1 = name
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            name1 = name

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, name, (left+6, bottom-6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Webcam_facerecognition', frame)

    key = cv2.waitKey(10)
    if key == ord('k'):
        if name1 == n and len(face_locations) != 0:
            print(name1)
            var = 1
            break
        else:
            print("No match found or no face detected.")
            time.sleep(10)  # This might cause an issue if it's not what you intend to do
            break

    elif key == 27:  # 27 is the ASCII value for the Escape key
        break  # Exit the loop if the Escape key is pressed

video_capture.release()
cv2.destroyAllWindows()

if var == 1:
    print("match")
    with open("src\\main\\resources\\templates/out.txt", "w") as text_file:
        text_file.write(sys.argv[1] + " 1")
else:
    print("not match")
    with open("src\\main\\resources\\templates/out.txt", "w") as text_file:
        text_file.write(sys.argv[1] + " 0")


