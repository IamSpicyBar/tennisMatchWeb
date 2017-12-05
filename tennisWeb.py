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

@app.route('/courts/huron')

def huron():
    return render_template('huron_high.html')

@app.route('/courts/racquet')

def racquet():
    return render_template('racquet.html')

@app.route('/courts/ypsilanti')

def ypsilanti():
    return render_template('ypsilanti_high.html')

@app.route('/courts/greenhills')

def greenhills():
    return render_template('greenhills_high.html')

@app.route('/courts/clague')

def clague():
    return render_template('clague_middle.html')

@app.route('/courts/sugarbush')

def sugarbush():
    return render_template('sugarbush.html')

#@app.route('/match')

#def match():
    #return render_template('match.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
