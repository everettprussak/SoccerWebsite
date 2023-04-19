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

@app.route("/coach_sign",methods=['GET','POST'])
def coach_sign():
        msg = ''
        if request.method == 'POST':
            coachID = request.form['coachID']
            coachName = request.form['coachName']
            cursor.execute('SELECT * FROM coach WHERE coachID = %s AND name = %s;', (coachID,coachName,))
            record = cursor.fetchone()
            if record:
                session['coachID'] = coachID
                session['coachName'] = coachName
                return redirect(url_for('coach'))
            else:
                msg = 'Incorrect coachID/Name'
        return render_template('coach_sign.html',msg=msg)


@app.route("/coach",methods=['GET','POST'])
def coach():
    coachID = session['coachID']
    coachName = session['coachName']
    cursor.execute("SELECT * FROM teams WHERE coachID = %s;", (coachID,))
    teamID = cursor.fetchone()[0]
    session['teamID'] = teamID
    if request.method == 'POST':
        choice = request.form['option']
        if(choice=='league'):
            return redirect(url_for('view_all_games'))
        elif(choice=='team'):
            return redirect(url_for('team_option'))
        elif(choice=='coaches'):
            return redirect(url_for('view_coaches'))
        elif(choice=='standings'):
            return redirect(url_for('coach_standings'))
        elif(choice=='goals'):
            return redirect(url_for('goals'))
    return render_template('coach.html',coachID=coachID,coachName=coachName)


@app.route("/coach_standings")
def coach_standings():
        query = '''
        SELECT *
        FROM teams
        ORDER BY wins DESC, totalGoals DESC
        ;
        '''

        cursor.execute(query)
        standings = cursor.fetchall()
        place = 1
        new_standings = []
        for i in standings:
            a = list(i)
            a.append(place)
            i = tuple(a)
            place = place + 1
            new_standings.append(a)


        return render_template('coach_standings.html',standings=new_standings)

@app.route("/goals")
def goals():
    query = '''
    SELECT goal.gameID, goal.goalID, player.name, teams.teamName
    FROM goal
    JOIN player ON goal.playerID = player.playerID
    JOIN teams ON teams.teamID = player.teamID
    ORDER BY goal.gameID ASC;
    '''

    cursor.execute(query)
    records = cursor.fetchall()
    print(records)
    return render_template('view_all_goals.html',records=records)


@app.route("/team_option",methods=['GET','POST'])
def team_option():
    msg = ''
    cursor.execute("SELECT * FROM teams;")
    teams = cursor.fetchall()
    if request.method == 'POST':
        session['currentID'] = request.form['teamID']
        teamID = session['currentID']
        if teamID.isnumeric() == False:
            msg = 'Incorrect. Try again!'
        else:
            found = False
            for i in teams:
                if int(teamID) == int(i[0]):
                    found = True

            if found:
                return redirect(url_for('team_stats'))
            else:
                msg = 'Incorrect. Try again!'
    return render_template('team_option.html',teams=teams,msg=msg)


@app.route("/team_stats",methods=['GET','POST'])
def team_stats():
    currID = session['currentID']
    print(currID)
    cursor.execute("SELECT * FROM player WHERE teamID = %s;",(currID,))
    players = cursor.fetchall()
    return render_template('team_stats.html',data=players)


@app.route("/view_coaches")
def view_coaches():
    cursor.execute('SELECT * FROM coach;')
    coaches = cursor.fetchall()
    return render_template('view_coaches.html',coaches=coaches)

