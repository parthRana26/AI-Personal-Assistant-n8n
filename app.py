import streamlit as st
import requests

WEBHOOK_URL = "https://parthrana.app.n8n.cloud/webhook-test/c625fd91-6217-484a-a323-4aa715e6f14f"

st.set_page_config(
    page_title="Parth Personal Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Parth Personal Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("Ask me anything...")

if prompt:
    # Display user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        payload = {
            "question": prompt
        }

        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            timeout=60
        )
        
        print("Status code:", response.status_code)

        if response.status_code == 200:

            data = response.json()

            if isinstance(data, dict):
                answer = data.get("answer") or data.get("output") or str(data)

            elif isinstance(data, list):
                if len(data) > 0:
                    answer = data[0].get("output", str(data[0]))
                else:
                    answer = "No response"

            else:
                answer = str(data)

        else:
            answer = f"Error: {response.status_code}"

    except Exception as e:
        answer = f"Error: {str(e)}"

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )