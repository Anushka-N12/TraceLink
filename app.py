from flask import Flask, render_template, request, redirect, make_response, Response
import subprocess
import deploy
from datetime import datetime
import json, os, serial
import cam, logo_d
import requests
import time

subprocess.run(["python", "deploy.py"])
subprocess.run(["python", "cam.py"])

def format_data(num):
    pid, pnum = num.split('x')
    pdata = deploy.showDetails(int(pid), int(pnum))
    id = 'Product Id: ' + str(pdata[0]) + '\n'
    name = 'Product Name: ' + str(pdata[1]) + '\n'
    brand = 'Brand: ' + str(pdata[2]) + '\n'
    desc = 'Description: ' + str(pdata[3])
    quant = 'Quantity Ordered: ' + str(len(pdata[4])) + '\n'
    piece = 'Your piece is no. : ' + str(pnum) + '\n'
    clicks = 'No. of times this piece has been checked: ' + str(pdata[4][int(pnum)-1]) + '\n'
    sections = pdata[5]
    entries = ' \n'
    count = 1
    print(sections)
    for i in sections:
        print(i)
        entries += f'-- \n Entry {count} - \n'
        cs = deploy.showC((i[1], i[2]))
        fc, tc = cs[0], cs[1]
        entries += f'\tFrom: {fc}\n\tTo: {tc}\n'
        entries += f'\tDetails: {i[4]}\n'
        entries += f'\tLocation of entry: {i[5]}\n'
        entries += f'\tTime of entry: {datetime.fromtimestamp(i[6])}\n'
        entries += f'\tThe above information was entered by Employee Id {i[3]} from {fc}\n -- '
        count += 1
    data = id + name + brand + quant + piece + clicks + entries
    data = data.split('\n')
    return(data)

app = Flask(__name__)  #says this file is the app obj
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        data = format_data(request.form['ProductId'])
        return render_template('home.html', data = data)

@app.route('/qr/<num>', methods=['GET'])
def show(num):
    return render_template('home.html', data = format_data(num))

# @app.route('/hardware/<num>', methods=['GET'])
# def send(num):
#     if request.method == 'GET':
#         num = num.split('x')
#         pid, pnum = num[0], num[1]
#         data = deploy.showDetails(int(pid), int(pnum))
#         '''Format of data show below doesn't directly work with responses, so next few lines change it accordingly -
#         (1, 'Bag', 'Gucci', [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [(1, 1, 1, 'df ht', 'rbth5ytn',
#         'wrhetrytjh', 1702211264), (1, 1, 1, 'm00wirbjefn', 'trial 2', 'dubai', 1702211264)])'''
#         d, c = {}, 0
#         for i in data[4]:
#             d[c] = i
#             c += 1
#         formatted_data = {
#             'id': data[0],
#             'name': data[1],
#             'brand': data[2],
#             'clicks': data[3],
#             'entries': d
#         }
#         # Create a JSON response and set custom header
#         response = json.dumps([formatted_data])
#         response = Response(response, status=200, content_type='application/json')
#         response.headers['X-My-Header'] = 'foo'
#         return response, 200
    
@app.route('/hardware', methods=['GET'])
def result():
    t = time.time()
    # while time.time()-t < 30:
    if True:
        result = False
        qr = cam.getimg('http://192.168.0.107')
        if len(qr) > 0:
            qr = qr[0]
            num = qr.split('/')[-1].split('x')
            pid, pnum = num[0], num[1]
            data = deploy.showDetails(int(pid), int(pnum))
            name = data[2].lower()
            logo = logo_d.detect()
            for i in logo:
                if name in i.lower():
                    result = True
        esp2 = 'http://192.168.0.108'
        try:
            if result:
                requests.get(esp2 + '/LED=OFF')
            else:
                requests.get(esp2 + '/LED=ON')
        except:
            pass
        
    return 'working'




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        #*post request not reaching here
        #*make vars global
        cid = request.form['CompanyId']
        eid = request.form['EmployeeId']
        pw = request.form['pw']
        mailid = request.form['Wemail']
        rcid = request.form['rcid']
        d = {'cid': cid, 'eid': eid, 'pw': pw, 'mailid': mailid, 'rcid': rcid}
        print(d)
        return render_template('response.html')

@app.route('/company', methods=['GET', 'POST'])
def comp():
    if request.method == 'GET':
        return render_template('add.html')
    if request.method == 'POST':
        pid = request.form['pidi']
        name = request.form['namei']
        brand = request.form['brandi']
        desc = request.form['desc']
        quant = request.form['quanti']
        task = request.form['taski']
        fid = request.form['fidi']
        tid = request.form['tidi']
        d = {'pid':pid, 'name':name, 'brand':brand, 'desc': desc, 'quant': quant, 'task': task, 'fid': fid, 'tid':tid}
        print(d)
        return render_template('response.html')

if __name__ == '__main__':
    #DO not remove any Code below
    #port = int(sys.argv[1])
    app.run(debug=True) #, host="0.0.0.0", port=port
#now run in console to get localhost number