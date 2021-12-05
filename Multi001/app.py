
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, jsonify
#from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators ,DecimalField, IntegerField, SelectField, MultipleFileField, SubmitField
from passlib.hash import sha256_crypt
from functools import wraps

import json

import numpy as np

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Email
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename

from ioanalyzer import cifanalyze, pwinpgen

import time

import os





##########################   GENERAL SETTING
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
##################################################################














app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 80 * 1024 * 1024  # 4MB max-limit.
# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)
csrf.init_app(app)





###################   CLASSES

class FileUploadForm(FlaskForm):
    ciffile = FileField('ciffile', validators=[FileRequired(), FileAllowed(['cif', 'CIF', 'txt','text'], 'cif only!')], id ='contentcode')


class PseudoUploadForm(FlaskForm):
    pseudofiles = MultipleFileField('File(s) Upload')


##  espresso input form class
class inpform(FlaskForm):
    calculation = SelectField(u'Calculation', choices=['scf', 'relax', 'vc-relax'], id="combobox1")
    orthomethod = SelectField(u'orthomethod', choices=['david', 'cg'], id="combobox2")
    spin = SelectField(u'spin', choices=['1', '2', '4'], id="combobox3")
    prefix = StringField('prefix',  render_kw={"placeholder": "prefix value"})
    ecut = DecimalField('ecut',  render_kw={"placeholder": "ecut value"})
    ecutrho = DecimalField('ecutrho',  render_kw={"placeholder": "ecutrho value"})
    mixbeta = DecimalField('mixbeta',  render_kw={"placeholder": "Mixing Beta"})
    degauss = DecimalField('degauss',  render_kw={"placeholder": "deguass"})
    nstep   = IntegerField('nstep',  render_kw={"placeholder": "Max interations"})

class gbform(FlaskForm):
    ciffile = FileField('ciffile', validators=[FileRequired(), FileAllowed(['cif', 'CIF', 'txt','text'], 'cif only!')], id ='contentcode')
    submitb=SubmitField('showplane')
    
##################################################################################################



#Articles = Articles()

# Index
@app.route('/')
def index():
    return render_template('home.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')


# Articles
@app.route('/articles')
@csrf.exempt
def articles():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    if result > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)
    # Close connection
    cur.close()


#Single Article
@app.route('/article/<string:id>/')
@csrf.exempt
def article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    article = cur.fetchone()

    return render_template('article.html', article=article)


#========================================================  SHOW CIF FILES  ============================================
# cif collection
@app.route('/database')
@csrf.exempt
def cifdata():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get ciftable
    result = cur.execute("SELECT * FROM ciftable")

    cifdata = cur.fetchall()

    if result > 0:
        print("cif data found")
        return render_template('dbpage.html', cifdata=cifdata)
    else:
        print("cif data NOT found")
        msg = 'No cif file Found'
        return render_template('dbpage.html', msg=msg)
    # Close connection
    cur.close()


#Single cif file
@app.route('/singlecif/<string:id>/')
@csrf.exempt
def onecif(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article
    result = cur.execute("SELECT * FROM ciftable WHERE id = %s", [id])

    singlecif = cur.fetchone()

    test = np.random.rand(5,3)  
    templist = test.tolist()
    tempjson = json.dumps(templist)

    return render_template('singlecif.html', singlecif=singlecif, jsondata=tempjson)



    ########################################################################################################








# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
@csrf.exempt
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
@csrf.exempt
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))



########### Dashboard
@app.route('/dashboard')
@csrf.exempt
@is_logged_in
def dashboard():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    #result = cur.execute("SELECT * FROM articles")
    # Show articles only from the user logged in 
    result = cur.execute("SELECT * FROM articles WHERE author = %s", [session['username']])

    articles = cur.fetchall()


    cifresult = cur.execute("SELECT * FROM ciftable WHERE author = %s", [session['username']])
    ciftable = cur.fetchall()


    if result > 0:
        return render_template('dashboard.html', articles=articles, ciftable=ciftable)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html', msg=msg, ciftable=ciftable)
    # Close connection
    cur.close()



######################################  add cif file

