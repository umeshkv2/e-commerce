from flask import Flask,render_template,request,session,redirect,url_for
#importing  the database library
from databaselib import getdbcur

app = Flask(__name__)
# adding session key
app.secret_key = "testing4ecommerce"
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        nm = request.form['name']
        em = request.form['email']
        ph = request.form['mobileno']
        ps = request.form['password']
        cur = getdbcur()
        sql = "insert into user values('"+nm+"','"+em+"','"+ph+"','"+ps+"')"
        cur.execute(sql)
        n = cur.rowcount
        if n == 1 :
            msg = "Registration Successful!"
            return render_template('register.html',rmsg = msg)
        else :
            msg = "Registration Failed!"
            return render_template('register.html',rmsg = msg)
    else :
        return render_template('register.html')

@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        em = request.form['email']
        ps = request.form['password']
        cur = getdbcur()
        sql = "select email from user where email = '"+em+"' and password = '"+ps+"' "
        cur.execute(sql)
        n = cur.rowcount
        if n == 1 :
            session['email'] = em
            return redirect(url_for(''))
        else :
            return render_template('login.html',lmsg = "Incorrect Email or password!")
    else :
        return render_template('login.html')
if __name__ == '__main__':
    app.run(debug = True)
