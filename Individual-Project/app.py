from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase




app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

confing  = {
  "apiKey": "AIzaSyAgn_FSrfaoF1-5CcXgbCWAopJ5NaqNg20",
  "authDomain": "cspro-d2046.firebaseapp.com",
  "projectId": "cspro-d2046",
  "storageBucket": "cspro-d2046.appspot.com",
  "messagingSenderId": "647196300841",
  "appId": "1:647196300841:web:a033249a1ae8c24207ae38",
  "measurementId": "G-XHD9YC9RCW",
  "databaseURL":"https://cspro-d2046-default-rtdb.europe-west1.firebasedatabase.app/"
}
firebase = pyrebase.initialize_app(confing)
auth = firebase.auth()
db = firebase.database()
#Code goes below here
# db.child('comments').push("i love arsenal")

@app.route('/', methods=['GET', 'POST'])
def signin():
    # error = ""
    if request.method == 'GET':
       return render_template('signinpro.html')
    else :
       email1= request.form['email']
       password1=request.form['password']
       try:
           login_session['user'] = auth.sign_in_with_email_and_password(email1,password1)
           return redirect(url_for('home'))
       except:
            # error = "Authentication error"
           return render_template('signinpro.html')

@app.route('/signuppro', methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        user={"email" : request.form['email'], "fname": request.form['firstname'], "lname":request.form['lname']}
        try: 
            login_session['user'] = auth.create_user_with_email_and_password(user["email"],request.form['password'])
            uid= login_session['user']['localId']
            db.child("user").child(uid).set(user)
            return redirect(url_for('home'))
        except Exception as e:
            return f"{e}"
            error = "auth failed"
    return render_template("signuppro.html")
@app.route('/ars')
def ars():
    return render_template('ars.html')
@app.route('/city')
def city():
    return render_template('city.html')
@app.route('/home', methods = ['GET','POST'])
def home():
    if request.method == 'POST':
        try:
            db.child("comments").push(request.form['comment'])
            return render_template("home.html", comments=db.child('comments').get().val())
            
        except:
            print ("wrong")
    return render_template("home.html", comments=db.child('comments').get().val())
        # return render_template('home.html')
@app.route('/fcb')
def fcb():
    return render_template('fcb.html')
@app.route('/rm')
def rm ():
    return render_template('rm.html')
# @app.route('/signout')
# def signout():
#     login_session['user']= none
#     auth.create  = none
#     return redirect(url_for('signinpro'))
#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)