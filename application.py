#chrome://net-internals/#sockets
#[Flush socket pools]

from flask import Flask, render_template, request, redirect, url_for, session

import random
import mysql.connector

#Make Connection
conn = mysql.connector.connect(host="localhost",
                                user = "root",
                                password = "Clippers47!",
                                auth_plugin = 'mysql_native_password',
                                database = "application")


cursor = conn.cursor()


app = Flask(__name__)
app = Flask(__name__, template_folder='template')
app.secret_key = "SecretKey"

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/coach_sign")
def coach_sign():
    return render_template('coach_sign.html')


@app.route("/team_sign",methods=['GET','POST'])
def team_sign():
    msg = ''

    if request.method == 'POST':
        teamID = request.form['teamID']
        teamName = request.form['teamName']
        cursor.execute('SELECT * FROM teams WHERE teamID = %s AND teamName = %s', (teamID, teamName,))
        record = cursor.fetchone()
        if record:
            #return teams(teamName,teamID)
            session['teamID'] = teamID
            session['teamName'] = teamName
            return redirect(url_for('teams'))
            #return render_template('teams')
        else:
            msg = 'Incorrect teamID/teamName!'

    # Show the login form with message (if any
    return render_template('team_sign.html', msg=msg)

@app.route("/player_sign")
def player_sign():
    return render_template('player_sign.html')



@app.route("/teams",methods=['GET','POST'])
def teams():
    cursor.execute('SELECT * FROM teams;')
    value = cursor.fetchall()
    print(value)
    if request.method == 'POST':
        team_choice = request.form['option']
        print(team_choice)
        if(team_choice=='add_player'):
            return redirect(url_for('add_player'))
        elif(team_choice=='players'):
            return redirect(url_for('view_players'))
        elif(team_choice=='schedule'):
            return redirect(url_for('schedule_game'))
        elif(team_choice=='edit'):
            return redirect(url_for('edit_game'))


    return render_template('teams.html',data=value,name=session['teamName'],teamID=session['teamID'])


@app.route("/add_player",methods=['GET','POST'])
def add_player():
    msg = ''
    if request.method == 'POST':
        player_name = request.form['name']
        player_age = request.form['age']
        if(player_age.isnumeric()==False):
            msg = 'Incorrect Value. Try Again'
        else:
            player_age = int(player_age)
            teamID = session['teamID']
            player_pos = request.form['option']
            cursor.execute('''
            INSERT INTO player(name,age,position,teamID)
            VALUES (%s, %s, %s, %s)
            ;
            ''', (player_name,player_age,player_pos,teamID))

            conn.commit()

            return redirect(url_for('teams'))

    return render_template('add_player.html',msg=msg)


@app.route("/view_players",methods=['GET','POST'])
def view_players():
    teamID = session['teamID']
    teamName = session['teamName']
    cursor.execute('SELECT * FROM player WHERE teamID = ' + str(teamID) + ';')
    records = cursor.fetchall()

    return render_template('view_players.html',data=records)


@app.route("/schedule_game",methods=['GET','POST'])
def schedule_game():
    msg = ''
    homeID = session['teamID']
    cursor.execute('SELECT * FROM teams WHERE teamID != ' + str(homeID) + ';')
    records = cursor.fetchall()
    if request.method == "POST":
        awayID = request.form['awayID']
        if(awayID.isnumeric()==False):
            msg = "Incorrect AwayID"
        else:
            awayID = int(awayID)
            query = "SELECT * FROM teams WHERE teamID = "
            query = query + str(awayID) + ' AND teamID != '
            query = query + str(homeID) + ';'
            cursor.execute(query)
            record = cursor.fetchall()
            if(len(record)==0):
                msg = "Choose an teamID from the list below!"
            else:
                cursor.execute('''
                INSERT INTO game(homeID,awayID,homeScore,awayScore)
                VALUES (%s, %s, 0, 0);
                ''', (homeID,awayID,))
                conn.commit()

                return redirect(url_for('teams'))

    return render_template('schedule_game.html',data=records, msg=msg)


@app.route("/edit_game",methods=['GET','POST'])
def edit_game():
    msg = ''
    homeID = session['teamID']
    query = 'SELECT * FROM game WHERE homeID = ' + str(homeID)
    query = query + ' OR awayID = ' + str(homeID) + ';'
    cursor.execute(query)
    games = cursor.fetchall()
    if(len(games)==0):
        msg = 'You have no games played. Click Home and then schedule a match!'
    else:
        if request.method == 'POST':
            gameID = request.form['gameID']
            if(gameID.isnumeric()==False):
                msg = 'Incorrect. Try again!'
            else:
                gameID = int(gameID)
                found = False
                ind = 0
                for i in games:
                    if(i[0] == gameID):
                        found = True
                        break
                    ind = ind + 1

                if(found):
                    session['otherID'] = games[ind][2]
                    if(int(session['otherID'])==int(session['teamID'])):
                        session['otherID'] = games[ind][1]

                    session['gameID'] = gameID
                    return redirect(url_for('edit_game_advanced'))
                else:
                    msg = 'GameID not found for this team. Try again!'

    return render_template('edit_game.html', data=games,msg=msg)


