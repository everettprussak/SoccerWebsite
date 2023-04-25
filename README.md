# FIFA 2022 Soccer Website Database

# By: Everett Prussak and Aidan Lewis-Grenz

## How to run:

### python3 db_operations.py

### python3 application.py

###

## Issues we had:

### There are 32 teams with 26 players per team, that would take too long to hard code so we went with the top 10 teams.

## Special cases:

###

## Project Details

1. Print/display records from your database/tables.
- Records are displayed on html

2. Query for data/results with various parameters/filters
- A query for top ten goal scorers. A query for team standings.

3. Create a new record
- Add a player to roster. Create a game. Add a goal scorer in a game.

4. Delete records (soft delete function would be ideal)
- Delete game

5. Update records
- Updating player totalGoals. Update team Wins, Losses, totalGoals.

6. Make use of transactions (commit & rollback)
- Need to do

7. Generate reports that can be exported (excel or csv format)
- Need to do

8. One query must perform an aggregation/group-by clause
- getGameGoals() and each_game()

9. One query must contain a subquery.
- each_game()?

10. Two queries must involve joins across at least 3 tables
- getGoalsInfo() and goals()

11. Enforce referential integrality (PK/FK Constraints)
- Done

12. Include Database Views, Indexes
- Database View in view_all_games().
- Indexes: need to do.

13. Use at least 5 entities
- 5 Entities (teams,player,coach,game,goal)
