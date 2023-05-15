#chrome://net-internals/#sockets
#[Flush socket pools]

from flask import Flask, render_template, request, redirect, url_for, session

import random
import mysql.connector
import csv

#Make Connection
#change password for your personal password!
conn = mysql.connector.connect(host="localhost",
                                user = "root",
                                password = "Clippers47!",
                                auth_plugin = 'mysql_native_password',
                                database = "application")


cursor = conn.cursor()


# these three lines are needed to use flask
app = Flask(__name__)
app = Flask(__name__, template_folder='template')
app.secret_key = "SecretKey"


# Starting screen for the website
@app.route("/index")
def index():

    # takes us to index.html screen
    return render_template('index.html')


# this is the coach-sign in html screen
# the function will store the session's coachID and coachName
@app.route("/coach_sign",methods=['GET','POST'])
def coach_sign():
        msg = ''
        if request.method == 'POST':
            coachID = request.form['coachID']
            coachName = request.form['coachName']

            # Query to find all coaches with this CoachID and CoachName
            cursor.execute('SELECT * FROM coach WHERE coachID = %s AND name = %s;', (coachID,coachName,))
            record = cursor.fetchone()
            if record:
                # Coach was found
                session['coachID'] = coachID
                session['coachName'] = coachName

                # takes us to 'coaches.html'
                return redirect(url_for('coach'))
            else:
                # CoachID and CoachName was not found.
                msg = 'Incorrect coachID/Name'
        return render_template('coach_sign.html',msg=msg)


# This is the screen that appears when the Coach successfully signs in
@app.route("/coach",methods=['GET','POST'])
def coach():
    coachID = session['coachID']
    coachName = session['coachName']

    # query to find the teamID that the Coach coaches.
    cursor.execute("SELECT * FROM teams WHERE coachID = %s;", (coachID,))
    teamID = cursor.fetchone()[0]
    session['teamID'] = teamID

    # option selected from coach.html
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



# When the coach selects standings from coach.html, then we are brought here
@app.route("/coach_standings")
def coach_standings():

        # query to order teams by wins, then total Goals
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

        # this for loop allows us to manipulate and place the teams with a ranking
        for i in standings:
            a = list(i)
            a.append(place)
            i = tuple(a)
            place = place + 1
            new_standings.append(a)


        return render_template('coach_standings.html',standings=new_standings)


# when coaches select View All Goals
@app.route("/goals")
def goals():

    # First Query that joins three tables
    query = '''
    SELECT goal.gameID, goal.goalID, player.name, teams.teamName
    FROM goal
    JOIN player ON goal.playerID = player.playerID
    JOIN teams ON teams.teamID = player.teamID
    ORDER BY goal.gameID ASC;
    '''

    cursor.execute(query)
    records = cursor.fetchall()
    return render_template('view_all_goals.html',records=records)


# Coach wants to see stats of all the teams. First they must select a team.
@app.route("/team_option",methods=['GET','POST'])
def team_option():
    msg = ''
    cursor.execute("SELECT * FROM teams;")
    teams = cursor.fetchall()
    if request.method == 'POST':
        # this allows us to remember what teamID the coach wants to see
        session['currentID'] = request.form['teamID']
        teamID = session['currentID']

        # make sure the coach entered a number (prevent int error)
        if teamID.isnumeric() == False:
            msg = 'Incorrect. Try again!'
        else:
            found = False
            for i in teams:
                if int(teamID) == int(i[0]):
                    # team entered was found
                    found = True

            if found:
                # team was found, redirect to view that teams_stats
                return redirect(url_for('team_stats'))
            else:
                # team was not found
                msg = 'Incorrect. Try again!'
    return render_template('team_option.html',teams=teams,msg=msg)


# Coach is brought to this screen after successfully choosing a team.
@app.route("/team_stats",methods=['GET','POST'])
def team_stats():
    # get current teamID using session
    currID = session['currentID']

    # get all the info for this current teamID
    cursor.execute("SELECT * FROM player WHERE teamID = %s;",(currID,))
    players = cursor.fetchall()
    return render_template('team_stats.html',data=players)


