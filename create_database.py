import MySQLdb
print('Connecting...')
conn = MySQLdb.connect(user='root', passwd='admin', host='127.0.0.1', port=3306)

conn.cursor().execute("DROP DATABASE `playlib`;")
conn.commit()

create_tables = '''SET NAMES latin1;
    CREATE DATABASE `playlib` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
    USE `playlib`;
    CREATE TABLE `game` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `name` varchar(50) COLLATE utf8_bin NOT NULL,
      `category` varchar(40) COLLATE utf8_bin NOT NULL,
      `console` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    CREATE TABLE `user` (
      `id` varchar(8) COLLATE utf8_bin NOT NULL,
      `name` varchar(20) COLLATE utf8_bin NOT NULL,
      `password` varchar(8) COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''

conn.cursor().execute(create_tables)

# insert users
cursor = conn.cursor()
cursor.executemany(
      'INSERT INTO playlib.user (id, name, password) VALUES (%s, %s, %s)',
      [
            ('luan', 'Luan Marques', 'flask'),
            ('nico', 'Nico', '7a1'),
            ('danilo', 'Danilo', 'vegas')
      ])

cursor.execute('select * from playlib.user')
print(' -------------  Users:  -------------')
for user in cursor.fetchall():
    print(user[1])

# insert games
cursor.executemany(
      'INSERT INTO playlib.game (name, category, console) VALUES (%s, %s, %s)',
      [
            ('God of War 4', 'Ação', 'PS4'),
            ('NBA 2k18', 'Esporte', 'Xbox One'),
            ('Rayman Legends', 'Indie', 'PS4'),
            ('Super Mario RPG', 'RPG', 'SNES'),
            ('Super Mario Kart', 'Corrida', 'SNES'),
            ('Fire Emblem Echoes', 'Estratégia', '3DS'),
      ])

cursor.execute('select * from playlib.game')
print(' -------------  Games:  -------------')
for game in cursor.fetchall():
    print(game[1])

# commit
conn.commit()
cursor.close()