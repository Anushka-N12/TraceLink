# Script to generate QR codes upon product creation
# Importing required packages
import os, qrcode, zipfile

# FUnction used by app.py
def makecodes(url, id, q):    # Takes url, product ID & quantity
    for i in range(1, q + 1):
        img = qrcode.make(url + '/qr/' + f'{id}x'+ str(i))
        img.save('QR_codes/'f'{id}x{str(i)}.png')
    fname = f'QR_codes/Product{id}.zip'
    with zipfile.ZipFile(fname,'w') as z:
        path = r'QR_codes/'
        for file in os.listdir(path):
            if file.endswith('.png'):
                filepath = os.path.join(path, file)
                z.write(filepath)
                os.remove(filepath)
    return fname

# Test to execute only if this file is executed directly    
if __name__ == '__main__':
    print(makecodes('http://127.0.0.1:5000', 3, 21))