import uuid
import os
from flask import Flask,render_template,request,session,redirect,url_for,flash
#importing  the database library
from databaselib import getdbcur
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer,SignatureExpired

app = Flask(__name__)
# adding session key
app.secret_key = "testing4ecommerce"
#adding config for mail
secret_url = URLSafeTimedSerializer(app.secret_key)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'umesh.us.suman@gmail.com'
# app.config['MAIL_PASSWORD'] = 'Enter ur pass here'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/')
def home():
    return render_template('hometemplate.html')

@app.route('/changepassword',methods = ['GET','POST'])
def changepassword():
    if request.method == 'POST':
        if 'email' in session :
            email = session['email']
            oldpass  =  request.form['oldpass']
            newpass = request.form['newpass']
            sql="update users set password='"+newpass+"' where email='"+email+"' AND password='"+oldpass+"' "
            cur=getdbcur()
            cur.execute(sql)
            n = cur.rowcount
            if n==1:
                session.pop('email', None)
                return render_template('changepassword.html',cmsg="password changed successfully!")
            else:
                    return render_template('changepassword.html',incorroldpassmsg="Incorrect old password!")
        else:
            return render_template('changepassword.html',errormsg="You can not change password  ..Login first!")
    else :
        return render_template('changepassword.html')


@app.route('/forget',methods = ['GET','POST'])
def forget():
    if request.method == 'POST':
        em = request.form['email']
        cur = getdbcur()
        sql = "select * from users where email = '"+em+"' "
        cur.execute(sql)
        n = cur.rowcount
        if n == 1 :
            session['email'] = em
            return render_template('confirmpassword.html')
        else :
            return render_template('forget.html',lmsg = "Incorrect Email")
    else :
        return render_template('forget.html')

@app.route('/verify',methods = ['GET','POST'])
def verify():
    if request.method == 'POST':
        try:
            em = request.form['email']
            cd = request.form['code']
            sql = "update users set email_confirm=1 where email = '"+em+"' AND verifcode = '"+cd+"'  "
            cur = getdbcur()
            cur.execute(sql)
            return render_template('verify.html',successmsg = "email confirmation successful")
        except:
            return render_template('verify.html',errormsg = "Email or code is incorrect")
    else:
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


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':

        try:
            nm = request.form['name']
            em = request.form['email']
            ph = request.form['mobileno']
            ps = request.form['password']
            code = uuid.uuid1()
            uc = code.node
            cmsg = Message('verification code', sender = 'umesh.us.suman@gmail.com', recipients = ['{}'.format(em)])
            cmsg.body = "Your verification code is: {}".format(uc)
            mail.send(cmsg)
            cur = getdbcur()
            sql = "insert into users(email,name,mobileno,password,verifcode) values(%s,%s,%s,%s,%s)"
            cur.execute(sql,(em,nm,ph,ps,uc))
            rsmsg = "Registration Successful please confirm your email!"
            return render_template('register.html',rsmsg = rsmsg)
        except:
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
        sql = "select * from users where email = '"+em+"' and password = '"+ps+"' "
        cur.execute(sql)
        n = cur.rowcount
        if n == 1 :
            session['email'] = em
            return redirect(url_for('profile'))
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



# Category items section
@app.route('/womens_fashion')
def womens_fashion():
    sql = "select * from product where category='womens fashion' "
    cur = getdbcur()
    cur.execute(sql)
    data = cur.fetchall()
    return render_template("category.html",data=data , msg="womens fashion")


@app.route('/watches')
def watches():

    sql = "select * from product where category='watches' "
    cur = getdbcur()
    cur.execute(sql)
    data = cur.fetchall()
    return render_template("category.html",data=data , msg="watches")

@app.route('/mens_fashion')
def mens_fashion():
    sql = "select * from product where category='mens fashion' "
    cur = getdbcur()
    cur.execute(sql)
    data = cur.fetchall()
    return render_template("category.html",data=data , msg="mens fashion")

@app.route('/kids_fashion')
def kids_fashion():

    sql = "select * from product where category='kids' "
    cur = getdbcur()
    cur.execute(sql)
    data = cur.fetchall()
    return render_template("category.html",data=data , msg="kids")

@app.route('/food')
def food():
    sql = "select * from product where category='food and vegetables' "
    cur = getdbcur()
    cur.execute(sql)
    data = cur.fetchall()
    return render_template("category.html",data=data , msg="food and vegetables")


@app.route('/beauty')
def beauty():

    sql = "select * from product where category='skin care' "
    cur = getdbcur()
    cur.execute(sql)
    data = cur.fetchall()
    return render_template("category.html",data=data , msg="skin care")

@app.route('/bags')
def bags():

    sql = "select * from product where category='bags' "
    cur = getdbcur()
    cur.execute(sql)
    data = cur.fetchall()
    return render_template("category.html",data=data , msg="bags")