@app.route("/view_all_games",methods=['GET','POST'])
def view_all_games():
    msg = ''
    query = '''
    CREATE VIEW allGames AS
    SELECT g.gameID, g.homeID, t1.teamName AS homeTeam, g.homeScore,g.awayID, t2.teamName AS awayTeam, g.awayScore
    FROM game g
    JOIN teams t1 ON g.homeID = t1.teamID
    JOIN teams t2 ON g.awayID = t2.teamID
    ;
    '''

    cursor.execute(query)

    query = '''
    SELECT *
    FROM allGames;
    '''

    cursor.execute(query)
    games = cursor.fetchall()

    query = '''
    DROP VIEW allGames;
    '''
    cursor.execute(query)

    if request.method == 'POST':
        gameID = request.form['gameID']
        if gameID.isnumeric() == True:
            found = False
            for i in games:
                if int(gameID) == int(i[0]):
                    found = True

            if found:
                session['gameID'] = gameID
                return redirect(url_for('view_game_info_coach'))
            else:
                msg = 'Incorrect GameID. Try again!'
        else:
            msg = 'Incorrect GameID. Try again!'

    return render_template('view_all_games.html',games=games,msg=msg)


@app.route("/view_game_info_coach",methods=['GET','POST'])
def view_game_info_coach():
    goals = getGoalsInfo(session['gameID'])
    gameID = session['gameID']
    game = getGameInfo(gameID)
    teamID = teamName(game[1])[0]
    otherID = teamName(game[2])[0]
    homeScore = game[3]
    awayScore = game[4]
    return render_template('view_game_info_coach.html',goals=goals,gameID=session['gameID'],teamID=teamID,otherID=otherID,homeScore=homeScore,awayScore=awayScore)




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

@app.route("/player_sign",methods=['GET','POST'])
def player_sign():
    msg = ''
    if request.method == 'POST':
        playerID = request.form['playerID']
        playerName = request.form['playerName']
        cursor.execute('SELECT * FROM player WHERE playerID = %s AND name = %s;', (playerID,playerName,))
        record = cursor.fetchone()
        if record:
            session['playerID'] = playerID
            session['playerName'] = playerName
            return redirect(url_for('players'))
        else:
            msg = 'Incorrect playerID/Name'
    return render_template('player_sign.html',msg=msg)


@app.route("/players",methods=['GET','POST'])
def players():
    playerID = session['playerID']
    playerName = session['playerName']
    cursor.execute("SELECT * FROM player WHERE playerID = %s;",(playerID,))
    records = cursor.fetchone()
    session['teamID'] = records[5]
    teamID = records[5]
    if request.method == 'POST':
        choice = request.form['option']
        if(choice=='games'):
            return redirect(url_for('view_games_player'))
        elif(choice=='personal'):
            return redirect(url_for('personal_stats'))
        elif(choice=='each_game'):
            return redirect(url_for('each_game'))
        elif(choice=='leaders'):
            return redirect(url_for('leaders'))
    return render_template('players.html',playerName=playerName,playerID=playerID)


@app.route("/leaders",methods=['GET','POST'])
def leaders():
    query = '''
    SELECT player.playerID,player.name,player.goals,teams.teamName
    FROM player
    INNER JOIN teams
    ON player.teamID = teams.teamID
    ORDER BY goals DESC,playerID ASC
    LIMIT 10;
    '''

    cursor.execute(query)
    records = cursor.fetchall()
    new_rankings = []
    rank = 1
    for i in records:
        a = list(i)
        a.append(rank)
        new_rankings.append(a)
        rank = rank + 1
    return render_template('leaders.html',records=new_rankings)


@app.route("/each_game",methods=['GET','POST'])
def each_game():
    playerID = session['playerID']
    teamID = session['teamID']
    playerName = session['playerName']

    query = '''
    SELECT g.gameID, IFNULL(COUNT(go.goalID), 0) AS goals_scored, g.homeID, g.awayID
    FROM game g
    LEFT JOIN (SELECT * FROM goal WHERE playerID = %s) go ON g.gameID = go.gameID
    GROUP BY g.gameID
    HAVING g.homeID = %s
    OR g.awayID = %s
    ;
    '''

    cursor.execute(query,(playerID,teamID,teamID,))
    records = cursor.fetchall()
    print(records)

    return render_template('each_game.html',playerName=playerName,goals=records)

@app.route("/personal_stats",methods=['GET','POST'])
def personal_stats():
    playerID = session['playerID']
    teamID = session['teamID']
    playerName = session['playerName']
    cursor.execute("SELECT * FROM player WHERE playerID = %s",(playerID,))
    stats = cursor.fetchall()
    return render_template('personal_stats.html',playerName=playerName,stats=stats)