@app.route("/edit_game_advanced",methods=['GET','POST'])
def edit_game_advanced():
    msg = ''
    players = ''
    #need to pass homeID and awayID for this cursor

    players = getPlayerTeam(session['teamID'])
    players2 = getPlayerTeam(session['otherID'])

    game = getGameInfo(session['gameID'])

    homeScore = game[3]
    awayScore = game[4]


    if request.method == 'POST':
        saving = request.form['option']
        playerID = request.form['playerID']

        record = checkPlayerValidity(playerID,session['teamID'],session['otherID'])

        if(len(record)==0):
                msg = '''
                PlayedID not present in this Game.
                If you tried to save this Game, all of the playerID's before this have been kept.
                If you tried to continue this Game, you may continue.
                Please Try Again!
                '''
        else:
            if saving == 'save':
                insertIntoGoal(playerID,session['gameID'])
                team_of_player = teamOfPlayer(playerID)
                updatePlayerGoals(playerID)

                record = getGameGoals(session['gameID'])
                teamTotalGoals(record[0][0])
                if(len(record)!=1):
                    teamTotalGoals(record[1][0])

                if(team_of_player==game[1]):
                    homeTeamScoreUpdate(team_of_player,game[0])

                else:
                    awayTeamScoreUpdate(team_of_player,game[0])

                players = getPlayerTeam(session['teamID'])
                players2 = getPlayerTeam(session['otherID'])

                gameOutcome(record[0][0],session['gameID'])
                updateTeamGoals(record[0][0])

                if(len(record)!=1):
                    gameOutcome(record[1][0], session['gameID'])
                    updateTeamGoals(record[1][0])
                else:
                    if int(session['teamID']) == int(record[0][0]):
                        gameOutcome(session['otherID'],session['gameID'])
                        updateTeamGoals(session['otherID'])
                    else:
                        gameOutcome(session['teamID'],session['gameID'])
                        updateTeamGoals(session['teamID'])

                return redirect(url_for('teams'))

            else:
                insertIntoGoal(playerID,session['gameID'])
                team_of_player = teamOfPlayer(playerID)
                updatePlayerGoals(playerID)

                #team_of_player = teamOfPlayer(playerID)

                record = getGameGoals(session['gameID'])
                teamTotalGoals(record[0][0])
                if(len(record)!=1):
                    teamTotalGoals(record[1][0])

                if(team_of_player==game[1]):
                    homeScore = homeTeamScoreUpdate(team_of_player,game[0])

                else:
                    awayScore = awayTeamScoreUpdate(team_of_player,game[0])

                players = getPlayerTeam(session['teamID'])
                players2 = getPlayerTeam(session['otherID'])

                gameOutcome(record[0][0],session['gameID'])
                updateTeamGoals(record[0][0])

                if(len(record)!=1):
                    gameOutcome(record[1][0], session['gameID'])
                    updateTeamGoals(record[1][0])
                else:
                    if int(session['teamID']) == int(record[0][0]):
                        gameOutcome(session['otherID'],session['gameID'])
                        updateTeamGoals(session['otherID'])
                    else:
                        gameOutcome(session['teamID'],session['gameID'])
                        updateTeamGoals(session['teamID'])

    return render_template('edit_game_advanced.html',msg=msg,data=players2,teamID=session['teamID'],otherID=session['otherID'],gameID=session['gameID'],homeScore=homeScore,awayScore=awayScore,data1=players)




def updatePlayerGoals(playerID):
    query = '''
    SELECT COUNT(*)
    FROM goal
    WHERE playerID = %s
    ;
    '''

    cursor.execute(query,(playerID,))
    numGoals = cursor.fetchone()[0]
    print(numGoals)

    query = '''
    UPDATE player
    SET goals = %s
    WHERE playerID = %s
    ;
    '''
    cursor.execute(query,(numGoals,playerID,))
    conn.commit()


#need to finish this
def teamTotalGoals(teamID):
    query = '''
    SELECT COUNT(*)
    FROM goal
    '''


def gameOutcome(teamID,gameID):
    game = getGameInfo(gameID)
    homeID = game[1]
    homeScore = game[3]
    awayID = game[2]
    awayScore = game[4]
    if int(homeID) == int(teamID):
        print('no?')
        currID = homeID
    else:
        print('yes')
        currID = awayID

    #still getting wins and losses anyways?
    totalWins = getWins(currID)
    totalLoss = getLosses(currID)

    updateTeamRecord(currID,totalWins,totalLoss)

def updateTeamRecord(currID,totalWins,totalLoss):
    query = '''
    UPDATE teams
    SET wins = %s
    WHERE teamID = %s
    ;
    '''

    query1 = '''
    UPDATE teams
    SET losses = %s
    WHERE teamID = %s
    ;
    '''

    cursor.execute(query,(totalWins,currID,))
    conn.commit()
    cursor.execute(query1,(totalLoss,currID,))
    conn.commit()


