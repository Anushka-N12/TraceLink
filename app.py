from flask import Flask, render_template, request, redirect, make_response, Response
import subprocess
import deploy
from datetime import datetime
import json, os, serial
import cam, logo_d, database
import requests
import time
from dotenv import load_dotenv
from urllib.request import urlopen

subprocess.run(["python", "deploy.py"])
# subprocess.run(["python", "cam.py"])

load_dotenv('.env')

def format_data(num):
    pid, pnum = num.split('x')
    pdata = deploy.showDetails(int(pid), int(pnum))
    if pdata != 0:
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
            entries += f'\tDetails: {i[5]}\n'
            entries += f'\tLocation of entry: {i[6]}\n'
            entries += f'\tTime of entry: {datetime.fromtimestamp(i[7])}\n'
            if i[4]:
                enterer = fc
            else:
                enterer = tc
            entries += f'\tThe above information was entered by Employee Id {i[3]} from {enterer}\n -- '
            count += 1
        data = id + name + brand + quant + piece + clicks + entries
        data = data.split('\n')
        return(data)
    else:
        return 'Product not found'

app = Flask(__name__)  #says this file is the app obj
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        data = format_data(request.form['ProductId'])
        return render_template('home.html', data = data)

#To show page from scanned QR code
@app.route('/qr/<num>', methods=['GET'])
def show(num):
    return render_template('home.html', data = format_data(num))
    
@app.route('/hardware', methods=['GET'])
def result():
    t = time.time()
    # while time.time()-t < 30:
    if True:
        result = False
        #might have to move run here
        qr = cam.getimg(os.getenv('esp1'))
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
        esp2 = os.getenv('esp2')
        try:
            if result:
                requests.get(esp2 + '/LED=OFF')
            else:
                requests.get(esp2 + '/LED=ON')
        except:
            pass
        
    return 'working'

compid = ''
e_id = ''
@app.route('/login', methods=['GET', 'POST'])
def login():
    global compid
    global e_id
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
        if len(cid) != 0 and len(pw) != 0 and len(rcid) == 0 and len(mailid) == 0:
            if database.authenticate(cid, eid, pw):
                compid = cid
                e_id = eid
                # print('login details saved')
                return redirect('/company')
            else:
                return render_template('response_loginf.html')
        elif len(cid) == 0 and len(pw) == 0 and len(rcid) != 0 and len(mailid) != 0:
            pass #register
            #Teams must integrate company login portal here
            # and update the email db
        # d = {'cid': cid, 'eid': eid, 'pw': pw, 'mailid': mailid, 'rcid': rcid}
        # print(d)

@app.route('/company', methods=['GET', 'POST'])
def company():
    global compid
    global e_id
    if request.method == 'GET':
        return render_template('add.html')
    if request.method == 'POST':
        if len(compid) == 0:
            redirect('/login')
        pid = request.form['pidi']
        name = request.form['namei']
        brand = request.form['brandi']
        desc = request.form['desc']
        quant = request.form['quanti']
        task = request.form['taski']
        fid = request.form['fidi']
        tid = request.form['tidi']
        # print('form data received')
        if len(pid) == 0 and len(name) != 0 and len(brand) != 0 and len(desc) != 0 and len(quant) != 0:
            #Add product
            # print('adding product')
            checkft = deploy.showC((int(fid), int(tid)))
            if len(checkft[0]) > 0 and len(checkft[1]) > 0 and len(e_id) > 0 and len(compid) > 0:
                response = urlopen('http://ipinfo.io/json')  #add user ip before json for deployment
                data = json.load(response)
                loc = data['ip'] + ' ' + data['loc'] + ' ' +  data['city'] + ' ' + data['country']
                e = True if compid == fid else False
                n = deploy.addP(int(compid), name, brand, desc, int(quant), int(fid), int(tid), e_id, e, task, loc)
        # d = {'pid':pid, 'name':name, 'brand':brand, 'desc': desc, 'quant': quant, 'task': task, 'fid': fid, 'tid':tid}
        # print(d)
                return render_template('response_padd.html', data=n)
            else:
                return render_template('response_pfail.html')
        elif len(pid) != 0 and len(name) == 0 and len(brand) == 0 and len(desc) == 0 and len(quant) == 0:
            checkft = deploy.showC((int(fid), int(tid)))
            pdata = deploy.showDetails(int(pid), 1)
            print(len(checkft[0]), len(checkft[1]), pdata, len(e_id), len(compid))
            if len(checkft[0]) > 0 and len(checkft[1]) > 0 and pdata != 0 and len(e_id) > 0 and len(compid) > 0:
                response = urlopen('http://ipinfo.io/json')  #add user ip before json for deployment
                data = json.load(response)
                loc = data['ip'] + ' ' + data['loc'] + ' ' +  data['city'] + ' ' + data['country']
                e = True if compid == fid else False
                n = deploy.storePi(int(pid), int(fid), int(tid), e_id, e, task, loc)
                return render_template('response_psc.html')
            else:
                return render_template('response_pfail.html')
        else:
            return render_template('response_pfail.html')

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

if __name__ == '__main__':
    #DO not remove any Code below
    #port = int(sys.argv[1])
    app.run(debug=True) #, host="0.0.0.0", port=port
#now run in console to get localhost number