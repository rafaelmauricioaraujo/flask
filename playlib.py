from flask import Flask, render_template

app = Flask(__name__)

@app.route('/home')
def ola():
    game_list = ['Tetris', 'Super-Mario', 'Pokemon Gold']
    return render_template('list.html',title='Games',game_list=game_list)

app.run()
