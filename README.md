# Balloon Pop - Lab 4

Personal repository: [shashankd06/05_Balloon_Pop](https://github.com/shashankd06/05_Balloon_Pop).

SRN: PES1UG24CS433
NAME: SHASHANK D
SECTION: H

A Pygame game where you click falling balloons before they leave the screen.
All four assigned tasks are completed: circle-aware clicks, three balloon types,
three lives, and a 30-second round with final score and restart.

## Completed tasks

| Task | Implementation | Evidence |
| --- | --- | --- |
| Fix click detection | Clicks anywhere inside the circle, including its edge, pop the balloon. Overlaps select the topmost balloon. | Before and after videos; circle-boundary checks |
| Add balloon types | Blue normal: +10; gold bonus: +30; red penalty: -10. Symbols also distinguish the types. | After video; scoring checks for all three types |
| Add lives/misses | Start with 3 lives. Each unpopped balloon loses one life when its entire circle exits the bottom. Popping any type preserves lives. | After video; miss and pop checks |
| Add timed rounds | Start with 30 seconds. Time or zero lives ends gameplay and freezes the final score. Restart resets everything. | Full after video; timer, end-state, and restart checks |

## Getting started

Tested on Windows with Python 3.12.14 and Pygame 2.6.1.
Python 3.10+ is required by the assignment. Python 3.12 is a tested choice
if Pygame installation fails with a newer interpreter.

Open a terminal in this repository folder:

```bash
python -m pip install -r requirements.txt
python main.py
```

For an isolated installation on Windows:

```text
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python main.py
```

## Controls and scoring

- **Left-click:** pop a balloon.
- **R / Enter / Play again:** start a new round after a round ends.
- **Escape / window close:** quit.

| Balloon | Color / symbol | Points |
| --- | --- | --- |
| Normal | Blue / + | +10 |
| Bonus | Gold / * | +30 |
| Penalty | Red / - | -10 |

The score can go below zero. Popping any balloon never costs a life.
Every missed type costs one life. A round ends when time reaches zero or lives
reach zero. The game shows the final score and a restart button.

## Repository structure

```text
05_balloon_pop/
├── README.md
├── main.py
├── requirements.txt
├── .gitignore
├── game/
│   ├── __init__.py
│   ├── balloon.py
│   ├── click_detection.py
│   ├── game_engine.py
│   └── renderer.py
├── tests/
│   └── test_game.py
├── videos/
│   ├── before.mp4
│   ├── after.mp4
│   └── after_full.mp4
└── submissions/
    ├── Chat_History.pdf
    ├── Submission_Links.md
    ├── Verification_Report.txt
    └── UPLOAD_GUIDE.md
```

The game entry point and modules sit at the repository root. Videos and
submission documents have their own folders, following the organization of
the supplied reference repository.

## Gameplay evidence

- [Before changes - 10 seconds](videos/before.mp4): the original game misses
  clicks inside the circle near the edge, but accepts center clicks.
- [After changes - 10-second highlights](videos/after.mp4): successful
  off-center hits, type scores, missed lives, final score, and restart.
- [After changes - continuous capture, about 38 seconds](videos/after_full.mp4):
  the full countdown, timer ending, restart, and an early ending from lost lives.

These MP4s contain actual game frames with scripted click inputs. They are
automated game captures. The short after video is an edit of excerpts from the
continuous capture, and its captions show the original capture timestamps.
Both short videos have exactly 300 frames at 30 fps: 10.00 seconds each.
See the [upload guide](submissions/UPLOAD_GUIDE.md) if personal screen recordings
are required instead.

## Chat and submission documents

- [Chat history PDF](submissions/Chat_History.pdf): visible conversation snapshot
  through the original packaging update; later messages are not included.
- [Chat and personal repository links](submissions/Submission_Links.md): add
  the personal repository link is provided; add the chat share link before submission.
- [Verification report](submissions/Verification_Report.txt): tests and capture
  metadata for this game.
- [Upload guide](submissions/UPLOAD_GUIDE.md): how to complete the remaining
  links and upload to your own repository or a `Lab-4` folder.

## Verification

From the repository root:

```bash
python -m unittest discover -s tests -v
```

All 18 checks pass, covering circular hit boundaries, overlaps, score effects,
all missed types, pop/life separation, timer display, both endings, frozen
results, spawn behavior, complete reset, and the application event loop.

## Source and layout reference

The game began from [SETAPESU26/05_balloon_pop](https://github.com/SETAPESU26/05_balloon_pop),
commit `c9a5e46d64da59c83365b8bc8cafed2c89ebbe9e`.

[Ritu0713/60_number_guess](https://github.com/Ritu0713/60_number_guess) was used
only as a reference for the repository layout: root game files, `videos/`, and
`submissions/`. Its game code, videos, personal links, and submission files were
not copied into this repository.
