This application is built to replicate the Heal Point system used by the Maine Principals' Association to determine which high school teams make the playoffs for a given sport as well as to determine their seedings. Team rankings are calculated based on athletic strength rather than purely on team win-loss records. The methods of calculation can be found here: https://www.mpa.cc/page/3174

For reference, only the mathematics from the website listed above were used and no code was taken from it.

The program used here utilizes both Python and MySQL. Team scores are passed to a MySQL database through Python, then the calculations for a team's indices are made through Python as it pulls data back from the database. Match/game results are entered into the MySQL database through Python, the full list of match/game results is passed from the database into Python to calculate teams' preliminary indices (team values) which are then stored in the database. The preliminary indices are then pulled from the database to calculate the tournament indices (playoff rating value) which are also stored in the database.

In its current state, the application calculates Heal Point ratings based on input data. Data can be input manually through one Python script or can be imported via .csv file through the use of a second script. School/team name, class, and region can now be added through a .csv file as well.

Future planned updates include a feature that allows for user calculations of ratings based on hypothetical additional game/match results and a frontend that allows the database to be viewed directly in Python.
