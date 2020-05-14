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
@app.route('/womens_fashion')
def womens_fashion():
    item = ['womens fashion',{'src':'https://cdn.pixabay.com/photo/2017/08/01/11/48/blue-2564660__340.jpg', 'name':'denim jacket', 'description':'(denim jacket for girls)', 'price':'3000'},
    {'src':'https://cdn.pixabay.com/photo/2017/07/31/11/32/people-2557472__340.jpg', 'name':'leather jacket', 'description':'(leather jacket for girls)', 'price':'3000'},
    {'src':'https://images.unsplash.com/photo-1565127453543-ad97bbbba30d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60', 'name':'jeans', 'description':'(jeans for woman)', 'price':'1500'},
    {'src':'https://cdn.pixabay.com/photo/2019/06/06/09/47/girl-4255600__340.jpg', 'name':'t-shirt', 'description':'(t-shirts for girls)', 'price':'500'},
    {'src':'https://cdn.pixabay.com/photo/2016/04/12/10/40/portrait-1324074__340.jpg', 'name':'tops', 'description':'(tops for girls)', 'price':'700'},
    {'src':'https://cdn.pixabay.com/photo/2017/07/25/14/50/shoe-2538424_960_720.jpg', 'name':'footwear', 'description':'footwear for girls', 'price':'1200'},
    ]
    return render_template('category.html', item = item)


@app.route('/watches')
def watches():

    item =['watches',{ 'src' : 'https://media.gettyimages.com/photos/closeup-of-wristwatch-on-table-picture-id1070075980?s=2048x2048', 'name' :  'Gen 5 Carlyle' , 'description' : '(Touchscreen Smartwatch with Speaker, GPS)', 'price' : '2999'},
    { 'src' : 'https://media.gettyimages.com/photos/watch-picture-id171585392?s=2048x2048', 'name' :  'Grant Chronograph' , 'description' : '(Analog Black Dial Mens Watch - FS4832)', 'price' : '2999'},
    { 'src' : 'https://media.gettyimages.com/photos/watch-picture-id171585391?s=2048x2048', 'name' :  'Analog Blue' , 'description' : '(Dial Mens Watch - FS4835)', 'price' : '2999'},
    { 'src' : 'https://media.gettyimages.com/photos/mens-stainless-steel-wristwatch-with-black-face-picture-id480226373?s=2048x2048', 'name' :  'Fastrack Black Magic' , 'description' : '(Analog Black Dial Mens Watch)', 'price' : '2999'},
    { 'src' : 'https://media.gettyimages.com/photos/watch-picture-id116471589?s=2048x2048', 'name' :  'Wizzy' , 'description' : '(Top brand women watch)', 'price' : '2999'}
    ]

    return render_template('category.html',item = item)

@app.route('/mens_fashion')
def mens_fashion():
    item =['mens fashion',{ 'src' : 'https://images.unsplash.com/photo-1521341057461-6eb5f40b07ab?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80', 'name' :  'Mens suit' , 'description' : '(suit of multiple sizes)', 'price' : '2000'},
    { 'src' : 'https://images.unsplash.com/photo-1516257984-b1b4d707412e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80', 'name' :  'Denim jackets' , 'description' : '(Jacket for men multiple sizes) ', 'price' : '2500'},
    { 'src' : 'https://images.unsplash.com/photo-1542272604-787c3835535d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=626&q=80', 'name' :  'Jeans' , 'description' : '(Jeans in Multiple color for men)', 'price' : '1700'},
    { 'src' : 'https://images.unsplash.com/photo-1539185441755-769473a23570?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=751&q=80', 'name' :  'Sneakers' , 'description' : '(Sneakers of multiple color)', 'price' : '2500'},
    { 'src' : 'https://images.unsplash.com/photo-1481729379561-01e43a3e1ed4?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=836&q=80', 'name' :  'Boots' , 'description' : '(Boots for men)', 'price' : '2999'}
    ]
    return render_template('category.html',item = item)

@app.route('/kids_fashion')
def kids_fashion():

    item =['kids fashion',{ 'src' : 'https://images.unsplash.com/photo-1471286174890-9c112ffca5b4?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60', 'name' :  'Kids t-shirt' , 'description' : '(t-shirt of multiple size and color)', 'price' : '800'},
    { 'src' : 'https://images.unsplash.com/flagged/photo-1571530765629-4efdab448a6d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60', 'name' :  'frok' , 'description' : '(frok for girl child multiple designs and color) ', 'price' : '1200'},
    { 'src' : 'https://images.unsplash.com/photo-1553440070-7b7e896ed9e9?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60', 'name' :  'Casual shoes' , 'description' : '(Casual shoes for kids various sizes and color)', 'price' : '1700'},
    { 'src' : 'https://images.pexels.com/photos/981619/pexels-photo-981619.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940', 'name' :  'Pants' , 'description' : '(Pants for  kids)', 'price' : '1500'},
    { 'src' : 'https://images.unsplash.com/photo-1503858928522-1bdf02d8825c?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=333&q=80', 'name' :  'Hats' , 'description' : '(Hats for kids)', 'price' : '500'}
    ]

    return render_template('category.html',item = item)