def getWins(homeID):
    query = '''
    SELECT COUNT(*)
    FROM game
    WHERE homeID = %s
    AND homeScore > awayScore
    ;
    '''

    print(homeID)
    cursor.execute(query,(homeID,))

    homeWins = cursor.fetchone()
    homeWins = homeWins[0]
    print('homeWins: ', homeWins)

    query = '''
    SELECT COUNT(*)
    FROM game
    WHERE awayID = %s
    AND awayScore > homeScore
    ;
    '''

    cursor.execute(query,(homeID,))

    awayWins = cursor.fetchone()
    awayWins = awayWins[0]
    print('awayWins: ', awayWins)
    totalWins = homeWins + awayWins
    return totalWins


def getLosses(homeID):
    query = '''
    SELECT COUNT(*)
    FROM game
    WHERE awayID = %s
    AND homeScore > awayScore
    ;
    '''

    cursor.execute(query,(homeID,))

    homeLoss = cursor.fetchone()
    homeLoss = homeLoss[0]

    query = '''
    SELECT COUNT(*)
    FROM game
    WHERE homeID = %s
    AND awayScore > homeScore
    ;
    '''

    cursor.execute(query,(homeID,))

    awayLoss = cursor.fetchone()
    awayLoss = awayLoss[0]

    return homeLoss + awayLoss




def getGameGoals(gameID):
    query = '''
    SELECT player.teamID, COUNT(*)
    FROM goal
    INNER JOIN player
    ON goal.playerID = player.playerID
    WHERE goal.gameID = %s
    GROUP BY player.teamID;
    '''

    cursor.execute(query,(gameID,))

    record = cursor.fetchall()
    print(record)
    return record


def checkPlayerValidity(playerID,teamID,otherID):
    query = '''
    SELECT *
    FROM player
    WHERE playerID = %s
    AND teamID IN (%s, %s)
    ;
    '''

    cursor.execute(query,(playerID,teamID,otherID,))
    record = cursor.fetchall()
    return record


def updateTeamGoals(teamID):
    query = '''
    SELECT COUNT(*)
    FROM goal
    INNER JOIN player
    ON goal.playerID = player.playerID
    WHERE player.teamID = %s
    ;
    '''

    cursor.execute(query,(teamID,))
    record = cursor.fetchone()
    print(record[0])


    query = '''
    UPDATE teams
    SET totalGoals = %s
    WHERE teamID = %s
    ;
    '''
    cursor.execute(query,(record[0],teamID,))
    print('teamGoals Updated')
    conn.commit()


def getGameInfo(gameID):
    cursor.execute('''
    SELECT *
    FROM game
    WHERE gameID = %s
    ;
    ''', (gameID,))

    game = cursor.fetchone()

    return game


def getTeamGoals(team_of_player):
    query = '''
    SELECT totalGoals
    FROM teams
    WHERE teamID = %s
    ;
    '''

    cursor.execute(query,(team_of_player,))
    value = cursor.fetchone()
    value = value[0]
    return value

def teamOfPlayer(playerID):
        query = '''
        SELECT teamID
        FROM player
        WHERE playerID = %s
        ;
        '''
        cursor.execute(query,(playerID,))
        team_of_player = cursor.fetchone()
        return team_of_player[0]


def insertIntoGoal(playerID, gameID):
    query = '''
    INSERT INTO goal (playerID,gameID)
    VALUES (%s, %s)
    ;
    '''
    cursor.execute(query,(playerID,gameID,))
    conn.commit()

    print("inserted goal for player: ", playerID)


def getPlayerTeam(teamID):
    cursor.execute('''
    SELECT *
    FROM player
    WHERE teamID = %s
    ;
    ''', (teamID,))

    record = cursor.fetchall()
    return record


def homeTeamScoreUpdate(team, game):
    query = '''
    SELECT homeScore
    FROM game
    WHERE gameID = %s
    ;
    '''

    cursor.execute(query,(game,))
    homeScore = cursor.fetchone()
    homeScore = homeScore[0]
    homeScore = homeScore + 1

    query = '''
    UPDATE game
    SET homeScore = %s
    WHERE gameID = %s
    ;
    '''

    cursor.execute(query,(homeScore,game,))
    conn.commit()

    print('successful update')
    return homeScore


def awayTeamScoreUpdate(team, game):
    query = '''
    SELECT awayScore
    FROM game
    WHERE gameID = %s
    ;
    '''

    cursor.execute(query,(game,))
    awayScore = cursor.fetchone()
    awayScore = awayScore[0]
    awayScore = awayScore + 1

    query = '''
    UPDATE game
    SET awayScore = %s
    WHERE gameID = %s
    ;
    '''

    cursor.execute(query,(awayScore,game,))
    conn.commit()

    print('successful update')
    return awayScore


if __name__ == "__main__":
    app.run(debug=True)
#    session = {}


print(conn)
conn.close()
