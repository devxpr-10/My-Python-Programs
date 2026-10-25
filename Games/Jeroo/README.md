# Jeroo

A Pygame-based collection game where you guide Jeroo to collect flowers and place them at designated points while avoiding obstacles before time runs out.

## Objective

- Collect all flowers scattered on the grid
- Place them at the marked target points
- Avoid the nets (enemies)
- Complete the task before time expires

## Gameplay

- Each level has 4-8 flowers to collect and 15-25 moving nets to avoid
- Time limit: 14-18 seconds per round
- Collect a flower by moving Jeroo over it
- Place flowers at the target points (marked locations)
- If time runs out or you hit a net, it's game over

## Controls

| Key | Action |
|-----|--------|
| **W** or **↑** | Move Up |
| **S** or **↓** | Move Down |
| **A** or **←** | Move Left |
| **D** or **→** | Move Right |
| **ESC** | Pause/Resume |
| **R** | Restart Game |
| **Q** | Quit (when paused) |

## Features

- Real-time grid-based movement
- Collision detection for flowers, targets, and enemies
- Sound effects for interactions
- Background music
- Pause/Resume functionality
- Randomized gameplay each round

## Installation

To directly play without touching the code just download 'jeroo.exe' otherwise,

Requires Python 3.x and Pygame:

```bash
pip install pygame
```

Then run:

```bash
python jeroo.py
```

## Project Structure

```
Jeroo/
├── jeroo.py          # Main game file
├── assets/
│   ├── imgs/         # Game sprites
│   └── auds/         # Sound effects
└── README.md
```

## Requirements

- Python 3.6+
- Pygame