@app.route('/clean_household')
def clean_household():

    item =['Cleaning & households',{ 'src' : 'https://images.unsplash.com/photo-1562886877-f12251816e01?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=889&q=80', 'name' :  'cleaning spray' , 'description' : '(Spray to clean mirror and Digital items)', 'price' : '200'},
    { 'src' : 'https://images.unsplash.com/photo-1583947582712-e880d61c71d0?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80', 'name' :  'Hand wash and senitizer' , 'description' : 'For germs protection ', 'price' : '300'},
    { 'src' : 'https://images.unsplash.com/photo-1523039031846-6b3f39302cb8?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=650&q=80', 'name' :  'utensil sets' , 'description' : '(Utensil sets for househols)', 'price' : '500'},
    { 'src' : 'https://images.unsplash.com/photo-1584634731339-252c581abfc5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=754&q=80', 'name' :  'face mask' , 'description' : '(protect you from bacteria)', 'price' : '200'},
    { 'src' : 'https://images.unsplash.com/photo-1584813470613-5b1c1cad3d69?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60', 'name' :  'floor cleaner' , 'description' : '(Kill germs and micro bacteria)', 'price' : '350'}
    ]

    return render_template('category.html',item = item)

@app.route('/food')
def food():

    item =['food products',{ 'src' : 'https://images.unsplash.com/photo-1557844352-761f2565b576?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60', 'name' :  'vegetables' , 'description' : '(Fresh and clean vegetables)', 'price' : '100'},
    { 'src' : 'https://cdn.pixabay.com/photo/2015/12/30/11/57/fruit-basket-1114060_960_720.jpg', 'name' :  'fruits' , 'description' : 'Fresh and clean fruits ', 'price' : '400'},
    { 'src' : 'https://cdn.pixabay.com/photo/2014/08/26/15/28/jam-428094_960_720.jpg', 'name' :  'fruit Jam' , 'description' : '(Make you food delicious )', 'price' : '300'},
    { 'src' : 'https://cdn.pixabay.com/photo/2015/06/26/15/31/oil-822618_960_720.jpg', 'name' :  'food oil' , 'description' : '(various types of food oil)', 'price' : '500'},
    { 'src' : 'https://image.shutterstock.com/image-photo/indian-namkeen-fried-600w-1249718911.jpg', 'name' :  'namkeen' , 'description' : '( varioust types of delicious namkeen)', 'price' : '350'}
    ]

    return render_template('category.html',item = item)

@app.route('/dairy_product')
def dairy_product():

    item =['dairy products',{ 'src' : 'https://images.unsplash.com/photo-1563636619-e9143da7973b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60', 'name' :  'milk' , 'description' : '(Fresh milk of cow and buffalo)', 'price' : '150'},
    { 'src' : 'https://images.unsplash.com/photo-1586152319516-d85a5c272a33?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80', 'name' :  'Curd' , 'description' : 'Fresh curd ', 'price' : '200'},
    { 'src' : 'https://images.unsplash.com/photo-1573812461383-e5f8b759d12e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60', 'name' :  'ghee' , 'description' : '(ghee for make food tasty  )', 'price' : '800'},
    { 'src' : 'https://images.unsplash.com/photo-1560801619-01d71da0f70c?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60', 'name' :  'desert' , 'description' : '(Pure milk Desert)', 'price' : '300'},
    { 'src' : 'https://cdn.pixabay.com/photo/2015/09/09/20/06/bowl-932980__340.jpg', 'name' :  'ice cream' , 'description' : '( ice cream of pure milk rich in taste)', 'price' : '150'}
    ]

    return render_template('category.html',item = item)

