from flask import Flask, render_template, request, redirect, session, flash, \
    url_for

app = Flask(__name__)
app.secret_key = 'playlib_secrect'

class Game:
    def __init__(self, name, category, console):
        self.name = name
        self.category = category
        self.console = console

game1 = Game('Super-Mario', 'Adventure', 'NES')
game2 = Game('Pokemon Gold', 'RPG', 'GBA')
game3 = Game('Mortal Combat', 'Action', 'SNES')
game_list = [game1, game2, game3]

class User:
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

user1 = User('rafael', 'Rafael', '123' )
user2 = User('teti', 'Teti', '456' )
user3 = User('flavio', 'Flavio', 'js')

users = { user1.id: user1, 
          user2.id: user2,
          user3.id: user3 }


@app.route('/')
def index():
    return render_template('list.html',title='Games',game_list=game_list)


@app.route('/new')
def new():
    if 'user_logged' not in session or session['user_logged'] == None:
        return redirect(url_for('login', next=url_for('new')))
    return render_template('new.html', title='New Game')


@app.route('/create', methods=['POST'])
def create():
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']

    game = Game(name, category, console)
    game_list.append(game)

    return redirect(url_for('index'))


@app.route('/login')
def login():
    next = request.args.get('next')
    return render_template('login.html', next=next)


@app.route('/auth', methods=['POST'])
def auth():
    if request.form['user'] in users:
        user = users[request.form['user']]
        if user.password == request.form['password']:
            session['user_logged'] = user.id
            flash(user.name + ' logged!')
            next_page = request.form['next']
            return redirect(next_page)
    else:
        flash('user or password incorrect!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['user_logged'] = None
    flash('User logout')
    return redirect(url_for('index'))


app.run(debug=True)
