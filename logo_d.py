# Script to detect logos & text
# Importing required packages
import io, os
import pandas as pd
from google.cloud import vision

# Function used by app.py 
def detect():
    # Open image saved by cam.py from camera
    with io.open(r"C:\Users\anush\Projects\TraceLink\media\frame.jpg", 'rb') as img:
        content = img.read()
    image = vision.Image(content=content)

    # Below JSON file was downloaded from configured google cloud account
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gc-api-tracelink-9d5886df7e14.json'
    client = vision.ImageAnnotatorClient()

    # Getting results
    response1 = client.logo_detection(image=image)
    response2 = client.text_detection(image=image)
    l=[]
    for label in response1.logo_annotations:
        l.append(label.description)
    for label in response2.text_annotations:
        l.append(label.description)
    return(l)

# Test to execute only if this file is executed directly    
if __name__ == '__main__':
    print(detect())