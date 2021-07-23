import time
from helpers import delete_cover, get_image
from flask import render_template, request, redirect, session, flash, \
    url_for, send_from_directory

from models import Game
from dao import GameDao, UserDao
from playlib import app, db
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
    timestamp = time.time()
    file.save(f'{upload_path}/cover{saved.id}-{timestamp}.jpg')
    
    return redirect(url_for('index'))


@app.route('/edit/<int:id>')
def edit(id):
    if 'user_logged' not in session or session['user_logged'] == None:
        return redirect(url_for('login', next=url_for('edit')))
    game = game_dao.find_per_id(id)
    img_cover = get_image(id)
    return render_template('edit.html', title='Edit Game', game=game, game_cover=img_cover)


@app.route('/update', methods=['POST'])
def update():
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']
    id = request.form['id']

    game = Game(name, category, console, id)
    game_dao.save(game)

    delete_cover(id)

    file = request.files['file']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()

    file.save(f'{upload_path}/cover{game.id}-{timestamp}.jpg')
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
    
