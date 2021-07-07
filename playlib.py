from flask import Flask, render_template

app = Flask(__name__)

@app.route('/home')
def ola():
    return render_template('list.html')

app.run()