@app.route('/beds')
def beds():
    sql = "select * from product where category='beds' "
    cur = getdbcur()
    cur.execute(sql)
    data = cur.fetchall()
    return render_template("category.html",data=data , msg="beds")


@app.route('/table_chair')
def table_chair():
    sql = "select * from product where category='tables & chair' "
    cur = getdbcur()
    cur.execute(sql)
    data = cur.fetchall()
    return render_template("category.html",data=data , msg="tables & chair")
  #category section end


@app.route('/profile')
def profile():
   if 'email' in session :
       email = session['email']
       sql = "select * from users where email ='"+email+"' "
       cur = getdbcur()
       cur.execute(sql)
       data = cur.fetchall()
       return render_template("profile.html",data=data)
   else :
       flash("you must login first to view your profile")
       return  redirect(url_for('login'))


@app.route('/editprofile',methods=['GET','POST'])
def editprofile():
    if 'email' in session :
        email = session['email']
        if request.method == 'POST':
            nm = request.form['name']
            ph = request.form['number']
            sql="update users set name='"+nm+"' , mobileno= '"+ph+"' where email='"+email+"'"
            cur=getdbcur()
            cur.execute(sql)
            return redirect(url_for('profile'))

        else:
            return render_template('editprofile.html')
    else :
         render_template('editprofile.html',errormsg="You can't change password  ..Login first!")


app.config["IMAGE_UPLOADS"]='../project1/uploads'
@app.route('/upload',methods=['GET','POST'])
def upload():
    if 'email' in session :
        email = session['email']
        if request.method == 'POST':
              nm = request.form['name']
              ca = request.form['category']
              pr = request.form['price']
              ds = request.form['description']
              im =  request.files['file']
              im.save(os.path.join(app.config["IMAGE_UPLOADS"],im.filename))
              cur = getdbcur()
              sql = "insert into product(name,category,price,description,email,filename) values(%s,%s,%s,%s,%s,%s)"
              cur.execute(sql,(nm,ca,pr,ds,email,im.filename))
              n = cur.rowcounts
              if n == 1 :
                  msg = "Uploaded Successful!"
                  return render_template('upload.html',msg = msg)
              else :
                  msg = "Upload Failed!"
                  return render_template('upload.html',msg = msg)
        else :
            return render_template('upload.html')


    else :
             return render_template('upload.html',msg="You can't upload products  ..Login first!")


#cart functionality
@app.route('/addtocart',methods = ['GET','POST'])
def addtocart():
    if 'email' in session:
        if request.method == 'POST':
            email = session['email']
            pname = request.form['pname']
            pdescription = request.form['pdescription']
            pprice = request.form['pprice']
            pimg = request.form['pimg']
            cur = getdbcur()
            try:
                sql = "insert into cart values( '"+email+"','"+pname+"','"+pdescription+"','"+pprice+"','"+pimg+"' )"
                cur.execute(sql)
                return redirect(url_for('cart'))
            except:
                return render_template('category.html',addtocartmsg = "item is not added to cart")
        else:
            return redirect(url_for('cart'))
    else:
        flash('Login first to add an item in your cart')
        return redirect(url_for('login'))

@app.route('/removeitem',methods =['GET','POST'])

def removeitem():
    if 'email' in session:
        if request.method == 'POST':
            cur = getdbcur()
            email = session['email']
            pname =request.form['pname']
            try:
                sql = "delete from cart where email ='"+email+"' AND productName = '"+pname+"'  "
                cur.execute(sql)
                flash('item is removed from cart')
                return redirect(url_for('cart'))
            except:
                flash('There is some error while removing')
                return redirect(url_for('cart'))
        else:
            flash('Direct access to this page is not allowed.')
            return redirect(url_for('cart'))
    else:
        flash('Login first')
        return redirect(url_for('login'))


@app.route('/cart',methods = ['GET', 'POST'])
def cart():
    if 'email' in session :
        email = session['email']
        sql = "select * from cart where email ='"+email+"' "
        cur = getdbcur()
        cur.execute(sql)
        n = cur.rowcount
        if n >=1 :
            data = cur.fetchall()
            return render_template('cart.html',cartdata = data)
        else:
            return render_template('cart.html',cartemptymsg  = "Looks like you have no items in your shopping cart.")
    else :
        flash('login first to view cart')
        return  redirect(url_for('login'))


@app.route('/buy',methods = ['GET','POST'])
def buy():
    if 'email' in session:
        email = session['email']
        session['productName'] = request.form['pname']
        session['productPrice'] = request.form['pprice']
        if request.method =='POST':
            sql = "select name,mobileno,email,address,city,state,zipcode from users where email = '"+email+"'  "
            cur = getdbcur()
            cur.execute(sql)
            data = cur.fetchone()
            return render_template('buy.html',userinfo = data)
        else:
            return redirect(url_for('home'))
    else:
        flash('login first to buy the product.')
        return redirect(url_for('login'))

if  __name__ == '__main__':
    app.run(debug = True)
