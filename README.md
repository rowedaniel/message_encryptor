# Simple project for locking a message behind some encryption codes

## Background 
I love making crossword puzzles for friends, but I always run into the same two issues.
First, My crosswords are usually personalized, and thus simple enough that there could ponentially be multiple answers for each clue.
I need a way of signalling to friends when they get an answer right, so they don't keep trying.
Second, I frequently want some ultimate goal or message at the end as a reward for once they finish.

With this project, I hope to remedy these issues.

## Requirements
I used python 3.11 for this project, with poetry for managing 

## Usage

This project is used to generate a supplementary HTML file which goes along a crossword puzzle.
To use it, you specify a .yml config file listing a final message, the different keys (typically corresponding to 1-across, 3-down, etc. on the crossword), and a mask for each key that determines how it is ultimately applied to the final message.
With this config file, you can generate the html file using the following syntax:

```
python generate.py examples/crossword3.yml crossword3.html
```

There are also several utility functions provided in ``make_keys.py`` and ``make_keymap.py`` for generating random keys and generating key masks.
