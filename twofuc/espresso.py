import os
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DecimalField, IntegerField, SelectField, MultipleFileField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Email
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename

from ioanalyzer import cifanalyze, pwinpgen

import time

import os
homedir = os.environ['HOME']


IMMSTOPDIR=homedir+"/IMMS"

if not os.path.exists(IMMSTOPDIR):
    os.makedirs(IMMSTOPDIR)


sessiontime="SESSION"+time.strftime("%d%b%Y")

SESSIONDIR = IMMSTOPDIR+"/"+sessiontime

if not os.path.exists(SESSIONDIR):
    os.makedirs(SESSIONDIR)



f=open(SESSIONDIR+"/nodata.txt", "w")
f.write("\n------------------------\n")
f.write("There is No data to show")
f.write("\n------------------------\n")
f.close()



#  data to tranfer between functions in dictionary format
passdata={
"ciffile" : [],
"cifpath" : [],
"workdir" : [SESSIONDIR],
"inpname" : [],
"cifelem" : [],
"cifposition": [],
"ciftypes"  : [],
"ceifcell" : [],
"pseudolist" : [],
"index"   : []  
}




csrf = CSRFProtect()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecretgf!'
app.config['MAX_CONTENT_LENGTH'] = 80 * 1024 * 1024  # 4MB max-limit.
csrf.init_app(app)


class FileUploadForm(FlaskForm):
    ciffile = FileField('ciffile', validators=[FileRequired(), FileAllowed(['cif', 'CIF', 'txt','text'], 'cif only!')], id ='contentcode')


class PseudoUploadForm(FlaskForm):
    pseudofiles = MultipleFileField('File(s) Upload')


##  espresso input form class
class inpform(FlaskForm):
    calculation = SelectField(u'Calculation', choices=['scf', 'relax', 'vc-relax'], id="combobox1")
    orthomethod = SelectField(u'orthomethod', choices=['davidson', 'cg'], id="combobox2")
    spin = SelectField(u'spin', choices=['1', '2', '4'], id="combobox3")
    prefix = StringField('prefix',  render_kw={"placeholder": "prefix value"})
    ecut = DecimalField('ecut',  render_kw={"placeholder": "ecut value"})
    ecutrho = DecimalField('ecutrho',  render_kw={"placeholder": "ecutrho value"})
    mixbeta = DecimalField('mixbeta',  render_kw={"placeholder": "Mixing Beta"})
    degauss = DecimalField('degauss',  render_kw={"placeholder": "deguass"})
    nstep   = IntegerField('nstep',  render_kw={"placeholder": "Max interations"})



@app.route('/')
def index():
    upload_form = FileUploadForm()
    input_form = inpform()
    pseudo_form = PseudoUploadForm()
    return render_template('qe.html', upload_form=upload_form, input_form=input_form, pseudo_form=pseudo_form)


@app.route('/cifupload', methods=['POST'])
def cifupload():
    message="Nofile"
    ciftext = "nodata.txt"
    upload_form = FileUploadForm()
    input_form = inpform()
    pseudo_form = PseudoUploadForm()
    if upload_form.validate_on_submit():
        filename = secure_filename(upload_form.ciffile.data.filename)
        message="you cif is   "+filename 
        upload_form.ciffile.data.save(SESSIONDIR+"/"+filename)
        backcol="#85F6BC"
        passdata["ciffile"].append(filename)
        cifpath=SESSIONDIR+"/"+filename
        cifdict=cifanalyze(cifpath)
        cifelements=cifdict["elements"]
        atomtypes=list(set(cifelements))
        passdata["cifelem"].append(cifelements)
        passdata["ciftypes"].append(sorted(atomtypes))
        ciftext=cifpath[:-3]+"txt"
        passdata["workdir"].append(SESSIONDIR)
        passdata["cifpath"].append(cifpath)
    else:
        message = "There is a PROBLEM"
        backcol =  "#F9887C"
        ciftepseudo= SESSIONDIR+"/pseudoata.txt"

    datatxt=open(ciftext, "r")
    content=datatxt.read()
    datatxt.close()
    return render_template('qe.html', upload_form=upload_form, input_form=input_form, pseudo_form=pseudo_form, fname=message, backcol=backcol, content=content)



@app.route('/pseudoupload', methods=['POST'])
def pseudoupload():
    upload_form = FileUploadForm()
    input_form = inpform()
    pseudo_form = PseudoUploadForm()
    if pseudo_form.validate_on_submit():
        pseudo_filenames = []
        for file in pseudo_form.pseudofiles.data:
            file_filename = secure_filename(file.filename)
            file.save(os.path.join(passdata["workdir"][-1], file_filename))
            pseudo_filenames.append(file_filename)
        print(pseudo_filenames)
        pseudo_filenames=sorted(pseudo_filenames)
        passdata["pseudolist"].append(pseudo_filenames)

    else:
        print("There is a prob !!!!!!")
    return render_template('qe.html', upload_form=upload_form, input_form=input_form, 
        pseudo_form=pseudo_form, pseudo_filenames=pseudo_filenames)




@app.route('/inpvalues', methods=['POST'])
def inpvalues():
    upload_form = FileUploadForm()
    input_form = inpform()
    pseudo_form = PseudoUploadForm()
    if ( (len(passdata["pseudolist"][-1]) !=0 ) & (len(passdata["ciftypes"][-1]) !=  0) ):
        print ("OK")
    else:
        print("Something went wrong, TRY AGAIN")

    pseudodict=dict(zip(passdata["ciftypes"][-1],passdata["pseudolist"][-1]))
    if input_form.validate_on_submit():
        cifpath=passdata["cifpath"][-1]

        inp_data={'prefix':input_form.prefix.data, 'electron_maxstep':input_form.nstep.data,'outdir':passdata["workdir"][-1],
        'pseudo_dir': passdata["workdir"][-1], 'tstress':True, 'tprnfor':True,'calculation':input_form.calculation.data, 
        'ecutrho':input_form.ecutrho.data,'verbosity':'high',
             'ecutwfc':input_form.ecut.data, 'diagonalization': input_form.orthomethod.data, 'occupations':'smearing',
             'smearing':'mp', 'mixing_mode':'plain', 'mixing_beta':0.7,
             'degauss':0.001, 'nspin':1}
        pwinpgen(cifpath, pseudodict, inp_data)
   
    return render_template('qe.html', upload_form=upload_form, input_form=input_form, pseudo_form=pseudo_form)




if __name__ == "__main__":
    app.run(debug=True)