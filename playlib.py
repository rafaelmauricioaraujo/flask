from flask import Flask, render_template, request

app = Flask(__name__)

class Game:
    def __init__(self, name, category, console):
        self.name = name
        self.category = category
        self.console = console

game1 = Game('Super-Mario', 'Adventure', 'NES')
game2 = Game('Pokemon Gold', 'RPG', 'GBA')
game3 = Game('Mortal Combat', 'Action', 'SNES')
game_list = [game1, game2, game3]

@app.route('/home')
def home():
    return render_template('list.html',title='Games',game_list=game_list)

@app.route('/new')
def new():
    return render_template('new.html', title='New Game')

@app.route('/create')
def create():
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']

    game = Game(name, category, console)
    game_list.append(game)

    return render_template('list.html', title='Games', game_list=game_list)


app.run()

