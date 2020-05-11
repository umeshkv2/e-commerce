from flask import Flask, render_template, request,redirect, url_for
import pymysql
app = Flask(__name__)
@app.route('/', methods = ['POST', 'GET'])
def register():

  db = pymysql.connect("85.10.205.173","umeshkv2","umeshkv2","multikart" )
  c = db.cursor()

  try:
      if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        number = request.form['number']
        address = request.form['address']
        password = request.form['password']

        sql = "INSERT INTO user(name,email,number,address,password) VALUES (%s, %s, %s, %s, %s)"

        x = c.execute('SELECT * FROM user WHERE email = %s AND number = %s', (email, number))


        if int(x) > 0:
            msg="The email or mobile number is already taken, please choose another"
            return render_template('register.html', msg = msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
            return render_template('register.html', msg = msg)
        elif not re.match(r'[A-Za-z]+', name):
            msg = 'Name must contain only characters !'
            return render_template('register.html', msg = msg)
        elif not name or not email or not number or not address or not password:
            msg = 'Please fill out the form!'
            return render_template('register.html', msg = msg)

        else:
            c.execute(sql)
            db.commit()
            msg="Thanks for registering!"
            c.close()
            db.close()
            return redirect(url_for('home'))


  except Exception as e:
        return(str(e))
  return render_template("register.html", msg = msg)

if __name__ == '__main__':
    app.run(debug=True)
