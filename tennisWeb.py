import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/home')

def home():
    return render_template('index.html')

@app.route('/login')

def loginPage():
    return render_template('login.html')

@app.route('/signup')

def signupPage():
    return render_template('signup.html')

@app.route('/courts')

def courts():
    return render_template('courts.html')

@app.route('/courts/VTC')

def varsity():
    return render_template('VTC.html')


@app.route('/courts/CCRB')

def ccrb():
    return render_template('ccrb.html')

@app.route('/courts/baits')

def baits():
    return render_template('baits.html')

#@app.route('/match')

#def match():
    #return render_template('match.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
