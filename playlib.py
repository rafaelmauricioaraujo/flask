from flask import Flask, render_template

app = Flask(__name__)

class Game:
    def __init__(self, name, category, console):
        self.name = name
        self.category = category
        self.console = console


@app.route('/home')
def ola():
    game1 = Game('Super-Mario', 'Adventure', 'NES')
    game2 = Game('Pokemon Gold', 'RPG', 'GBA')
    game3 = Game('Mortal Combat', 'Action', 'SNES')
    game_list = [game1, game2, game3]
    return render_template('list.html',title='Games',game_list=game_list)

app.run()
