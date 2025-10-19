# Mimi Task Logger

A sassy, memory-driven task logger built with Python + Streamlit.

Status: Prototype (v0.1). Focused on a playful UX with a simple, local JSON memory. Suitable for single-user, local use.

What is it?
- A lightweight Streamlit app where “Mimi” helps you add and complete tasks with a sassy tone.
- Persists tasks and Mimi’s mood to a local file (mimi_memory.json).
- Provides reminders, a morning check-in, and a basic adaptive “learning” system that nudges you when you ignore tasks.

Key features (as implemented)
- Add tasks and mark them complete
- Mimi’s mood system that reacts to your behavior (proud/neutral/annoyed)
- Reminders that increase pressure if tasks linger
- Smart Reminder that uses simple patterns to choose when/how to nudge
- Morning Check-In with contextual messaging
- Local persistence to mimi_memory.json

Project structure
- app.py — Streamlit UI and interactions
- mimi_brain.py — Core logic: tasks, mood, reminders, memory, learning
- mimi_memory.json — Local data store created at runtime
- assets/mimi_icon.png — App icon
- requirements.txt — Python dependencies
- RunMimi.bat — Windows helper to start the app

Requirements
- Python 3.9+
- See requirements.txt (streamlit, streamlit-extras, ipython)

How to run
1) Create/activate a virtual environment (recommended)
   - macOS/Linux: python3 -m venv .venv && source .venv/bin/activate
   - Windows (PowerShell): py -m venv .venv; .venv\\Scripts\\Activate.ps1
2) Install dependencies: pip install -r requirements.txt
3) Start the app: streamlit run app.py
   - Or on Windows, double-click RunMimi.bat

Data and persistence
- The app saves tasks, mood points, and Mimi’s current mood to mimi_memory.json in the project root.
- This is a simple, local, single-user storage. Deleting the file resets the app’s memory.

Credits:

Contributors:
- Niyi Adebayo (https://github.com/chinesefirewall)
