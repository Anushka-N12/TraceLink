import io, os
import pandas as pd
from google.cloud import vision

def detect():
    with io.open(r"C:\Users\anush\Projects\TraceLink\media\frame.jpg", 'rb') as img:
        content = img.read()
    image = vision.Image(content=content)

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gc-api-tracelink-9d5886df7e14.json'
    client = vision.ImageAnnotatorClient()

    response1 = client.logo_detection(image=image)
    response2 = client.text_detection(image=image)
    l=[]
    for label in response1.logo_annotations:
        l.append(label.description)
    for label in response2.text_annotations:
        l.append(label.description)
    return(l)

if __name__ == '__main__':
    print(detect())