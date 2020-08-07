# All league scenarios

A small python programm to calculate all possible outcomes (standings of the teams) of a league. Currently implemented are the esport leagues LEC and LCS.

## Warning
Be careful when trying to process high amount of probabilities. My system crashed around 2^23 possibilities.

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
- leaguename_matches.json
- leaguename_output.md

The matchdata json file will be only downloaded when missing!

The output file will be the result of the program.

Run the unittests:
```
python3 -m unittest
```