from flask import Flask,render_template,redirect,url_for,request,session
#importing  the database library
import databaselib
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')
if __name__ == '__main__':
    app.run(debug = True)
