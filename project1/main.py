from flask import Flask,render_template,request,session,redirect,url_for
#importing  the database library
from databaselib import getdbcur

app = Flask(__name__)
# adding session key
app.secret_key = "testing4ecommerce"
@app.route('/')
def home():
    return render_template('hometemplate.html')

@app.route('/forget',methods = ['GET','POST'])
def forget():
    if request.method == 'POST':
        em = request.form['email']
        cur = getdbcur()
        sql = "select * from user where email = '"+em+"' "
        cur.execute(sql)
        n = cur.rowcount
        if n == 1 :
            session['email'] = em
            return render_template('confirmpassword.html')
        else :
            return render_template('forget.html',lmsg = "Incorrect Email")
    else :
        return render_template('forget.html')


@app.route('/confirmpassword',methods = ['GET','POST'])
def confirmpassword():

    email = session['email']
    if request.method == 'POST':
        newpass = request.form['newpass']
        cpass=request.form['cpass']
        if newpass==cpass:
           sql="update user set password='"+newpass+"' where email='"+email+"' "
           cur=getdbcur()
           cur.execute(sql)
           n = cur.rowcount
           return render_template('login.html')
        else:
           return render_template('changepassword.html',cmsg="Password donot mathch")
    else:
        render_template('changepassword.html',errormsg="You can't change password!")




@app.route('/verify',methods = ['GET','POST'])
def verify():
    if request.method == 'POST':
        #em = request.form['em']
        #cur =getdbcur()
        return "<h1 >curreent this functionality is not active</h1>"
    return render_template('verify.html')

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

# Category items section
@app.route('/watches')
def watches():

    item =['watches',{ 'src' : 'https://media.gettyimages.com/photos/closeup-of-wristwatch-on-table-picture-id1070075980?s=2048x2048', 'name' :  'Gen 5 Carlyle' , 'description' : '(Touchscreen Smartwatch with Speaker, GPS)', 'price' : '2999'},
    { 'src' : 'https://media.gettyimages.com/photos/watch-picture-id171585392?s=2048x2048', 'name' :  'Grant Chronograph' , 'description' : '(Analog Black Dial Mens Watch - FS4832)', 'price' : '2999'},
    { 'src' : 'https://media.gettyimages.com/photos/watch-picture-id171585391?s=2048x2048', 'name' :  'Analog Blue' , 'description' : '(Dial Mens Watch - FS4835)', 'price' : '2999'},
    { 'src' : 'https://media.gettyimages.com/photos/mens-stainless-steel-wristwatch-with-black-face-picture-id480226373?s=2048x2048', 'name' :  'Fastrack Black Magic' , 'description' : '(Analog Black Dial Mens Watch)', 'price' : '2999'},
    { 'src' : 'https://media.gettyimages.com/photos/watch-picture-id116471589?s=2048x2048', 'name' :  'Wizzy' , 'description' : '(Top brand women watch)', 'price' : '2999'}
    ]


    return render_template('category.html',item = item)

  #category section end
            
@app.route('/profile')
def profile():
   if 'email' in session :
       email = session['email']
       sql = "select * from user where email ='"+email+"' "
       cur = getdbcur()
       cur.execute(sql)
       data = cur.fetchall()
       return render_template("profile.html",data=data)
   else :
       return  render_template('login.html', lmsg = "You have to login first to view your profile.")


if __name__ == '__main__':
    app.run(debug = True)