# view coaches screen
@app.route("/view_coaches")
def view_coaches():
    # simple queyr to get all the coaches in the database
    cursor.execute('SELECT * FROM coach;')
    coaches = cursor.fetchall()
    return render_template('view_coaches.html',coaches=coaches)


# view_all_games screen. The coach must pick what game they want to select first
# before looking at the full game details
@app.route("/view_all_games",methods=['GET','POST'])
def view_all_games():
    msg = ''

    # this is the View used in the application
    # this query gives more information to coach by telling team names, not just teamID
    query = '''
    CREATE VIEW allGames AS
    SELECT g.gameID, g.homeID, t1.teamName AS homeTeam, g.homeScore,g.awayID, t2.teamName AS awayTeam, g.awayScore
    FROM game g
    JOIN teams t1 ON g.homeID = t1.teamID
    JOIN teams t2 ON g.awayID = t2.teamID
    ;
    '''

    cursor.execute(query)

    # simple query to view the view we created
    query = '''
    SELECT *
    FROM allGames;
    '''

    cursor.execute(query)
    games = cursor.fetchall()


    # dropping the view so that it can be created again later.
    query = '''
    DROP VIEW allGames;
    '''
    cursor.execute(query)

    if request.method == 'POST':
        gameID = request.form['gameID']

        # making sure gameID entered was a number
        if gameID.isnumeric() == True:
            found = False
            for i in games:
                if int(gameID) == int(i[0]):
                    found = True

            if found:
                # gameID was found. Take coach to view_game_info_coach screen to view stats of game
                session['gameID'] = gameID
                return redirect(url_for('view_game_info_coach'))
            else:
                # gameID was not found in database.
                msg = 'Incorrect GameID. Try again!'
        else:
            # user did not enter a number
            msg = 'Incorrect GameID. Try again!'

    return render_template('view_all_games.html',games=games,msg=msg)


# Coach successfully picked a gameID from the list of games.
# The coach will be brought to this screen.
@app.route("/view_game_info_coach",methods=['GET','POST'])
def view_game_info_coach():
    # get all the goals from the gameID choosen
    goals = getGoalsInfo(session['gameID'])
    gameID = session['gameID']
    game = getGameInfo(gameID)
    teamID = teamName(game[1])[0]
    otherID = teamName(game[2])[0]
    homeScore = game[3]
    awayScore = game[4]
    return render_template('view_game_info_coach.html',goals=goals,gameID=session['gameID'],teamID=teamID,otherID=otherID,homeScore=homeScore,awayScore=awayScore)



# team_sign simulates a team signing into the website.
# The team will sign in with their teamID and teamName.
@app.route("/team_sign",methods=['GET','POST'])
def team_sign():
    msg = ''
    #
    if request.method == 'POST':
        teamID = request.form['teamID']
        teamName = request.form['teamName']

        # query to get all the teams where teamID and teamName are the same as form submitted.
        cursor.execute('SELECT * FROM teams WHERE teamID = %s AND teamName = %s', (teamID, teamName,))
        record = cursor.fetchone()

        # check if the team exists, or entered correctly.
        if record:
            session['teamID'] = teamID
            session['teamName'] = teamName
            return redirect(url_for('teams'))
        else:
            # teamID or teamName was wrong, or not in the database.
            msg = 'Incorrect teamID/teamName!'

    return render_template('team_sign.html', msg=msg)


# player sign-in screen.
# if the player submits a playerID and playerName that is correctly in the
# database, then the player will sign-in.
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
            # playerID or playerName not found
            msg = 'Incorrect playerID/Name'
    return render_template('player_sign.html',msg=msg)


# player successfully signed-in
# this screen will have a dropdown menu that will allow the user
# choose from a variety of options. Whatever option chosen, the player will
# go to that screen.
@app.route("/players",methods=['GET','POST'])
def players():
    playerID = session['playerID']
    playerName = session['playerName']

    # simple query to get the teamID for this player (teamID = records[5])
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



# this screen will have the top 10 player goal scorers in the league.
# a query will get the playerID, playerName, goals scored, and their team name
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

    # for loop allows us to manipulate and rank the players. This is better
    # for the user to understand what place each player is
    for i in records:
        a = list(i)
        a.append(rank)
        new_rankings.append(a)
        rank = rank + 1
    return render_template('leaders.html',records=new_rankings)


