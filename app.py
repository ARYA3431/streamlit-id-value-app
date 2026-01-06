import streamlit as st
import sqlite3

# ---------------- DATABASE ----------------
# /tmp is required for Streamlit Cloud
conn = sqlite3.connect("/tmp/master.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS master (
    id INTEGER PRIMARY KEY,
    current TEXT,
    previous TEXT
)
""")
conn.commit()

# Default initialization (only once)
defaults = {
    1:'A', 2:'B', 3:'C', 4:'D', 5:'E',
    6:'F', 7:'G', 8:'H', 9:'I'
}

for k, v in defaults.items():
    cur.execute("""
        INSERT OR IGNORE INTO master (id, current, previous)
        VALUES (?, ?, NULL)
    """, (k, v))
conn.commit()

# ---------------- UI ----------------
st.title("ID Value Management App")

id_input = st.number_input(
    "Select ID (1–9)",
    min_value=1,
    max_value=9,
    step=1
)

cur.execute(
    "SELECT current, previous FROM master WHERE id=?",
    (id_input,)
)
row = cur.fetchone()

if row:
    current_val, previous_val = row

    st.info(f"Current Value: {current_val}")
    st.warning(f"Previous Value: {previous_val if previous_val else '-'}")

    updated_val = st.text_input("Enter Updated Value (A to ZZ)")

    if st.button("Save Update"):
        if updated_val.strip() == "":
            st.error("Updated value cannot be empty")
        else:
            cur.execute("""
                UPDATE master
                SET previous = current,
                    current = ?
                WHERE id = ?
            """, (updated_val, id_input))
            conn.commit()

           st.success("Value updated successfully")
           st.rerun()

