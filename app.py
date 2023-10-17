from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import os
import random
import string
from flask_mail import Mail, Message
  
app = Flask(__name__)
app.secret_key=os.urandom(24)

conn=mysql.connector.connect(host="127.0.0.1",user="root",password="",database="user-system")
cursor=conn.cursor()

app.config['MAIL_SERVER'] = 'smtp-relay.brevo.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = '2022pietcrrituraj047@poornima.org'
app.config['MAIL_PASSWORD'] = 'xTc9OWKfz5rdgJZY'

mail = Mail(app)

def send_email(recipient, subject, body):
    msg = Message(subject, sender='2022pietcrrituraj047@poornima.org', recipients=[recipient])
    msg.body = body
    mail.send(msg)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main')
def  main():
    return render_template('main.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/reset')
def reset():
    return render_template('reset.html')

@app.route('/login2')
def login2():
    return render_template('login2.html')


@app.route('/home')
def home():
    if 'user_id' in session:
       return render_template('home.html')
    else:
        return redirect('/')
    
@app.route('/customerP')
def customerP():
    return render_template('customerP.html')


@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/login_validation',methods=["POST"])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')
    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))
    users=cursor.fetchall()
    if len(users)>0:
        session['user_id']=users[0][0]
        return render_template('search.html')
    else:
        return redirect('/login')
    
@app.route('/login_validation2',methods=["POST"])
def login_validation2():
    email=request.form.get('email')
    password=request.form.get('password')
    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))
    users=cursor.fetchall()
    if len(users)>0:
        session['user_id']=users[0][0]
        return render_template('customerP.html')
    else:
        return redirect('/login2')

@app.route('/add_user', methods=['POST'])
def add_user():
    name=request.form.get('uname')
    email=request.form.get('uemail')
    password =request.form.get('upassword')
    otp = ''.join(random.choices(string.digits, k=6))
    cursor.execute("""INSERT INTO `users` (`user_id`, `name`, `email`, `password`, `otp`) VALUES(NULL, '{}', '{}', '{}', '{}')""".format(name, email, password, otp))
    conn.commit()
    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
    subject = 'Registration OTP'
    message = f'Your OTP for registration is: {otp}'
    send_email(email, subject, message)

    return render_template('verify.html')

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    email = request.form.get('email')
    otp = request.form.get('otp')

    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `otp` LIKE '{}'""".format(email,otp))
    users = cursor.fetchone()

    if len(users) > 0:
        cursor.execute("""UPDATE `users` SET `verified` = 1 WHERE `email` LIKE '{}'""".format(email))
        conn.commit()
        return render_template('login.html')
    else:
        return render_template('verify.html')
    
@app.route('/verify_otp1', methods=['POST'])
def verify_otp1():
    email = request.form.get('email')
    otp = request.form.get('otp')

    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `otp` LIKE '{}'""".format(email,otp))
    users = cursor.fetchone()

    if len(users) > 0:
        cursor.execute("""UPDATE `users` SET `verified` = 1 WHERE `email` LIKE '{}'""".format(email))
        conn.commit()
        return render_template('login2.html')
    else:
        return render_template('verify1.html')
    
@app.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.form.get('email')
    otp = request.form.get('otp')
    new_password = request.form.get('new_password')

    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `otp` LIKE '{}'""".format(email, otp))
    users = cursor.fetchall()

    if len(users) > 0:
        cursor.execute("""UPDATE `users` SET `password` = '{}' WHERE `email` LIKE '{}'""".format(new_password, email))
        conn.commit()
        return render_template('login.html')
    else:
        return render_template('reset.html')

@app.route('/add_user2', methods=['POST'])
def add_user2():
    name=request.form.get('uname')
    email=request.form.get('uemail')
    password=request.form.get('upassword')
    otp = ''.join(random.choices(string.digits, k=6))
    cursor.execute("""INSERT INTO `users` (`user_id`, `name`, `email`, `password`, `otp`) VALUES(NULL, '{}', '{}', '{}', '{}')""".format(name, email, password, otp))
    conn.commit()
    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
    subject = 'Registration OTP'
    message = f'Your OTP for registration is: {otp}'
    send_email(email, subject, message)

    return render_template('verify1.html')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')


@app.route('/worker_user', methods=['POST'])
def worker_user():
    FullName=request.form.get('FullName')
    DateOfBirth=request.form.get('DateOfBirth')
    Gender=request.form.get('Gender')
    Email=request.form.get('Email')
    ContactNumber=request.form.get('ContactNumber')
    Address=request.form.get('Address')
    Skills=request.form.get('Skills')
    cursor.execute("""INSERT INTO `workers` (`UserID`,`FullName`, `DateOfBirth`,`Gender`,`Email`,`ContactNumber`,`Address`,`Skills`) VALUES(NULL,'{}','{}','{}','{}','{}','{}','{}')""".format(FullName,DateOfBirth,Gender,Email,ContactNumber,Address,Skills))
    conn.commit()
    cursor.execute("""SELECT * FROM `workers` WHERE `ContactNumber` LIKE '{}'""".format(ContactNumber))
    return render_template('main.html')

@app.route('/searching', methods=['GET','POST'])
def searching():
    if request.method== 'POST':
        search_term=request.form['search_term']
        cursor.execute("""SELECT * FROM `workers` WHERE `skills` LIKE '{}'""".format(search_term))
        results=cursor.fetchall()
        return render_template('searchP.html',results=results)
    return render_template('search.html')

if __name__ == "__main__":
    app.run(port=5001,debug=True)