# this screen allows the player to view the goals they score in each game their
# team have played in.
@app.route("/each_game",methods=['GET','POST'])
def each_game():
    playerID = session['playerID']
    teamID = session['teamID']
    playerName = session['playerName']


    # Subquery ??
    # this query is complicated. First the IFNULL is used because if the
    # player does not score in that game, they will be given 0 goals. Without this
    # the game would have been completely forgotten when returned.
    # Then game will left join with another query, on gameID
    # Then it will be grouped by each game.
    # Lastly, if the team the player was on played in that game, then it
    # would select those.
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


# This is the personal_stats screen. This function will have a simple query
# that selects all of the information for this specific player.
@app.route("/personal_stats",methods=['GET','POST'])
def personal_stats():
    playerID = session['playerID']
    teamID = session['teamID']
    playerName = session['playerName']
    cursor.execute("SELECT * FROM player WHERE playerID = %s",(playerID,))
    stats = cursor.fetchall()
    return render_template('personal_stats.html',playerName=playerName,stats=stats)


# This screen will take the player to view all the games their team have player in.
# They will get an option to choose one of the games by typing in the gameID into the
# the form.
@app.route("/view_games_player",methods=['GET','POST'])
def view_games_player():
    teamID = session['teamID']
    games = viewGamesMore()
    msg = ''
    if len(games)==0:
        # The players team have not played a game
        msg = 'You do not have any Games Played!'
    else:
        if request.method == 'POST':
            gameID = request.form['gameID']
            if(gameID.isnumeric()==False):
                # player did not enter a number
                msg = 'Incorrect. Try again!'
            else:
                gameID = int(gameID)
                found = False
                ind = 0
                for i in games:
                    if(i[0] == gameID):
                        # gameID was found
                        found = True
                        break
                    ind = ind + 1

                if found:
                    session['gameID'] = gameID
                    return redirect(url_for('view_game_info_player'))

    return render_template('view_games_player.html',games=games)


# This screen will show the full game stats that player choose.
# The screen will have the players team, the opponents team, both teams
# scores, and all the players who scored in that specified game.
@app.route("/view_game_info_player",methods=['GET','POST'])
def view_game_info_player():
    goals = getGoalsInfo(session['gameID'])
    gameID = session['gameID']
    game = getGameInfo(gameID)

    #getting the teamIDs
    teamID = teamName(game[1])[0]
    otherID = teamName(game[2])[0]

    #scores for both teams
    homeScore = game[3]
    awayScore = game[4]
    return render_template('view_games_info_player.html',goals=goals,gameID=session['gameID'],teamID=teamID,otherID=otherID,homeScore=homeScore,awayScore=awayScore)

# This is the teams page, once the team successfully signs in.
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
        elif(team_choice=='download'):
            teamID = session['teamID']
            with open('download.csv', 'w', newline='') as file:
            # simple query to select all the players that have the teams teamID
                cursor.execute('SELECT * FROM player WHERE teamID = ' + str(teamID) + ';')
                teams = cursor.fetchall()
                writer = csv.writer(file)
                field = ["teamID", "teamName", "teamCity","wins","losses","totalGoals","coachID"]

                writer.writerow(field)
                for i in teams:
                    writer.writerow(i)


    return render_template('teams.html',data=value,name=session['teamName'],teamID=session['teamID'])

