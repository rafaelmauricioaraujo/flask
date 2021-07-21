from models import Game, User

SQL_DELETE_GAME = 'delete from game where id = %s'
SQL_GAME_PER_ID = 'SELECT id, name, category, console from game where id = %s'
SQL_USER_PER_ID = 'SELECT id, name, password from user where id = %s'
SQL_UPDATE_GAME = 'UPDATE game SET name=%s, category=%s, console=%s where id = %s'
SQL_FIND_GAME = 'SELECT id, name, category, console from game'
SQL_CREATE_GAME = 'INSERT into game (name, category, console) values (%s, %s, %s)'

class GameDao:
    def __init__(self, db):
        self.__db = db

    def save(self, game):
        cursor = self.__db.connection.cursor()

        if (game.id):
            cursor.execute(SQL_UPDATE_GAME, (game.name, game.category, game.console, game.id))
        else:
            cursor.execute(SQL_CREATE_GAME, (game.name, game.category, game.console))
            game.id = cursor.lastrowid
        self.__db.connection.commit()
        return game

    def list(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_FIND_GAME)
        games = convert_games(cursor.fetchall())
        return games

    def find_per_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_GAME_PER_ID, (id,))
        tupla = cursor.fetchone()
        return Game(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def delete(self, id):
        self.__db.connection.cursor().execute(SQL_DELETE_GAME, (id, ))
        self.__db.connection.commit()


class UserDao:
    def __init__(self, db):
        self.__db = db

    def find_per_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USER_PER_ID, (id,))
        data = cursor.fetchone()
        user = convert_user(data) if data else None
        return user


def convert_games(games):
    def make_game_with_tupla(tupla):
        return Game(tupla[1], tupla[2], tupla[3], id=tupla[0])
    return list(map(make_game_with_tupla, games))


def convert_user(tupla):
    return User(tupla[0], tupla[1], tupla[2])
