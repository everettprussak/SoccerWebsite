# FIFA 2022 Soccer Website Database

# By: Everett Prussak and Aidan Lewis-Grenz

## How to run:

### Try install Flask with the following
- pip3 install flask

### Ensure you have mysql and mysqlworkbench downloaded

### python3 scehma_creation.py (schema created, unless datadumping then Option 2)

### Chose either player, team, coaches data without games and goals or option 2 to replicate the entire database.
Option 1 will have no goals for any team or player. Each team will have zero wins and zero losses with no games played. Each coach will have 0 wins. This is because the goals and games datatable is not available in this option. For option 2, if you want to replicate the entire database, then it will include all goals and games as well.

### Option 1: python3 first_run.py (players, teams, and coaches inserted into tables)
- Each Player will start with Null (or zero) goals
- Each team will have zero wins, zero losses, and zero totalGoals
- Each coach will have zero wins.

### Option 2: If you want to replicate the entire database including games, goals, and more, I have provided the datadump of the database. The file is called 'application.sql'

### python3 application.py
- If "Access to 127.0.0.1 was denied" is ever seen do the following:
 - Control + C to disconnect from application.py
 - Go this link (chrome://net-internals/#sockets)
 - Click "Flush socket pools"
 - run application.py again


### Full Commands using Option 1:
- python3 schema_creation.py
- python3 first_run.py
- python3 application.py

### Go to this link (http://127.0.0.1:5000/index)

### To sign-in with a team, you can look inside the WorkBench or simply start with the teamID of 1 and the teamName of Argentina. After that, all of the teams and their teamID will appear. You may sign-in with any of them.

### For player Sign-In, use playerID 1 and Lionel Messi. Again, all of the other players may be signed in with.


### For coach sign-in, you may again use any of the coaches, but coachID 1 and coach Name Lionel Scaloni is given.

## Issues we had:
- We wanted to make 32 teams, but instead went with 10.
- Had issues with using 'COMMIT' inside python code as mentioned above.
 - conn.commit() is used instead


### Project Details

1. Print/display records from your database/tables.
- Records are displayed on html (players, standings, etc.)

2. Query for data/results with various parameters/filters
- A query for top ten goal scorers. A query for team standings.

3. Create a new record
- Add a player to roster. Create a game. Add a goal scorer in a game.

4. Delete records (soft delete function would be ideal)
- Delete game

5. Update records
- Updating player totalGoals. Update team Wins, Losses, totalGoals.

6. Make use of transactions (commit & rollback)
- Using 'COMMIT; and START TRANSACTION;' when using Python to connect with mysql database would throw errors. We spoke in class, but all of the commits for this project was similar to Project 4 and 5, by simply using commit(). There was no need for rollback in this project because the transactions all were checked and had to follow a flow to be able to insert or update data.

7. Generate reports that can be exported (excel or csv format)
- When signed-in as team, there is an option in the home screen choices for 'Download Team Stats'. A csv file called 'download.csv' will be updated for whatever team chooses to download.

8. One query must perform an aggregation/group-by clause
- getGameGoals() and each_game()

9. One query must contain a subquery.
- each_game()

10. Two queries must involve joins across at least 3 tables
- getGoalsInfo() and goals()

11. Enforce referential integrality (PK/FK Constraints)
- Done

12. Include Database Views, Indexes
- Database View in view_all_games().
- Indexes in standings()

13. Use at least 5 entities
- 5 Entities (teams,player,coach,game,goal)


### Video Link: https://www.youtube.com/watch?v=ii2JTlmhOGE
