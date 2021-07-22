import os
from flask import Flask, render_template, request, redirect, session, flash, \
    url_for, send_from_directory
from flask.helpers import get_flashed_messages

from models import Game, User
from dao import GameDao, UserDao
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'playlib_secrect'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'playlib'
app.config['MYSQL_PORT'] = 3306

app.config['UPLOAD_PATH'] = \
    os.path.dirname(os.path.abspath(__file__)) + '/uploads'

db = MySQL(app)
game_dao = GameDao(db)
user_dao = UserDao(db)

@app.route('/')
def index():
    game_list = game_dao.list()
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
    saved = game_dao.save(game)

    file = request.files['file']
    upload_path = app.config['UPLOAD_PATH']
    file.save(f'{upload_path}/cover{saved.id}.jpg')
    
    return redirect(url_for('index'))


@app.route('/edit/<int:id>')
def edit(id):
    if 'user_logged' not in session or session['user_logged'] == None:
        return redirect(url_for('login', next=url_for('edit')))
    game = game_dao.find_per_id(id)
    game_cover = f'cover{id}.jpg'
    return render_template('edit.html', title='Edit Game', game=game, game_cover=game_cover)


@app.route('/update', methods=['POST'])
def update():
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']
    id = request.form['id']

    game = Game(name, category, console, id)
    game_dao.save(game)

    return redirect(url_for('index'))
    

@app.route('/delete/<int:id>')
def delete(id):
    game_dao.delete(id)
    flash('Game deleted')
    return redirect(url_for('index'))


@app.route('/login')
def login():
    next = request.args.get('next')
    return render_template('login.html', next=next)


@app.route('/auth', methods=['POST'])
def auth():
    user = user_dao.find_per_id(request.form['user'])
    if user:
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


@app.route('/uploads/<filename>')
def image(filename):
    return send_from_directory('uploads', filename)
    

app.run(debug=True)
