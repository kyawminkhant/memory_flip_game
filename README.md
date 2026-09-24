# Memory Flip Game

A desktop memory-matching game built with Python and Tkinter. Enter a username, flip cards to find all eight emoji pairs, and try to earn a place on the local top-10 leaderboard.

![Memory Flip Game logo](icon/logo.png)

## Features

- 4x4 shuffled emoji card board
- Username entry before play
- Turn counter and 0.1-second timer
- Encouragement messages and matching sound effects
- Persistent leaderboard, ranked by fastest time and then fewest turns
- Retry button for a freshly shuffled board

## Requirements

- Python 3.10 or newer
- Tkinter (included with most standard Python installations)
- Pygame

On some Linux distributions, install Tkinter first:

```bash
sudo apt install python3-tk
```

## Installation

```bash
git clone https://github.com/kyawminkhant/memory_flip_game.git
cd memory_flip_game
python -m pip install -r requirements.txt
```

## Run

```bash
python "Memory Flip Game.py"
```

## How to play

1. Type a username and select **Set Username** (or press Enter).
2. Flip two cards at a time to find matching emoji pairs.
3. Complete all eight pairs. Your time, turns, and username are saved to `leaderboards/mfg_leaderboard.txt`.
4. Select **Retry** whenever you want a newly shuffled board.

## Project structure

```text
Memory Flip Game.py       # Game application
requirements.txt          # Python dependency list
icon/                     # Application icon
images/                   # Image assets
sounds/                   # Sound effects
leaderboards/             # Local leaderboard storage
```

## License

Released under the [MIT License](LICENSE).
