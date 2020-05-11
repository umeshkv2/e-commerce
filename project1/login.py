from flask import Flask, render_template, request,redirect, url_for,session
import pymysql
app = Flask(__name__)
@app.route('/', methods = ['POST', 'GET'])
def login():

  db = pymysql.connect("85.10.205.173","umeshkv2","umeshkv2","multikart" )
  c = db.cursor()

  try:
      if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        c.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        account = c.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['name']
            msg= 'Logged in successfully!'
            c.close()
            db.close()
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect email/password!'
    except Exception as e:
          return(str(e))

    return render_template('login.html', msg=msg)
if __name__ == '__main__':
    app.run(debug=True)
