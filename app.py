import streamlit as st
from mimi_brain import (
    add_task, complete_task, remind_user, smart_remind_user,
    load_learning_data, save_learning_data, mimi_check_in, tasks
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
        cols = st.columns([0.1, 0.7, 0.2])
        done = cols[0].checkbox("", value=t["completed"], key=t["title"])
        cols[1].write(f"**{t['title']}**")
        if done and not t["completed"]:
            complete_task(t["title"])
            save_learning_data()
            st.balloons()
        if cols[2].button("🧠 Remind", key=f"r_{t['title']}"):
            remind_user()
else:
    st.info("Mimi: no tasks? suspiciously confident of you 😒")

st.divider()

# --- Smart Reminders & Save ---
if st.button("😤 Smart Reminder"):
    smart_remind_user()
    save_learning_data()

st.caption("© 2025 Mimi AI — A sassy productivity companion by Mosunmola")