# This is the Delete for the application.
# Similar to many of the other game screens, this screen will show
# the games played by the team. Whatever gameID they want to delete they
# can simply type the GameID into the website and click submit.
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

                # gameInfo is all of the info of the game being deleted
                gameInfo = getGameInfo(gameID)


                deleteGameMore(gameID)
                deleteGameGoals(gameID)
                totalWins = getWins(gameInfo[1])
                totalLoss = getLosses(gameInfo[1])

                # updating both teams records because one game is gone now.
                updateTeamRecord(gameInfo[1],totalWins,totalLoss)
                totalWins = getWins(gameInfo[2])
                totalLoss = getLosses(gameInfo[2])
                updateTeamRecord(gameInfo[2],totalWins,totalLoss)
                updateTeamGoals(gameInfo[1])
                updateTeamGoals(gameInfo[2])

                # queries to get all of the players on both teams
                cursor.execute('SELECT * FROM player WHERE teamID = ' + str(gameInfo[1]) + ';')
                team1 = cursor.fetchall()
                cursor.execute('SELECT * FROM player WHERE teamID = ' + str(gameInfo[2]) + ';')
                team2 = cursor.fetchall()
                for i in team1:
                    #updating total goals for each player on team1
                    updatePlayerGoals(i[0])

                for i in team2:
                    #updating total goals for each player on team2
                    updatePlayerGoals(i[0])
                return redirect(url_for('teams'))
            else:
                msg = 'Game Not Found!'


    return render_template('delete_game.html',games=games,msg=msg)

# deletes the game from the database given the gameID
def deleteGameMore(gameID):
    query = '''
    DELETE FROM game
    WHERE gameID = %s
    ;
    '''

    cursor.execute(query,(gameID,))
    conn.commit()

# deletes all the goals that happened during the GameID that was chosen to be deleted.
def deleteGameGoals(gameID):
    query = '''
    DELETE FROM goal
    WHERE gameID = %s
    ;
    '''

    cursor.execute(query,(gameID,))
    conn.commit()

# standings screen for the team.
@app.route("/standings",methods=['GET','POST'])
def standings():
    # query to get all the teams ordered by their wins, then goals
    query = '''
    SELECT *
    FROM teams
    ORDER BY wins DESC, totalGoals DESC
    ;
    '''

    cursor.execute(query)
    standings = cursor.fetchall()

    cursor.execute("SHOW INDEX FROM teams WHERE Key_name = 'team_index'")
    result = cursor.fetchone()

    if result:
        print('team_index already exists')
    else:
        cursor.execute("CREATE INDEX team_index ON teams (teamName)")
    place = 1
    new_standings = []
    for i in standings:
        # list manipulation to insert their ranking
        a = list(i)
        a.append(place)
        i = tuple(a)
        place = place + 1
        new_standings.append(a)


    return render_template('standings.html',standings=new_standings)


# updating the team name and or city
@app.route("/update_team",methods=['GET','POST'])
def update_team():
    if request.method == 'POST':
        teamID = session['teamID']
        team_name = request.form['name']
        team_city = request.form['city']

        # a query to that updates the team city or name that is signed in
        updateTeamQuery(teamID,team_name,team_city)
        return redirect(url_for('teams'))
    return render_template('update_team.html')


# updating the team info
def updateTeamQuery(teamID,name,city):
    # simple query to update the teamName where the teamID is the current teamID
    query = '''
    UPDATE teams
    SET teamName = %s
    WHERE teamID = %s
    ;
    '''

    # simple query to updaet the teamCity where the teamID is the current teamID
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

# view games that team has played in.
# very similar to view_game for the player.

@app.route("/view_games",methods=['GET','POST'])
def view_games():
    games1 = viewGamesMore()
    msg = ''
    if (len(games1)==0):
        # the team has not played in any games.
        msg = 'Your team has not played any games! Schedule a game in the main menu!'
    if request.method == 'POST':
        gameID = request.form['gameID']
        if(gameID.isnumeric()==False):
            # ensuring the user entered a number
            msg = 'Incorrect. Try again!'
        else:
            gameID = int(gameID)
            found = False
            ind = 0
            for i in games1:
                if(i[0] == gameID):
                    # game found
                    found = True
                    break
                ind = ind + 1

            if found:
                session['gameID'] = gameID
                return redirect(url_for('view_game_info'))

    return render_template('view_games.html',msg=msg,games=games1)

# this screen comes from the previous function. The screen will consist of the
 # scores for both teams, and the goals scored in that game, and the player who scored it.
@app.route("/view_game_info",methods=['GET','POST'])
def view_game_info():
    goals = getGoalsInfo(session['gameID'])
    gameID = session['gameID']
    game = getGameInfo(gameID)

    # query to receive the teamName of the teamID
    teamID = teamName(game[1])[0]
    otherID = teamName(game[2])[0]

    # the tuple game has the information for the home and away scores, so simply taking where it would be.
    homeScore = game[3]
    awayScore = game[4]
    return render_template('view_games_info.html',goals=goals,gameID=session['gameID'],teamID=teamID,otherID=otherID,homeScore=homeScore,awayScore=awayScore)