@app.route('/beauty')
def beauty():

    item =['beauty products',{ 'src' : 'https://images.unsplash.com/photo-1571646034647-52e6ea84b28c?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60', 'name' :  'lipsticks' , 'description' : '(make yourself look beautiful and pretty)', 'price' : '350'},
    { 'src' : 'https://cdn.pixabay.com/photo/2015/03/20/22/08/eyeshadow-682998__340.jpg', 'name' :  'facial makeup kit' , 'description' : '(facial kit) ', 'price' : '1400'},
    { 'src' : 'https://cdn.pixabay.com/photo/2017/09/06/20/16/eyeliner-2722845__340.jpg', 'name' :  'eye liner' , 'description' : '(vatious color eyeliner )', 'price' : '100'},
    { 'src' : 'https://cdn.pixabay.com/photo/2017/03/14/11/39/perfume-2142817__340.jpg', 'name' :  'perfume' , 'description' : '(fragrance smell )', 'price' : '500'},
    
    ]

    return render_template('category.html',item = item)


@app.route('/bags')
def bags():

    item =['bags',{ 'src' : 'https://images.unsplash.com/photo-1486037242572-f25faf7505e3?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60', 'name' :  'trekking bag' , 'description' : '(Bag for trekking and capacity storage)', 'price' : '2500' },
    { 'src' : 'https://images.unsplash.com/photo-1525708570275-58d59ffe4a93?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60', 'name' : 'handbag' , 'description' : '(hand bag for ladies) ', 'price' : '1200'},
    { 'src' : 'https://images.unsplash.com/photo-1472717400230-1c592a3179d5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60', 'name' : 'school bag' , 'description' : '(beautiful and tough bag)', 'price' : '1000'},
    { 'src' : 'https://cdn.pixabay.com/photo/2015/12/08/00/36/luggage-1081872__340.jpg', 'name' :  'lugage bags' , 'description' : '(lugage bags with high toughness and capacity)', 'price' : '3500'},
    { 'src' : 'https://cdn.pixabay.com/photo/2017/06/19/17/36/luggage-2420316_960_720.jpg', 'name' :  'suit case' , 'description' : '(suit case that you can take anywhere in hand)', 'price' : '2500'},
    
    ]
    
    return render_template('category.html',item = item)

@app.route('/beds')
def beds():

    item =['beds',
    { 'src' : 'https://images.unsplash.com/photo-1583221742001-9ad88bf233ff?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60', 'name' :  'wooden bed' , 'description' : '(high strength,flexible and long) ', 'price' : '12000'},
    { 'src' : 'https://images.unsplash.com/photo-1530334580314-1e7a340426a0?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60', 'name' :  'steel and iron bed' , 'description' : '(low cost high strength)', 'price' : '6000'},
    { 'src' : 'https://cdn.pixabay.com/photo/2017/07/10/10/06/mattress-2489615__340.jpg', 'name' :  'matress' , 'description' : '(matress for instant sleep and comfort)', 'price' : '3000'},
    { 'src' : 'https://cdn.pixabay.com/photo/2015/11/07/11/22/pillows-1031079__340.jpg', 'name' :  'pillow' , 'description' : '(pillow for comfort your head)', 'price' : '500'},
    
    ]
    
    return render_template('category.html',item = item)

@app.route('/sofa')
def sofa():

    item =['sofa',{ 'src' : 'https://cdn.pixabay.com/photo/2017/08/02/01/01/living-room-2569325__340.jpg', 'name' :  'simple sofa' , 'description' : '(simple sofa for hall and living room)', 'price' : '7000'},
    { 'src' : 'https://cdn.pixabay.com/photo/2014/09/15/21/46/couch-447484__340.jpg', 'name' :  'fancy sofa' , 'description' : '(couch) ', 'price' : '7000'},
    { 'src' : 'https://cdn.pixabay.com/photo/2013/09/26/11/59/leather-sofa-186636__340.jpg', 'name' :  'leather sofa' , 'description' : '(leather sofa or extrem comfort and look)', 'price' : '15000'},
 
    ]    
    return render_template('category.html',item = item)
@app.route('/table_chair')
def table_chair():
    item = ['tables & chair',{'src':'https://images.unsplash.com/photo-1564383424695-05a0668266ec?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60','name':'wooden table','description':'(tough and multi purpose table)','price':'5000' },
                {'src':'https://cdn.pixabay.com/photo/2018/04/10/01/34/chair-3306118__340.jpg','name':'steel and iron table','description':'(For outdoor uses)','price':'3000' },
                {'src':'https://cdn.pixabay.com/photo/2017/05/09/03/47/and-2297209__340.jpg','name':'wooden chairs','description':'(wooden chair for indoor ,outdoor use)','price':'2000' },
                {'src':'https://cdn.pixabay.com/photo/2016/11/22/23/05/chairs-1851078__340.jpg','name':'steel chair','description':'(for both indoor and outdoor uses)','price':'1200' },
                {'src':'https://cdn.pixabay.com/photo/2020/03/23/17/30/chair-4961552_960_720.jpg','name':'steel and iron','description':'(for indoor and public usage)','price':'10000' },
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
