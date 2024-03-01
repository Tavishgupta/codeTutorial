import streamlit as st
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('chat1.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS messages
             (user text, message text, message_type text)''')
conn.commit()

def insert_message(user, message, message_type):
    c.execute("INSERT INTO messages (user, message, message_type) VALUES (?, ?, ?)", (user, message, message_type))
    conn.commit()

def get_all_messages():
    c.execute("SELECT * FROM messages")
    return c.fetchall()

def main():
    st.title("Chat App")

    # Get user name
    user_name = st.text_input("Enter your name:")

    # Get message input
    message = st.text_input("Type your message:")

    # Get code input
    code_message = st.text_area("Paste your code here:", height=200)

    # Button to send message
    if st.button("Send"):
        if message:
            # Add text message to the database
            insert_message(user_name, message, "text")
        if code_message:
            # Add code message to the database
            insert_message(user_name, code_message, "code")

    # Display all messages
    messages = get_all_messages()
    if messages:
        st.header("Chat History")
        for msg in messages:
            if msg[2] == "text":
                st.write(f"{msg[0]}: {msg[1]}")
            elif msg[2] == "code":
                st.code(f"{msg[0]} (code snippet):\n{msg[1]}")


if __name__ == "__main__":
    main()