# used from previous function. This function simplt returns the teamName given the teamID
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


# 2nd Query that joins across three tables.
# this table will get the gameID, goalID, playerID, player Name, and more
# then return it.
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

# This function will get necessary information in the game, and more information
# across the team tables to display better data and results.
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


# this screen will allow the team to add a player to the team.
# when a player is added, it is assumed that they played in the previous
# games before.
@app.route("/add_player",methods=['GET','POST'])
def add_player():
    msg = ''
    if request.method == 'POST':
        player_name = request.form['name']
        player_age = request.form['age']
        if(player_age.isnumeric()==False):
            # making sure that the age is a number
            msg = 'Incorrect Value. Try Again'
        else:
            player_age = int(player_age)
            teamID = session['teamID']
            player_pos = request.form['option']

            # insert query to add player to database.
            cursor.execute('''
            INSERT INTO player(name,age,position,teamID)
            VALUES (%s, %s, %s, %s)
            ;
            ''', (player_name,player_age,player_pos,teamID))

            conn.commit()

            return redirect(url_for('teams'))

    return render_template('add_player.html',msg=msg)

# this screen allows the team to view the players on their own team
@app.route("/view_players",methods=['GET','POST'])
def view_players():
    teamID = session['teamID']
    teamName = session['teamName']

    # simple query to select all the players that have the teams teamID
    cursor.execute('SELECT * FROM player WHERE teamID = ' + str(teamID) + ';')
    records = cursor.fetchall()

    return render_template('view_players.html',data=records)


# this screen allows the team logged in, to schedule a game with another team in the league.
# when a team schedules a game, the team scheduling the game (team logged in) will automatically be the home team.
@app.route("/schedule_game",methods=['GET','POST'])
def schedule_game():
    msg = ''
    homeID = session['teamID']

    # query to get all teams except team that is logged in
    cursor.execute('SELECT * FROM teams WHERE teamID != ' + str(homeID) + ';')
    records = cursor.fetchall()
    if request.method == "POST":
        awayID = request.form['awayID']
        if(awayID.isnumeric()==False):
            # making sure team enters teamID as number
            msg = "Incorrect AwayID"
        else:
            awayID = int(awayID)

            # this query is making sure that the teamID exists and is not the team logged in
            query = "SELECT * FROM teams WHERE teamID = "
            query = query + str(awayID) + ' AND teamID != '
            query = query + str(homeID) + ';'
            cursor.execute(query)
            record = cursor.fetchall()
            if(len(record)==0):
                # team was not found
                msg = "Choose an teamID from the list below!"
            else:
                # inserting into game table. The defeault score is 0, 0
                # The stats must be edited to change score.
                cursor.execute('''
                INSERT INTO game(homeID,awayID,homeScore,awayScore)
                VALUES (%s, %s, 0, 0);
                ''', (homeID,awayID,))
                conn.commit()

                return redirect(url_for('teams'))

    return render_template('schedule_game.html',data=records, msg=msg)

# edit_game is very similar to other view games.
# the main differnet is that it takes us to an edit_game_advanced screen afterwords
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



