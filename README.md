# HealPointsSystem
This application is built to replicate the Heal Point system used by the Maine Principals' Association to determine which high school teams make the playoffs for a given sport as well as their seedings.
Team rankings are calculated based on athletic strength rather than purely on team win-loss records.
The system, along with how its ratings are calculated, can be found here: https://www.mpa.cc/page/3174

The program used here utilizes both Python and MySQL. Team scores are passed to a MySQL database through Python, then the calculations for a team's indecies are made through Python as it pulls data back from the database.
In its current state, the application simply calculates Heal Point ratings based on input data.
Future updates are intended to include support for data entry from .csv files and a feature that allows for user calculations of hypothetical match results.
