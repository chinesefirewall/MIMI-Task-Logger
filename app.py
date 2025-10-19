import streamlit as st
from mimi_brain import (
    add_task, complete_task, remind_user, smart_remind_user,
    load_learning_data, save_learning_data, mimi_check_in, tasks,
    edit_task, delete_task
)

# --- Streamlit Page Config ---
st.set_page_config(page_title="Mimi Task Logger", page_icon="😏", layout="centered")

st.title("😏 Mimi Task Logger")
st.write("Your sarcastic but caring productivity buddy. 💅🏽")

# --- Load Mimi's memory and learning ---
load_learning_data()

# --- Mimi Check-In ---
if st.button("☀️ Mimi Check-In"):
    mimi_check_in()

st.divider()

# --- Add a New Task ---
st.subheader("Add a New Task")
new_task = st.text_input("What do you need to do?")

if st.button("➕ Add Task"):
    if new_task.strip():
        add_task(new_task)
        save_learning_data()
        st.success(f"Mimi added: **{new_task}**")
    else:
        st.warning("Mimi: add something real please 😏")

st.divider()

# --- Show All Tasks ---
st.subheader("Your Tasks")

if tasks:
    for t in tasks:
        cols = st.columns([0.1, 0.45, 0.25, 0.1, 0.1])
        done = cols[0].checkbox("", value=t["completed"], key=f"cb_{t['title']}")
        cols[1].write(f"**{t['title']}**")

        # Inline edit input and save
        new_title = cols[2].text_input("Edit title", value=t["title"], key=f"edit_{t['title']}")
        if cols[2].button("Save", key=f"save_{t['title']}"):
            if new_title.strip() and new_title.strip() != t["title"].strip():
                if edit_task(t["title"], new_title.strip()):
                    save_learning_data()
                    st.success(f"Renamed to: **{new_title.strip()}**")
            else:
                st.warning("Provide a new, non-empty title to save.")

        # Delete button
        if cols[3].button("🗑️", key=f"del_{t['title']}"):
            if delete_task(t["title"]):
                save_learning_data()
                st.warning(f"Deleted: **{t['title']}**")
                st.experimental_rerun()

        # Remind button
        if cols[4].button("🧠", key=f"r_{t['title']}"):
            remind_user()

        if done and not t["completed"]:
            complete_task(t["title"])
            save_learning_data()
            st.balloons()
else:
    st.info("Mimi: no tasks? suspiciously confident of you 😒")

st.divider()

# --- Smart Reminders & Save ---
if st.button("😤 Smart Reminder"):
    smart_remind_user()
    save_learning_data()

st.caption("© 2025 Mimi AI — A sassy productivity companion by Mosunmola")
