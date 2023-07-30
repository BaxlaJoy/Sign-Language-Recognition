import numpy as np
from keras.models import model_from_json
import operator
import cv2
import sys, os

json_file = open("model-bw.json", "r")
model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(model_json)

loaded_model.load_weights("model-bw.h5")
print("Loaded model from disk")

cap = cv2.VideoCapture(0)

categories = {0: 'ZERO', 1: 'ONE', 2: 'TWO', 3: 'THREE', 4: 'FOUR', 5: 'FIVE', 6: 'A', 7: 'B', 8: 'C', 9: 'D', 10: 'E', 11: 'HELLO', 12: 'YES', 13: 'THANK YOU', 14: 'WELCOME', 15: 'NO'}

while True:
    _, frame = cap.read()
    
    frame = cv2.flip(frame, 1)
    
    x1 = int(0.5*frame.shape[1])
    y1 = 10
    x2 = frame.shape[1]-10
    y2 = int(0.5*frame.shape[1])
   
    cv2.rectangle(frame, (x1-1, y1-1), (x2+1, y2+1), (255,0,0) ,1)
    
    roi = frame[y1:y2, x1:x2]
    
    roi = cv2.resize(roi, (64, 64)) 
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, train_image = cv2.threshold(roi, 120, 255, cv2.THRESH_BINARY)
    cv2.imshow("train", train_image)
  
    result = loaded_model.predict(train_image.reshape(1, 64, 64, 1))
    prediction = {'ZERO': result[0][0], 
                  'ONE': result[0][1], 
                  'TWO': result[0][2],
                  'THREE': result[0][3],
                  'FOUR': result[0][4],
                  'FIVE': result[0][5],
                  'A': result[0][6], 
                  'B': result[0][7],
                  'C': result[0][8],
                  'D': result[0][9],
                  'E': result[0][10],
                  'HELLO': result[0][11], 
                  'YES': result[0][12],
                  'THANK YOU': result[0][13],
                  'WELCOME': result[0][14],
                  'NO': result[0][15]}
    
    prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
    
    cv2.putText(frame, prediction[0][0], (10, 120), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,255), 1)    
    cv2.imshow("Frame", frame)
    
    interrupt = cv2.waitKey(10)
    if interrupt & 0xFF == 27: 
        break
        
 
cap.release()
cv2.destroyAllWindows()
