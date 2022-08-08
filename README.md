# All league scenarios

A small python programm to calculate all possible outcomes (standings of the teams) of a league. Currently implemented are the esport leagues LEC and LCS.

## Warning
Be careful when trying to process high amount of probabilities. My system crashed around 2^23 possibilities (with 16GB RAM).

Also I forgot to add a file so some unittests dont find a file and fail :3.
## Setup
Clone the repository, cd in to the repository and install the requirements with:

```
pip install -r requirements.txt
```

Now you are ready to run the program.

## Run it
```
python3 main.py
```

This will create following files in src/app/files:
- [leaguename]_matches.json
- [leaguename]_output.md

The matchdata json file will be only downloaded when missing!

The output files content is the result of the program run.

Run the unittests:
```
python3 -m unittest
```
## Configuration
### Get up to date data
To get data of the current split to get informations about:
- current wins of the teams
- upcomming games
- wins in second half of the split

you need to update a link in src/app/process_data/league.py. By setting the "gamepedia_url" attribute to the fandom page of the current split, like here for the Summer Split 2022 of the LEC:
```
gamepedia_url = 'https://lol.fandom.com/wiki/LEC/2022_Season/Summer_Season'
```
(Yes if they change the html, then its doomed)

### Set up your own scenario
You want to know what happens on what places a team can finish if they lose their next game?
Then you should have a look at the file: src/app/files/[league]_matches.json. Downloaded after running main.py!

In this file are all games of a split. By manipulating the games in this file, you can calculate where teams can end up for your own scenario.

### LCS
In main.py you can run the program for LCS. By replacing:
```
League = LEC
```

with 
```
League = LCS
```

Keep in mind to set the correct number of LCS playoff teams in the LCS class within src/app/process_data/league.py. For example a LCS split with 6 playoff teams:
```
playoff_teams = 6
```