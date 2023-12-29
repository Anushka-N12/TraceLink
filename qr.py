import os, qrcode, zipfile

def makecodes(url, id, q):
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
            
    # folder = os.path.join(r'C:\Users\anush\Projects\TraceLink', 'QR_codes')
    # for i, imgfile in enumerate(image_list):
    #     with open(os.path.join(folder, str(i)), 'wb+') as f:
    #         f.write(imgfile)
    # response = HttpResponse(content_type='application/zip')
    # s = StringIO.StringIO()

    # resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
    # resp['Content-Disposition'] = 'attachment; filename=gik.zip'
    
    #Delete imgs in dir

    # return resp
if __name__ == '__main__':
    print(makecodes('http://127.0.0.1:5000', 1, 2))