import streamlit as st
from openai import OpenAI

# Танзимоти саҳифаи веб
st.set_page_config(
    page_title="Чат-боти Замонавӣ (AI)", page_icon="🤖", layout="centered"
)

st.title("🤖 Чат-боти шахсии ман (AI)")
st.write(
    "Саволи худро нависед, то зеҳни сунъӣ ба шумо бо тарзи замонавӣ ҷавоб"
    " диҳад!"
)

# Гирифтани калиди OpenAI API аз тарафи корбар ё муҳити барнома
api_key = st.text_input(
    "Калиди OpenAI API-ро ворид кунед (API Key):", type="password"
)

if not api_key:
    st.info(
        "Лутфан барои кор кардани бот калиди API-и худро ворид кунед."
        " (OpenAI API Key)"
    )
else:
    # Пайвастшавӣ ба OpenAI
    client = OpenAI(api_key=api_key)

    # Интихоби модел
    model_name = "gpt-4o-mini"

    # Нигоҳ доштани таърихи чат дар хотираи сессия
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Намоиши паёмҳои қаблӣ дар экран
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Қуттии навиштани савол дар поёни экран
    if prompt := st.chat_input("Чӣ мехоҳед пурсед?"):
        # Илова кардани паёми корбар ба таърих
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Гирифтани ҷавоб аз зеҳни сунъӣ
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                )
                assistant_response = response.choices[0].message.content
                message_placeholder.markdown(assistant_response)

                # Илова кардани ҷавоби бот ба таърих
                st.session_state.messages.append(
                    {"role": "assistant", "content": assistant_response}
                )
            except Exception as e:
                st.error(f"Хатогӣ рӯй дод: {e}")
