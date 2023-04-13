import mysql.connector

def first_run():
    conn = mysql.connector.connect(host="localhost",
                                    user = "root",
                                    password = "Clippers47!",
                                    auth_plugin = 'mysql_native_password')


    cursor = conn.cursor()
    cursor.execute('''
    CREATE SCHEMA application
    ''')

def second_run():
    conn = mysql.connector.connect(host="localhost",
                                    user = "root",
                                    password = "Clippers47!",
                                    auth_plugin = 'mysql_native_password',
                                    database = 'application')


    cursor = conn.cursor()
    cursor.execute('''
    DROP TABLE Team;
    ''')

    cursor.execute('''
    CREATE TABLE teams(
        teamID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        teamName VARCHAR(50) UNIQUE NOT NULL,
        teamCity VARCHAR(50) NOT NULL,
        totalGoals INT,
        wins INT,
        losses INT,
        coachID INT
    );
    ''')

    print(conn)
    conn.close()

#first_run()

#second_run()



conn = mysql.connector.connect(host="localhost",
                                user = "root",
                                password = "Clippers47!",
                                auth_plugin = 'mysql_native_password',
                                database = 'application')


cursor = conn.cursor()


def getTeams():
    cursor.execute('''
    SELECT *
    FROM teams;
    ''')

    values = cursor.fetchall()
    print(values)

def enterTeams():
    cursor.execute('''
    INSERT INTO teams(teamName, teamCity, totalGoals, wins, losses)
    VALUES ('Warriors','Golden State',0,0,0)
    ''')
    conn.commit()


def createPlayerTable():
    cursor.execute('''
    CREATE TABLE player(
        playerID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        age INT NOT NULL,
        position VARCHAR(25) NOT NULL,
        goals INT
    );
    ''')


def createTeamInfoTable():
    cursor.execute('''
    ALTER TABLE player
    ADD COLUMN teamID INT;
    ''')

def enterPlayers():
    cursor.execute('''
    INSERT INTO players()
    ''')


def createGameTable():
    cursor.execute('''
    CREATE TABLE game(
        gameID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        homeID INT NOT NULL,
        awayID INT NOT NULL,
        homeScore INT,
        awayScore INT
    )
    ''')

def updateGameTable():
    cursor.execute('''
    UPDATE game
    SET awayID = 3
    WHERE awayID = 6
    AND homeID = 6;
    ''')
    print('done')
    conn.commit()

def createGoalTable():
    cursor.execute('''
    CREATE TABLE goal(
        goalID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        playerID INT NOT NULL,
        gameID INT NOT NULL
    );
    ''')

def createCoachTable():
    cursor.execute('''
    CREATE TABLE coach(
        coachID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50),
        wins INT,
        active INT
    );
    ''')


def misc():
    #Total Goals: Team 3 has 9 goals.
    query = '''
    SELECT player.teamID, COUNT(*)
    FROM goal
    INNER JOIN player
    ON goal.playerID = player.playerID
    GROUP BY player.teamID;
    '''

    cursor.execute(query)
    record = cursor.fetchall()
    print(record)
    for i in record:
        print(i)


    #Total Goals in the season for each player
    query = '''
    SELECT player.playerID, COUNT(*)
    FROM goal
    INNER JOIN player
    ON goal.playerID = player.playerID
    GROUP BY goal.playerID;
    '''

    cursor.execute(query)
    record = cursor.fetchall()
    print(record)
    for i in record:
        print(i)


#Tells the number of goals that each team score in gameID 2
    query = '''
    SELECT player.teamID, COUNT(*)
    FROM goal
    INNER JOIN player
    ON goal.playerID = player.playerID
    WHERE goal.gameID = 2
    GROUP BY player.teamID;
    '''

    cursor.execute(query)
    record = cursor.fetchall()
    print(record)
    for i in record:
        print(i)


def deleteGoals():
    query = '''
    DELETE FROM goal
    '''

    cursor.execute(query)

    conn.commit()


#second_run()


def misc2():
    query = '''
    SELECT player.teamID, goal.gameID, COUNT(*)
    FROM goal
    INNER JOIN player
    ON goal.playerID = player.playerID;
    '''

    cursor.execute(query)
    record = cursor.fetchall()
    print(record)
    for i in record:
        print(i)


def delete():
    query = '''
    DELETE FROM goal;
    '''

    query1 = '''
    DELETE FROM game;
    '''
    cursor.execute(query)
    conn.commit()
    cursor.execute(query1)
    conn.commit()


def restartTeamRecord():
    query = '''
    UPDATE teams
    SET totalGoals = 0
    '''

    query1 = '''
    UPDATE teams
    SET wins = 0
    '''

    query2 = '''
    UPDATE teams
    SET losses = 0
    '''

    query3 = '''
    UPDATE player
    SET goals = NULL
    '''

    cursor.execute(query)
    conn.commit()
    cursor.execute(query1)
    conn.commit()
    cursor.execute(query2)
    conn.commit()
    cursor.execute(query3)
    conn.commit()

#deleteGoals()
#enterTeams()
#createPlayerTable()
#createTeamInfoTable()
#createGameTable()
#getTeams()
#createCoachTable()
#misc()
#misc2()
#createGoalTable()
#updateGameTable()
delete()
restartTeamRecord()

query = '''
SELECT COUNT(*)
FROM game
WHERE homeID = 5
AND homeScore > awayScore
;
'''

cursor.execute(query)
records = cursor.fetchone()
print(records[0])

print(conn)
conn.close()
