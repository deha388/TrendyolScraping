import streamlit as st
import requests
from pathlib import Path


def fetch(session, url, user_input):

    try:
        message = {"url": user_input}
        data=session.post(url, json=message)
        return data
    except Exception as e:
        print(e)


def main():
    filename = ""
    st.set_page_config(page_title="Example App", page_icon="🤖")
    st.title("Get Product URL")
    session = requests.Session()
    with st.form("my_form"):
        user_input = st.text_input("URL", key="index")
        submitted = st.form_submit_button("Submit")
        if submitted:
            if len(user_input) > 0:
                try:
                    data=fetch(session, f"http://127.0.0.1:8000/data", user_input)
                    if data=="error":
                        st.error('Input is not a URL', icon="⚠")
                    else:
                        st.write("Successfully added")
                except Exception as e:
                    print(e)
            else:
                st.error('URL can not be empty', icon="⚠")

if __name__ == '__main__':
    main()