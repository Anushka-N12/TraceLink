#Import neccessary libraries
from flask import Flask, render_template, request, redirect, make_response, Response, send_file  #Main backend framework
import subprocess                      # To run scripts
import deploy                          # Script that runs the smart contract and has functions to interact with it
import time                            # To take timestamps when changes are made
from datetime import datetime          # To convert timestamps to readable format
import json, os                        # Reading & writing data of JSON format, accessing environment variables
from dotenv import load_dotenv         # Access to environment variables
import cam, logo_d                     # Script that GETs data from camera, logo detector
import database, qr                    # SQL database access, QR code zip file generator
import requests                        # To send GET request to ESP32
from urllib.request import urlopen     # For getting current location
import smtplib                         # To send emails aka alerts

subprocess.run(["python", "deploy.py"])
# subprocess.run(["python", "cam.py"])

load_dotenv('.env')

def format_data(num):
    pid, pnum = num.split('x')
    pdata = deploy.showDetails(int(pid), int(pnum))
    if pdata != 0:
        id = 'Product Id: ' + str(pdata[0]) + '\n'
        name = 'Product Name: ' + str(pdata[1]) + '\n'
        brand = 'Brand: ' + str(deploy.showC((pdata[2], pdata[2]))[0]) + '\n'
        desc = 'Description: ' + str(pdata[3] + '\n')
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
        data = id + name + brand + desc + quant + piece + clicks + entries
        data = data.split('\n')
        return(data)
    else:
        return 'Product not found'

def sendemail(message, emailid):
    s = smtplib.SMTP('smtp.gmail.com', 587)           # Starting session
    s.starttls()                                      # Starting TLS for security
    s.login(os.getenv('gmail'), os.getenv('gpw'))      # Authentication
    ''' Currently I am using my personal gmail id & password to send alerts,
        but this must be changed to a government address in implementation '''
    s.sendmail(os.getenv('gmail'), emailid, message)  # Sending
    s.quit()                                          # Terminating session

app = Flask(__name__)  #says this file is the app object
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
        url = os.getenv('esp_1')
        print('Taking pic')
        qr = cam.getimg(url)
        if len(qr) > 0:
            qr = qr[0]
            num = qr.split('/')[-1].split('x')
            pid, pnum = num[0], num[1]
            pdata = deploy.showDetails(int(pid), int(pnum))
            data = str(deploy.showC((pdata[2], pdata[2]))[0])
            name = data.lower()
            print('QR company: ', name)
            print('Detecting pic')
            logo = logo_d.detect()
            print('Logo detection list: ', logo)
            for i in logo:
                if name in i.lower():
                    result = True
        print('Triggering esp')
        esp2 = os.getenv('esp_2')
        print(esp2)
        try:
            if result:
                print('Supposed to turn green')
                blah = esp2 + '/LED=OFF'
                print(blah)
                requests.get(blah)
            else:
                print('Supposed to turn red')
                message = "A suspicious product has been detected by TraceLink! \nHere are the product details: \n"
                message += str(pdata)
                #*checks piece 1
                sendemail(message, os.getenv('gmail'))
                blah = esp2 + '/LED=ON'
                print(blah)
                requests.get(blah)
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
            data = {'registered company id': rcid, 'employee id': eid, 'mail id': mailid}
            message = "A new company wants to join TraceLink! \nHere are the given details: \n"
            message += str(data)
            sendemail(message, os.getenv('gmail'))
            return render_template('response_register.html')
            #Teams should integrate company login portal here

prid = ''
prnum = ''
@app.route('/company', methods=['GET', 'POST'])
def company():
    global compid
    global e_id
    global prid
    global prnum
    if request.method == 'GET':
        return render_template('add.html')
    if request.method == 'POST':
        if len(compid) == 0:
            redirect('/login')
        pid = request.form['pidi']
        name = request.form['namei']
        # brand = request.form['brandi']
        desc = request.form['desc']
        quant = request.form['quanti']
        task = request.form['taski']
        fid = request.form['fidi']
        tid = request.form['tidi']
        # print('form data received')
        if len(pid) == 0 and len(name) != 0 and len(desc) != 0 and len(quant) != 0:
            #Add product
            # print('adding product')
            checkft = deploy.showC((int(fid), int(tid)))
            if len(checkft[0]) > 0 and len(checkft[1]) > 0 and len(e_id) > 0 and len(compid) > 0:
                response = urlopen('http://ipinfo.io/json')  #add user ip before json for deployment
                data = json.load(response)
                loc = data['ip'] + ' ' + data['loc'] + ' ' +  data['city'] + ' ' + data['country']
                e = True if compid == fid else False
                n = deploy.addP(int(compid), name, desc, int(quant), int(fid), int(tid), e_id, e, task, loc)
                d = {'product id': n, 'name': name, 'description': desc, 'quantitiy': quant, 'from id': fid, 'to id':tid, 
                     'employee id': e_id, 'task': task, 'loc': loc}
                message = "A new product has been created under your company at TraceLink! \nHere are the given details: \n"
                message += str(d)
                #*checks piece 1
                sendemail(message, database.getemail(deploy.showDetails(n,1)[2]))
                print(pid, quant)
                prid = int(n)
                prnum = int(quant)
                return render_template('response_padd.html', data=n)
            else: 
                return render_template('response_pfail.html')
        elif len(pid) != 0 and len(name) == 0 and len(desc) == 0 and len(quant) == 0:
            checkft = deploy.showC((int(fid), int(tid)))
            pdata = deploy.showDetails(int(pid), 1)
            print(len(checkft[0]), len(checkft[1]), pdata, len(e_id), len(compid))
            if len(checkft[0]) > 0 and len(checkft[1]) > 0 and pdata != 0 and len(e_id) > 0 and len(compid) > 0:
                response = urlopen('http://ipinfo.io/json')  #add user ip before json for deployment
                data = json.load(response)
                loc = data['ip'] + ' ' + data['loc'] + ' ' +  data['city'] + ' ' + data['country']
                e = True if compid == fid else False
                n = deploy.storePi(int(pid), int(fid), int(tid), e_id, e, task, loc)
                d = {'product id': pid, 'from id': fid, 'to id':tid, 'employee id': e_id, 'task': task, 'loc': loc}
                message = "A new log has been added to your product at TraceLink! \nHere are the given details: \n"
                message += str(d)
                #*checks piece 1
                sendemail(message, database.getemail(deploy.showDetails(n,1)[2]))
                return render_template('response_psc.html')
            else:
                return render_template('response_pfail.html')
        else:
            return render_template('response_pfail.html')
        
@app.route('/download', methods=['GET'])
def download():
    global prid
    global prnum
    zip = qr.makecodes('http://127.0.0.1:5000', prid, prnum)
    return send_file(zip)

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