# This was the most complicated function to write, and had the most functions.
# the overall function will allow the team to enter a playerID for either team.
# when the goal is entered, the stats will automatically update on the page.
# To successfully save everything, the user will submit their last goal with save game, instead of continue game.
@app.route("/edit_game_advanced",methods=['GET','POST'])
def edit_game_advanced():
    msg = ''
    players = ''

    players = getPlayerTeam(session['teamID'])
    players2 = getPlayerTeam(session['otherID'])

    game = getGameInfo(session['gameID'])

    # used for the html
    homeScore = game[3]
    awayScore = game[4]


    if request.method == 'POST':
        saving = request.form['option']
        playerID = request.form['playerID']

        # checking if playerID entered is on either the home team or away team
        record = checkPlayerValidity(playerID,session['teamID'],session['otherID'])

        if(len(record)==0):
                msg = '''
                PlayerID not present in this Game.
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

                # updating the score for both teams
                if(team_of_player==game[1]):
                    homeTeamScoreUpdate(team_of_player,game[0])

                else:
                    awayTeamScoreUpdate(team_of_player,game[0])

                # getting the teamID of the player who scored
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
                # continue option was clicked.

                # inserting the playerID who scored in this game
                insertIntoGoal(playerID,session['gameID'])
                team_of_player = teamOfPlayer(playerID)

                # updating the total goals that the player has scored
                updatePlayerGoals(playerID)

                record = getGameGoals(session['gameID'])

                #
                teamTotalGoals(record[0][0])
                if(len(record)!=1):
                    # if the other team has scored, we can
                    teamTotalGoals(record[1][0])

                # updating score information for team that scored
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
                    # only one team scored. Update the team that scored that game.
                    if int(session['teamID']) == int(record[0][0]):
                        gameOutcome(session['otherID'],session['gameID'])
                        updateTeamGoals(session['otherID'])
                    else:
                        gameOutcome(session['teamID'],session['gameID'])
                        updateTeamGoals(session['teamID'])


    if int(session['teamID']) == int(game[1]):
        a = 1 #nothing here
    else:
        # these lines were added because if one team scheduled a game, then
        # the other team edited it, I had to be able to change the scores
        # that were displayed. I created the function by assuming the team that
        # scheduled the game (home team) was editing. However, the away team
        # can also update the score, so if this is the case the scores between
        # the two teams would need to be 'swapped.'
        homeScore_other = homeScore
        homeScore = awayScore
        awayScore = homeScore_other
    return render_template('edit_game_advanced.html',msg=msg,data=players2,teamID=session['teamID'],otherID=session['otherID'],gameID=session['gameID'],homeScore=homeScore,awayScore=awayScore,data1=players)



# updating the goals for the player who scored in the game
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

# getting wins, losses for the teams
def gameOutcome(teamID,gameID):
    game = getGameInfo(gameID)
    homeID = game[1]
    homeScore = game[3]
    awayID = game[2]
    awayScore = game[4]

    # ensuring we are updating the correct teamID
    if int(homeID) == int(teamID):
        currID = homeID
    else:
        currID = awayID

    #still getting wins and losses anyways?
    totalWins = getWins(currID)
    totalLoss = getLosses(currID)

    updateTeamRecord(currID,totalWins,totalLoss)

# updating wins, and losses for the team
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

    query2 = '''
    SELECT coachID
    FROM teams
    WHERE teamID = %s
    ;
    '''

    cursor.execute(query2,(currID,))
    coachID = cursor.fetchone()[0]

    query3 = '''
    UPDATE coach
    SET wins = %s
    WHERE coachID = %s
    ;
    '''

    cursor.execute(query3,(totalWins,coachID,))
    conn.commit()
    cursor.execute(query,(totalWins,currID,))
    conn.commit()
    cursor.execute(query1,(totalLoss,currID,))
    conn.commit()

# two queriers that calculates the wins for the teamID given they are home and away
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


# two queriers that calculates the losses for the teamID given they are home and away
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



# returns from a query of the total goals scored by a team in a game
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

# this function is to ensure a playerID is in the two teams in the specific game
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


# updating the total goals for the team
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

# getting all of the information of a specific gameID
def getGameInfo(gameID):
    cursor.execute('''
    SELECT *
    FROM game
    WHERE gameID = %s
    ;
    ''', (gameID,))

    game = cursor.fetchone()

    return game

# getting all of the goals scored by a specific teamID
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

# getting the teamID of a player given the playerID
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

# inserting the player who scored into the goal table
def insertIntoGoal(playerID, gameID):
    query = '''
    INSERT INTO goal (playerID,gameID)
    VALUES (%s, %s)
    ;
    '''
    cursor.execute(query,(playerID,gameID,))
    conn.commit()


# getting all players who are on a specific teamID
def getPlayerTeam(teamID):
    cursor.execute('''
    SELECT *
    FROM player
    WHERE teamID = %s
    ;
    ''', (teamID,))

    record = cursor.fetchall()
    return record

# updating the homeTeams score
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
