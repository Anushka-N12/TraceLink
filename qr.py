import os

def makecodes(url, id, q):
    l = []
    for i in range(1, q + 1):
        l.append(url + '/qr/' + f'{id}x'+ str(i))
    print(l)

    # folder = os.path.join(settings.BASE_DIR, "imgs")
    # if not os.path.exists(folder):
    #     os.mkdir(folder)
    # for i, imgfile in enumerate(image_list):
    #     with open(os.path.join(folder, str(i)), 'wb+') as f:
    #         f.write(imgfile)
    # response = HttpResponse(content_type='application/zip')
    # s = StringIO.StringIO()

    # zip_file = zipfile.ZipFile(s, "w")
    # folder_files = os.listdir(folder)
    # for filename in folder_files:
    #     file = os.path.join(folder, filename)
    #     zip_file.write(file)

    # zip_file.close()

    # resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
    # resp['Content-Disposition'] = 'attachment; filename=gik.zip'
    # return resp

makecodes('http://127.0.0.1:5000', 1, 30)