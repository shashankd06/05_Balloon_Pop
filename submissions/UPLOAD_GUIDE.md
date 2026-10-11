# Upload the Balloon Pop repository

This folder follows the reference project's layout: `main.py` and `game/`
at the root, gameplay recordings in `videos/`, and documentation in `submissions/`.
All source and evidence here belong to the Balloon Pop work.

## Use this as a standalone personal repository

1. Extract `Balloon_Pop_Repository.zip` and open its `05_balloon_pop` folder.
2. Read `README.md`; run the game with the commands there.
3. Create your own empty GitHub repository, or open your existing Balloon Pop
   fork. Use that repository's URL, not the supplied number-guess reference.
4. Use **Add file > Upload files** and upload the contents of `05_balloon_pop`
   so that `README.md`, `main.py`, `game/`, `videos/`, and `submissions/` appear
   directly at the repository root. Upload the extracted contents, not only the ZIP.
5. Commit the upload. Do not upload `__pycache__`, temporary files, virtual
   environments, or downloaded dependencies.
6. Complete `submissions/Submission_Links.md` with your personal repository URL
   and an accessible chat share link. Open the links in a private browser window
   to verify that your instructor can use them.
7. If your instructor wants a links PDF like the reference, export the completed
   links document as `submissions/prompt_and_repo.pdf` and upload it too.

If you already have a local clone of your own repository, copy these files into
it and run, from the clone:

```text
git add README.md main.py requirements.txt .gitignore game tests videos submissions
git commit -m "Complete Lab 4 Balloon Pop game and deliverables"
git push
```

No personal repository has been changed by the assistant. Your destination URL
was not provided. Do not open a pull request to the instructor's SETAPESU26 repo.

## If your course uses one repository for all labs

The lab handout says to place the submission under `Lab-4` in your personal lab
repository. Copy the contents of `05_balloon_pop` into that `Lab-4` folder:

```text
your-lab-repository/
└── Lab-4/
    ├── README.md
    ├── main.py
    ├── requirements.txt
    ├── game/
    ├── tests/
    ├── videos/
    └── submissions/
```

Use your course's required destination if it differs from the reference's
standalone game repository. The layout reference does not change the assignment.

## Chat history and sharing

The included PDF is the original conversation snapshot. To include the entire
finished exchange, export the conversation after this reply if the app offers
that option. Otherwise copy the visible messages into Word/Google Docs and
export a PDF, replacing `submissions/Chat_History.pdf`.

Use the app's Share control, if available, for the chat page link. Sharing
publishes a snapshot accessible to people with the link. If Share is unavailable,
ask the instructor whether the full PDF can substitute; do not invent a URL.

## If you must record yourself playing

The included videos use actual game frames with automated click inputs. The
short after video is an explicitly labeled highlights edit. It is not a
continuous 10-second personal desktop recording.

1. Extract the separate `Starter_Code.zip` from the earlier deliverables, or
   use the supplied local starter shortcut on this computer.
2. Run the original game. Record at least 10 seconds with a screen recorder and
   the pointer visible: show an inside-circle edge click failing, then a center
   click working. Save the result as `videos/before.mp4`.
3. Run this updated game's `main.py`. Record off-center clicks, the different
   balloon effects, the lives counter, and the countdown. Save a 10-second clip
   as `videos/after.mp4` if a short recording is required.
4. Keep a longer recording to show the timer ending, final score, and restart.
   A 30-second countdown cannot be shown from start to finish in an unedited
   10-second real-time clip. Include `videos/after_full.mp4` for that evidence.
5. On Windows, Xbox Game Bar (Win+Alt+R if available) or Snipping Tool's Record
   option can capture the game. Trim/export the recordings as MP4 as needed.

The original and updated local game shortcuts in the earlier outputs folder
use the tested runtime and dependencies already installed in this workspace.
For a portable installation, use Python 3.12 and install `requirements.txt`.
