import streamlit as st
from typing import List, Dict, Any, Optional

# === Mimi Style Display ===

def mimi_say(message: str, mood: str = "neutral") -> None:
    """Display Mimi's message with styled flair.

    Args:
        message: The text to display to the user.
        mood: One of {"neutral", "sassy", "proud", "annoyed", "sweet"} to style the message.

    Returns:
        None
    """
    colors = {
        "neutral": "#FFD700",   # gold
        "sassy": "#FF69B4",     # hot pink
        "proud": "#32CD32",     # lime green
        "annoyed": "#FF4500",   # orange red
        "sweet": "#87CEFA",     # light blue
    }
    emoji = {
        "neutral": "💬",
        "sassy": "😏",
        "proud": "💖",
        "annoyed": "😤",
        "sweet": "🥰",
    }
    color = colors.get(mood, "#FFD700")
    face = emoji.get(mood, "💬")
    html = f"""
    <div style='background-color:{color};
                padding:10px;
                border-radius:10px;
                color:white;
                font-weight:bold;
                font-size:15px;
                width:fit-content;
                margin:5px 0;'>
        {face} Mimi: {message}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# === Mimi Task Logger v0.1 ===
tasks: List[Dict[str, Any]] = []

def add_task(title: str) -> None:
    """Add a new task to Mimi's list.

    Args:
        title: The task title to add.

    Returns:
        None
    """
    task: Dict[str, Any] = {"title": title, "completed": False, "days_pending": 0}
    tasks.append(task)
    mimi_say(f"Added '{title}'. Now go do it.", mood="sassy")



# Task editing and deletion

def edit_task(old_title: str, new_title: str) -> bool:
    """Rename an existing task by title.

    Args:
        old_title: Current title of the task to rename (case-insensitive).
        new_title: New title to assign. Must be non-empty after trimming.

    Returns:
        True if the task was renamed; False otherwise.
    """
    original = old_title.strip()
    updated = " ".join(new_title.split()).strip()
    if not updated:
        mimi_say("Mimi refuses to save empty tasks. Try again.", mood="annoyed")
        return False

    # Prevent duplicate titles (case-insensitive)
    for t in tasks:
        if t["title"].lower() == updated.lower():
            if t["title"].lower() != original.lower():
                mimi_say(f"There's already a task called '{updated}'. Pick a unique name.", mood="annoyed")
                return False

    for t in tasks:
        if t["title"].lower() == original.lower():
            t["title"] = updated
            mimi_say(f"Renamed task to '{updated}'. Fancy.", mood="sassy")
            return True

    mimi_say(f"Mimi couldn't find a task called '{old_title}'.", mood="annoyed")
    return False


def delete_task(title: str) -> bool:
    """Delete a task by title.

    Args:
        title: Title of the task to delete (case-insensitive).

    Returns:
        True if the task was deleted; False otherwise.
    """
    target = title.strip().lower()
    for idx, t in enumerate(tasks):
        if t["title"].lower() == target:
            del tasks[idx]
            mimi_say(f"Deleted '{title}'. One less excuse.", mood="neutral")
            return True
    mimi_say(f"No task called '{title}' to delete.", mood="annoyed")
    return False

# === Step 4: Personality Mood System ===

mimi_mood: str = "neutral"
mood_points: int = 0  # goes up when you finish tasks, down when you ignore them

def update_mimi_mood(change: int) -> None:
    """Adjust Mimi's mood based on user behavior.

    Args:
        change: Positive values improve mood; negative values worsen mood.

    Returns:
        None
    """
    global mood_points, mimi_mood
    mood_points += change

    if mood_points >= 3:
        mimi_mood = "proud"
    elif mood_points <= -3:
        mimi_mood = "annoyed"
    else:
        mimi_mood = "neutral"

    mimi_say(f"Mimi’s mood is now: {mimi_mood.upper()} ({mood_points})", mood=mimi_mood)

# Modify complete_task and remind_user slightly:
def complete_task(title: str) -> None:
    """Mark a task completed by title (case-insensitive).

    Args:
        title: The title of the task to complete.

    Returns:
        None
    """
    for task in tasks:
        if task["title"].lower() == title.lower():
            if task["completed"]:
                mimi_say(f"'{title}' was already done! Mimi remembers. 🙄", mood="annoyed")
            else:
                task["completed"] = True
                mimi_say(f"Finally did '{title}'? Miracles happen! 😏✨", mood="proud")
                update_mimi_mood(+1)
            return
    mimi_say(f"Mimi checked everywhere — no task called '{title}'. 🤨", mood="annoyed")

def remind_user() -> None:
    """Nudge the user about all pending tasks and adjust mood accordingly.

    Returns:
        None
    """
    pending = [t for t in tasks if not t["completed"]]
    if not pending:
        mimi_say("All done?! Who even ARE you?! Mimi’s proud! 😭💖", mood="proud")
        update_mimi_mood(+2)
        return
    for task in pending:
        task["days_pending"] += 1
        if task["days_pending"] == 1:
            mimi_say(f"'{task['title']}' is still there. Just saying. 😒", mood="neutral")
            update_mimi_mood(-1)
        elif task["days_pending"] == 2:
            mimi_say(f"Mimi’s been patient, but '{task['title']}' is now collecting dust. 🕸️", mood="annoyed")
            update_mimi_mood(-2)
        else:
            mimi_say(f"Three days and '{task['title']}' is STILL not done?! Bold strategy. 😤", mood="annoyed")
            update_mimi_mood(-3)



# === Step 5: Mimi's Memory System ===
import json
import os

SAVE_FILE: str = "mimi_memory.json"

def save_mimi_data() -> None:
    """Save tasks and Mimi's mood to file.

    Returns:
        None
    """
    data = {
        "tasks": tasks,
        "mood_points": mood_points,
        "mimi_mood": mimi_mood
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)
    mimi_say("Mimi saved everything! Your chaos is now safe. 💾", mood="sweet")

def load_mimi_data() -> None:
    """Load tasks and Mimi's mood from file, if it exists.

    Returns:
        None
    """
    global tasks, mood_points, mimi_mood
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        tasks[:] = data.get("tasks", [])
        mood_points = data.get("mood_points", 0)
        mimi_mood = data.get("mimi_mood", "neutral")
        mimi_say(f"Mimi remembers everything 😏 Mood: {mimi_mood.upper()}, Tasks loaded: {len(tasks)}", mood=mimi_mood)
    else:
        mimi_say("Fresh start! Mimi’s ready to judge your productivity anew. 😌", mood="neutral")


# === Step 6: Mimi's Morning Check-In ===
from datetime import datetime

def mimi_check_in() -> None:
    """Display a contextual greeting based on time and current mood.

    Returns:
        None
    """
    hour = datetime.now().hour
    time_of_day = (
        "morning" if 5 <= hour < 12 else
        "afternoon" if 12 <= hour < 18 else
        "evening"
    )

    # Count pending tasks
    pending = [t for t in tasks if not t["completed"]]
    num_pending = len(pending)

    # Choose message tone based on Mimi's mood
    if mimi_mood == "proud":
        mimi_say(f"Good {time_of_day}! ☀️ You’ve been on fire lately 🔥 Only {num_pending} tasks today. Let’s keep that streak going!", mood="proud")

    elif mimi_mood == "annoyed":
        if num_pending > 3:
            mimi_say(f"Good {time_of_day}... 😤 You’ve got {num_pending} tasks waiting. Yesterday’s slacking? Unacceptable. Let’s fix it.", mood="annoyed")
        else:
            mimi_say(f"Good {time_of_day}! Mimi’s still slightly vexed 😒 but maybe today you’ll redeem yourself.", mood="annoyed")

    else:  # neutral
        if num_pending == 0:
            mimi_say(f"Good {time_of_day}! You’ve got a clean slate today. Mimi’s proud already! 💖", mood="sweet")
        elif num_pending <= 3:
            mimi_say(f"Good {time_of_day}! Light day — only {num_pending} things to crush. You’ve got this 💪", mood="sweet")
        else:
            mimi_say(f"Good {time_of_day}! You’ve got {num_pending} things waiting. Mimi’s watching 👀", mood="neutral")


# === Step 7: Adaptive Learning System ===
from datetime import datetime

# Mimi’s learning data
mimi_learning: Dict[str, Any] = {
    "morning_completions": 0,
    "afternoon_completions": 0,
    "evening_completions": 0,
    "ignored_tasks": {}
}

def record_task_completion_time() -> None:
    """Track the time of day when tasks are completed.

    Returns:
        None
    """
    hour = datetime.now().hour
    if 5 <= hour < 12:
        mimi_learning["morning_completions"] += 1
    elif 12 <= hour < 18:
        mimi_learning["afternoon_completions"] += 1
    else:
        mimi_learning["evening_completions"] += 1

def record_ignored_task(task_title: str) -> None:
    """Track how often a specific task is ignored.

    Args:
        task_title: The title of the ignored task.

    Returns:
        None
    """
    mimi_learning["ignored_tasks"][task_title] = (
        mimi_learning["ignored_tasks"].get(task_title, 0) + 1
    )

def analyze_patterns() -> None:
    """Analyze user behavior and give insights.

    Returns:
        None
    """
    morning = mimi_learning["morning_completions"]
    afternoon = mimi_learning["afternoon_completions"]
    evening = mimi_learning["evening_completions"]

    # Figure out the user’s best productivity period
    best_time = max(
        [("morning", morning), ("afternoon", afternoon), ("evening", evening)],
        key=lambda x: x[1]
    )[0]

    # Identify most-ignored task (if any)
    ignored = mimi_learning["ignored_tasks"]
    worst_task = max(ignored, key=ignored.get) if ignored else None

    # Give feedback
    if best_time == "morning":
        mimi_say("Mimi’s noticed you’re a morning superstar 🌅. Tackle big stuff early!", mood="sweet")
    elif best_time == "evening":
        mimi_say("You seem to thrive at night 🌙. Mimi’s adjusting her nagging schedule accordingly 😌", mood="neutral")
    else:
        mimi_say("Afternoons are your sweet spot ☀️. Mimi will chill before lunch next time 😏", mood="sweet")

    if worst_task:
        mimi_say(f"By the way... you *really* avoid '{worst_task}'. Want Mimi to help break it down next time? 😏", mood="annoyed")

def save_learning_data() -> None:
    """Save all Mimi data, including learning patterns, to disk.

    Returns:
        None
    """
    data = {
        "tasks": tasks,
        "mood_points": mood_points,
        "mimi_mood": mimi_mood,
        "mimi_learning": mimi_learning
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)
    mimi_say("Mimi updated her brain with your patterns 🧠💾", mood="sweet")

def load_learning_data() -> None:
    """Load saved tasks, mood, and learning data safely from disk.

    Returns:
        None
    """
    global tasks, mood_points, mimi_mood, mimi_learning

    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                content = f.read().strip()
                if not content:
                    raise ValueError("Empty file")
                data = json.loads(content)
        except (json.JSONDecodeError, ValueError):
            mimi_say("Mimi found a corrupted memory file 😢 — starting fresh!", mood="annoyed")
            data = {}
        except Exception as e:
            mimi_say(f"Unexpected error while loading memory: {e}", mood="annoyed")
            data = {}
    else:
        data = {}
        mimi_say("New session! Mimi’s ready to start learning your habits 👀", mood="neutral")

    # Restore defaults or loaded values
    tasks[:] = data.get("tasks", [])
    mood_points = data.get("mood_points", 0)
    mimi_mood = data.get("mimi_mood", "neutral")
    mimi_learning = data.get("mimi_learning", mimi_learning)


# === Step 8: Smarter Mimi Actions ===
import random

def smart_remind_user() -> None:
    """Remind the user based on learned patterns (time of day and avoided tasks).

    Returns:
        None
    """
    pending = [t for t in tasks if not t["completed"]]
    if not pending:
        mimi_say("No tasks to bug you about 😌 Mimi’s impressed.", mood="proud")
        update_mimi_mood(+1)
        return

    hour = datetime.now().hour
    night_person = mimi_learning["evening_completions"] > (mimi_learning["morning_completions"] + mimi_learning["afternoon_completions"])

    for task in pending:
        title = task["title"]
        days = task["days_pending"]
        ignored_count = mimi_learning["ignored_tasks"].get(title, 0)

        # --- Decide reminder timing & tone ---
        if night_person and hour < 15:
            # Night worker -> gentle before evening
            mimi_say(f"Early ping, but Mimi knows you work best later 😴. Just a heads-up about '{title}'.", mood="sweet")
        elif not night_person and hour >= 18:
            # Morning person -> gentle in evening
            mimi_say(f"It’s getting late 🌙. Maybe leave '{title}' for tomorrow when you’re sharper.", mood="neutral")
        else:
            # Normal reminder
            mood = "annoyed" if ignored_count > 2 or days > 1 else "neutral"
            lines = [
                f"‘{title}’ is giving *professional procrastination* vibes 😏",
                f"You’ve dodged ‘{title}’ {ignored_count+1} times… Mimi’s counting 👀",
                f"Still no progress on ‘{title}’? Mimi’s gonna start charging rent 🏚️"
            ]
            mimi_say(random.choice(lines), mood=mood)
        
        # If a task is frequently ignored → break it down
        if ignored_count >= 3 and " → " not in title:
            subtasks = [
                f"{title} → Step 1",
                f"{title} → Step 2",
                f"{title} → Step 3"
            ]
            mimi_say(f"Mimi’s helping you out. Breaking '{title}' into smaller steps 💡", mood="sweet")
            for s in subtasks:
                tasks.append({"title": s, "completed": False, "days_pending": 0})
            record_ignored_task(title)  # log that Mimi intervened

if __name__ == "__main__":
    load_learning_data()
    mimi_check_in()

