import streamlit as st
import sqlite3
from openai import OpenAI

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

def process_text_with_api(api_key, text):
    client = OpenAI(api_key=api_key)
    try:
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=text + "\n" ,
            temperature=0.7,
            max_tokens=2650,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"An error occurred with the API: {e}")
        return None

def get_api_key():
    api_key = st.secrets["API-KEY"]
    if not api_key:
        raise ValueError("No OpenAI API key found. Please set the OPENAI_API_KEY environment variable.")
    return api_key

def main():
    api_key = get_api_key()
    st.title("Chat App")

    # Get user name
    user_name = st.text_input("Enter your name:")

    # Get message input
    message = st.text_input("Type your message:")

    # Get code input
    code_message = st.text_area("Paste your code here:", height=200)

    # Get input for ChatGPT
    chatgpt_message = st.text_area("Type your message:", height=200)

    # Button to send message
    if st.button("Send"):
        if message:
            # Add text message to the database
            insert_message(user_name, message, "text")
        if code_message:
            # Add code message to the database
            insert_message(user_name, code_message, "code")
        if chatgpt_message:
            # Process message with ChatGPT API
            bot_response = process_text_with_api(api_key, chatgpt_message)
            if bot_response:
                st.write(f"ChatGPT: {bot_response}")

    # Display all messages
    messages = get_all_messages()
    if messages:
        st.header("Chat History")
        for msg in messages:
            if msg[2] == "text":
                st.write(f"{msg[0]}: {msg[1]}")
            elif msg[2] == "code":
                st.code(f"{msg[0]} (code snippet):\n{msg[1]}")

    # Button to delete messages
    if st.button("Delete Messages"):
        c.execute("DELETE FROM messages")
        conn.commit()
        st.write("All messages deleted.")

if __name__ == "__main__":
    main()