@app.route("/view_games_player",methods=['GET','POST'])
def view_games_player():
    teamID = session['teamID']
    games = viewGamesMore()
    msg = ''
    if len(games)==0:
        msg = 'You do not have any Games Played!'
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

                if found:
                    session['gameID'] = gameID
                    return redirect(url_for('view_game_info_player'))

    return render_template('view_games_player.html',games=games)


@app.route("/view_game_info_player",methods=['GET','POST'])
def view_game_info_player():
    goals = getGoalsInfo(session['gameID'])
    gameID = session['gameID']
    game = getGameInfo(gameID)
    teamID = teamName(game[1])[0]
    otherID = teamName(game[2])[0]
    homeScore = game[3]
    awayScore = game[4]
    return render_template('view_games_info_player.html',goals=goals,gameID=session['gameID'],teamID=teamID,otherID=otherID,homeScore=homeScore,awayScore=awayScore)

@app.route("/teams",methods=['GET','POST'])
def teams():
    cursor.execute('SELECT * FROM teams;')
    value = cursor.fetchall()
    if request.method == 'POST':
        team_choice = request.form['option']
        if(team_choice=='add_player'):
            return redirect(url_for('add_player'))
        elif(team_choice=='players'):
            return redirect(url_for('view_players'))
        elif(team_choice=='schedule'):
            return redirect(url_for('schedule_game'))
        elif(team_choice=='edit'):
            return redirect(url_for('edit_game'))
        elif(team_choice=='games'):
            return redirect(url_for('view_games'))
        elif(team_choice=='update'):
            return redirect(url_for('update_team'))
        elif(team_choice=='standings'):
            return redirect(url_for('standings'))
        elif(team_choice=='delete_game'):
            return redirect(url_for('delete_game'))


    return render_template('teams.html',data=value,name=session['teamName'],teamID=session['teamID'])


@app.route("/delete_game",methods=['GET','POST'])
def delete_game():
    teamID = session['teamID']
    msg = ''

    games = viewGamesMore()

    if request.method == 'POST':
        gameID = request.form['gameID']
        msg = str(gameID)
        found = False

        for i in games:
            if str(gameID) == str(i[0]):
                found = True

            if found==True:
                msg = 'Game Found'
                gameInfo = getGameInfo(gameID)
                deleteGameMore(gameID)
                deleteGameGoals(gameID)
                totalWins = getWins(gameInfo[1])
                totalLoss = getLosses(gameInfo[1])
                updateTeamRecord(gameInfo[1],totalWins,totalLoss)
                totalWins = getWins(gameInfo[2])
                totalLoss = getLosses(gameInfo[2])
                updateTeamRecord(gameInfo[2],totalWins,totalLoss)
                updateTeamGoals(gameInfo[1])
                updateTeamGoals(gameInfo[2])
                cursor.execute('SELECT * FROM player WHERE teamID = ' + str(gameInfo[1]) + ';')
                team1 = cursor.fetchall()
                cursor.execute('SELECT * FROM player WHERE teamID = ' + str(gameInfo[2]) + ';')
                team2 = cursor.fetchall()
                for i in team1:
                    updatePlayerGoals(i[0])

                for i in team2:
                    updatePlayerGoals(i[0])
                return redirect(url_for('teams'))
            else:
                msg = 'Game Not Found!'


    return render_template('delete_game.html',games=games,msg=msg)


def deleteGameMore(gameID):
    query = '''
    DELETE FROM game
    WHERE gameID = %s
    ;
    '''

    cursor.execute(query,(gameID,))
    conn.commit()

def deleteGameGoals(gameID):
    query = '''
    DELETE FROM goal
    WHERE gameID = %s
    ;
    '''

    cursor.execute(query,(gameID,))
    conn.commit()


@app.route("/standings",methods=['GET','POST'])
def standings():
    query = '''
    SELECT *
    FROM teams
    ORDER BY wins DESC, totalGoals DESC
    ;
    '''

    cursor.execute(query)
    standings = cursor.fetchall()
    place = 1
    new_standings = []
    for i in standings:
        a = list(i)
        a.append(place)
        i = tuple(a)
        place = place + 1
        new_standings.append(a)


    return render_template('standings.html',standings=new_standings)



