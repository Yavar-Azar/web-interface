from flask import Flask, render_template, request, jsonify
from GBBUILD import  axisdata, gbbuilder
from werkzeug.utils import secure_filename


import os, sys

from pathlib import Path

# homedir = Path.home()+"/MYAPP2"

# try:
#   os.mkdir(homedir)
# except(FileNotFoundError):
#   pass


app = Flask(__name__)


@app.route('/gbbuild')
def index():
    return render_template('form.html')

@app.route('/gbbuild/findplane', methods=['POST'])
def process():

    rotaxis = request.form['rotaxis']
    maxsigma = request.form['maxsigma']

    rotaxlist=[int(char) for char in rotaxis]
    maxsigmaint=int(maxsigma)


    resdict=axisdata(rotaxlist, maxsigmaint)
    sigmalist=list(resdict.keys())

    tempdict={}

    for k in sigmalist:
        temp = resdict[k]['plane'][0]
        tempstring=[]
        for i in range(len(temp)):
            b=temp[i]
            c=[str(var) for var in b]
            tempstring.append(c)
        tempdict.update({str(k):tempstring})



##  TODO    !!!    we must convert the this dict to validate json--- two problem break every three line and change keys from number to character


    aba={"ab":[['1', '1', '-1'],['1', '1', '-1']], "ba":"four"}
    print("message")
    print(tempdict)





    if sigmalist:
        return jsonify(aba)

    return jsonify({'error' : 'Missing data!'})


@app.route('/gbbuild/sendfile', methods=['POST'])
def send1():
    fx = request.files['newfile']
    fx.save(os.path.join(app.root_path, 'uploaded_file', secure_filename(fx.filename)))
    fname = str(secure_filename(fx.filename))
    errors = {}
    success = False


    with open(os.path.join(app.root_path, 'uploaded_file', secure_filename(fx.filename)), 'r') as file:
        fx_content = file.read()
        success = True
    print(fx_content, type(fx_content).__name__)


    if success and errors:
        errors['message'] = 'File(s) Failed in uploading'
        resp = jsonify(errors)
        resp.status_code = 500
        return resp


    if success:
        resp = jsonify(resultsingle=fname)
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp


























@app.route('/gbbuild/makegb', methods=['POST'])
def sec_process():

    a = request.form['rotaxis']
    b = request.form['maxsigma']


    a=float(a)
    b=float(b)

    c=a*b**2+5
    if a and b:
        res = c

        return jsonify({'result' : res})

    return jsonify({'error' : 'Missing data!'})


if __name__ == '__main__':
    app.run(debug=True)