from flask import Flask,render_template,request,session,redirect,url_for
#importing  the database library
from databaselib import getdbcur

app = Flask(__name__)
# adding session key
app.secret_key = "testing4ecommerce"
@app.route('/')
def home():
    return render_template('hometemplate.html')
@app.route('/search',methods = ['GET','POST'])
def search():
    if request.method == 'POST':
        items = request.form['searchbar']
        cur = getdbcur()
        sql = "select *  from product where product_name like %'"+items+"' OR '"+items+"'%  OR %'"+items+"'% "
        cur.execute(sql)
        n = cur.rowcount
        if n >= 1:
            data = cur.fetchall()
            return render_template('searchitems.html', searchdata = data)
        else :
            return render_template('seachitems.html',searchmsg = "There is no item is available that you search,try different name.")
    else :
        return redirect(url_for('home'))


@app.route('/cart',methods = ['GET', 'POST'])
def cart():
    if 'email' in session :
        email = session['email']
        sql = "select * from cart where email ='"+email+"' "
        cur = getdbcur()
        cur.execute(sql)
        n = cur.rowcount()
        if n >=1 :
            data = cur.fetchall()
            return render_template('cart.html',cartdata = data)
        else:
            return render_template('cart.html',cartemptymsg  = "Your cart is empty")
    else :
        return  render_template('cart.html', loginmsg = "You have to login first to view your cart.")

@app.route('/contact')
def contact():
    return render_template('contact.html')

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
        sql = "select * from user where email = '"+em+"' and password = '"+ps+"' "
        cur.execute(sql)
        n = cur.rowcount
        if n == 1 :
            session['email'] = em
            return redirect(url_for('home'))
        else :
            return render_template('login.html',lmsg = "Incorrect Email or password!")
    else :
        return render_template('login.html')

@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email',None)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/changepassword',methods = ['GET','POST'])
def changepassword():
    if 'email' in session :
        email = session['email']
        if request.method == 'POST':
            oldpass  =  request.form['oldpass']
            newpass = request.form['newpass']
            sql="update user set password='"+newpass+"' where email='"+email+"' AND password='"+oldpass+"' "
            cur=getdbcur()
            cur.execute(sql)
            n = cur.rowcount
            if n==1:
                session.pop('email', None)
                return render_template('changepassword.html',cmsg="Password changed Successfully")
            else:
                    return render_template('changepassword.html',cmsg="Incorrect old password!")
        else:
            return render_template('changepassword.html')
    else :
         render_template('changepassword.html',errormsg="you can't change password  ..Login first!")
if __name__ == '__main__':
    app.run(debug = True)