@app.route("/update_team",methods=['GET','POST'])
def update_team():
    if request.method == 'POST':
        teamID = session['teamID']
        team_name = request.form['name']
        team_city = request.form['city']

        updateTeamQuery(teamID,team_name,team_city)
        return redirect(url_for('teams'))
    return render_template('update_team.html')


def updateTeamQuery(teamID,name,city):
    query = '''
    UPDATE teams
    SET teamName = %s
    WHERE teamID = %s
    ;
    '''

    query1 = '''
    UPDATE teams
    SET teamCity = %s
    WHERE teamID = %s
    ;
    '''

    cursor.execute(query,(name,teamID,))
    conn.commit()
    cursor.execute(query1,(city,teamID,))
    conn.commit()

@app.route("/view_games",methods=['GET','POST'])
def view_games():
    games1 = viewGamesMore()
    msg = ''
    if (len(games1)==0):
        msg = 'Your team has not played any games! Schedule a game in the main menu!'
    if request.method == 'POST':
        gameID = request.form['gameID']
        if(gameID.isnumeric()==False):
            msg = 'Incorrect. Try again!'
        else:
            gameID = int(gameID)
            found = False
            ind = 0
            for i in games1:
                if(i[0] == gameID):
                    found = True
                    break
                ind = ind + 1

            if found:
                session['gameID'] = gameID
                return redirect(url_for('view_game_info'))

    return render_template('view_games.html',msg=msg,games=games1)


@app.route("/view_game_info",methods=['GET','POST'])
def view_game_info():
    goals = getGoalsInfo(session['gameID'])
    gameID = session['gameID']
    game = getGameInfo(gameID)
    teamID = teamName(game[1])[0]
    otherID = teamName(game[2])[0]
    homeScore = game[3]
    awayScore = game[4]
    return render_template('view_games_info.html',goals=goals,gameID=session['gameID'],teamID=teamID,otherID=otherID,homeScore=homeScore,awayScore=awayScore)


def teamName(teamID):
    query = '''
    SELECT teamName
    FROM teams
    WHERE teamID = %s
    ;
    '''

    cursor.execute(query,(teamID,))
    name = cursor.fetchone()
    return name


def getGoalsInfo(gameID):
    query = '''
    SELECT goal.gameID,goal.goalID, player.playerID, player.Name, player.teamID, teams.teamName, teams.teamCity
    FROM goal
    INNER JOIN player
    ON player.playerID = goal.playerID
    INNER JOIN teams
    ON player.teamID = teams.teamID
    WHERE gameID = %s
    ORDER BY goalID ASC;
    '''

    cursor.execute(query,(gameID,))
    goals = cursor.fetchall()
    return goals


def viewGamesMore():
    teamID = session['teamID']
    query = '''
    SELECT g.gameID, g.homeID, t1.teamName AS homeTeam, g.homeScore,g.awayID, t2.teamName AS awayTeam, g.awayScore
    FROM game g
    JOIN teams t1 ON g.homeID = t1.teamID
    JOIN teams t2 ON g.awayID = t2.teamID
    WHERE g.homeID = %s
    OR g.awayID = %s;
    '''

    cursor.execute(query,(teamID,teamID,))
    records = cursor.fetchall()

    return records

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


    if int(session['teamID']) == int(game[1]):
        a = 1 #nothing here
    else:
        homeScore_other = homeScore
        homeScore = awayScore
        awayScore = homeScore_other
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
        currID = homeID
    else:
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

    cursor.execute(query,(homeID,))

    homeWins = cursor.fetchone()
    homeWins = homeWins[0]

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


    query = '''
    UPDATE teams
    SET totalGoals = %s
    WHERE teamID = %s
    ;
    '''
    cursor.execute(query,(record[0],teamID,))
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

    return awayScore


if __name__ == "__main__":
    app.run(debug=True)
#    session = {}


print(conn)
conn.close()