@app.route('/dashboard/addcif', methods=['POST'])
@csrf.exempt
@is_logged_in
def addcif():

    mycif= request.files['myciffile']
    mycifname = secure_filename(mycif.filename)

    cifbase=mycifname[:-3]

    if len(cifbase) > 11:
        mycifname=cifbase[:10]+".cif"


    ciffullpath=os.path.join(SESSIONDIR, mycifname)
    #  upload in server
    mycif.save(ciffullpath)
    print("file saved in    "+SESSIONDIR)

    cifdata = cifanalyze(ciffullpath)
    print(cifdata)

    if request.method =='POST':
        symbol = cifdata['symbol']
        spg = cifdata['spgroup']
        cifname = mycifname


        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("INSERT INTO ciftable(cifname, symbol, spg, author) VALUES(%s, %s, %s, %s)",(cifname, symbol, spg, session['username']))

        # Commit to DB
        mysql.connection.commit()


        #Close connection
        cur.close()        

        print("added to db")

        flash('cif added', 'success')
        msg ="OK"
        return redirect(url_for('dashboard'))
    return render_template('dashbord.html')






# Article Form Class
class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])

# Add Article
@app.route('/add_article', methods=['GET', 'POST'])
@csrf.exempt
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)",(title, body, session['username']))

        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('Article Created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)




# Edit Article
@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
@csrf.exempt


def edit_article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article by id
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    article = cur.fetchone()
    cur.close()
    # Get form
    form = ArticleForm(request.form)

    # Populate article form fields
    form.title.data = article['title']
    form.body.data = article['body']


    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        # Create Cursor
        cur = mysql.connection.cursor()
        app.logger.info(title)
        # Execute
        cur.execute ("UPDATE articles SET title=%s, body=%s WHERE id=%s",(title, body, id))
        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('Article Updated', 'success')

        return redirect(url_for('dashboard'))
    return render_template('edit_article.html', form=form)

# Delete Article
@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
@csrf.exempt

def delete_article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Execute
    cur.execute("DELETE FROM articles WHERE id = %s", [id])

    # Commit to DB
    mysql.connection.commit()

    #Close connection
    cur.close()

    flash('Article Deleted', 'success')

    return redirect(url_for('dashboard'))










# calc
@app.route('/calculator')
def calculator():
    return render_template('calculators.html')



############# !!! ============================================================  ROUTE FOR ESPRESSO
###################################
###########################################
################################################






@app.route('/qepage')
def qepage():
    upload_form = FileUploadForm()
    input_form = inpform()
    pseudo_form = PseudoUploadForm()
    return render_template('qe.html', upload_form=upload_form, input_form=input_form, pseudo_form=pseudo_form)


@app.route('/qepage/cifupload', methods=['POST'])
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
    return render_template('qe.html', upload_form=upload_form, input_form=input_form, pseudo_form=pseudo_form, 
        fname=message, backcol=backcol, content=content)



@app.route('/qepage/pseudoupload', methods=['POST'])
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




@app.route('/qepage/inpvalues', methods=['POST'])
def inpvalues():
    buildmessage="nothing"
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
        'ecutrho':float(input_form.ecutrho.data),'verbosity':'high',
             'ecutwfc':float(input_form.ecut.data), 'diagonalization': input_form.orthomethod.data, 'occupations':'smearing',
             'smearing':'mp', 'mixing_mode':'plain', 'mixing_beta':float(input_form.mixbeta.data),
             'degauss':float(input_form.degauss.data), 'nspin':1}
        pwinpgen(cifpath, pseudodict, inp_data)
        buildmessage=cifpath[:-3]+" is generated successfully"
        pwiname = cifpath[:-3]+"pwi"
        pwoname = cifpath[:-3]+"pwo"
        if os.path.isfile(pwiname):
            print("File found")
            os.system("pw.x  <  "+pwiname+" > "+pwoname )
            submitmessage="Job is submitted"
        else:
            submitmessage="There is problem! please check your input file"


   
    return render_template('qe.html', upload_form=upload_form, input_form=input_form, pseudo_form=pseudo_form)




#####################------------------------------------  END OF QE

# calc
@app.route('/mdcalc')
def mdcalc():
    return render_template('mdcalc.html')







# calc
@app.route('/fgr')
def fgr():
    return render_template('fgr.html')


@app.route('/gbcalc', methods=['GET', 'POST'])
@csrf.exempt
def gbcalc():
    if request.method == "POST":
        print("POST method")
        if request.form["action"] == "showplane":
            #filename = secure_filename(form.ciffile.data.filename)
            #message="you cif is   "+filename 
            #form.ciffile.data.save(SESSIONDIR+"/"+filename)
            print("showpage")
        elif request.form["action"] == "make_gb":
            #filename = secure_filename(form.ciffile.data.filename)
            #message="you cif is   "+filename 
            #form.ciffile.data.save(SESSIONDIR+"/"+filename)
            print("    Make GB IS active")
        else:
            print("nothinf")
    return render_template('gbcalc.html')

        

























#database
@app.route('/database')
def database():
    return render_template('dbpage.html')

@app.route('/dftcalc')
def dftcalc():
    return render_template('dftcalc.html')


if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
