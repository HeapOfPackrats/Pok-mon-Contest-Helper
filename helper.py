''' 
Currently parses specific rock-paper-scizzor posts on 
my /r/pokemontrades posts for a very specific combination 
and number of plays.
'''

import random
import re
import string
import praw

# https://stackoverflow.com/a/34294398
# used to remove punctuation via string.translate()
translator = str.maketrans('', '', string.punctuation)

# rock-paper-scissors string regex
rps = "[rpsRPS][rpsRPS][rpsRPS][rpsRPS][rpsRPS][rpsRPS][rpsRPS]"

# initialize reddit and submission objects
reddit = praw.Reddit("bot1")
submission = reddit.submission(url="https://www.reddit.com/r/pokemontrades/comments/6vdj68/hoardofpackrats_vs_rpokemontrades/")

# count and store all entries (root-level comments)
counter = 0
entries = []

for top_level_comment in submission.comments:
    top_level_comment.body = top_level_comment.body.translate(translator)
    parent = top_level_comment.body.split()
    entry = {}

    for word in parent:
        if re.match(rps, word):
            entry.update(plays=word)
        elif word.isnumeric():
            entry.update(rng=word)

    entry.update(redditor=top_level_comment.author.name)
    entries.append(entry)

    counter += 1

# find winners
winners = []
highest = 0

for item in entries:
    wins = 0

    if "plays" not in item:
        continue
    if item["plays"][0] == "R" or item["plays"][0] == "r":
        wins += 1
    if item["plays"][1] == "S" or item["plays"][1] == "s":
        wins += 1
    if item["plays"][2] == "P" or item["plays"][2] == "p":
        wins += 1
    if item["plays"][3] == "P" or item["plays"][3] == "p":
        wins += 1
    if item["plays"][4] == "S" or item["plays"][4] == "s":
        wins += 1
    if item["plays"][5] == "P" or item["plays"][5] == "p":
        wins += 1
    if item["plays"][6] == "R" or item["plays"][6] == "r":
        wins += 1

    if wins > highest:
        highest = wins
        winners.clear()
        winners.append({"redditor":item["redditor"], "plays":item["plays"], "rng":item["rng"], "wins":wins})
    elif wins == highest:
        winners.append({"redditor":item["redditor"], "plays":item["plays"], "rng":item["rng"], "wins":wins})

for winner in winners:
    print(winner)

print("RNG: " + str(random.randint(1, 2873)))

print("#parent comments: " + str(counter))
