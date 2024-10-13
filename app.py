import streamlit as st
import os

from prompt import general_system_prompt, link_reader_system, link_reader_prompt, translation_system_prompt
from chat import Chat, modelList

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")

pass_word: str = os.getenv("PASSWORD")

if "login" not in st.session_state:
    st.session_state.login = False

if "sys" not in st.session_state:
    st.session_state.sys = ""
if "msg" not in st.session_state:
    st.session_state.msg = []
if "mem" not in st.session_state:
    st.session_state.mem = []

if "token" not in st.session_state:
    st.session_state.token = 4096
if "temp" not in st.session_state:
    st.session_state.temp = 0.70
if "topp" not in st.session_state:
    st.session_state.topp = 0.70
if "freq" not in st.session_state:
    st.session_state.freq = 0.00
if "pres" not in st.session_state:
    st.session_state.pres = 0.00

if "retry_switch" not in st.session_state:
    st.session_state.retry_switch = False
if not st.session_state.mem or st.session_state.mem[-1]["role"] != "assistant":
    st.session_state.retry_switch = True
elif st.session_state.mem and st.session_state.mem[-1]["role"] == "assistant":
    st.session_state.retry_switch = False
if "retry_state" not in st.session_state:
    st.session_state.retry_state = False

with st.sidebar:
    password: str = st.text_input("Password", "", key="password", type="password")

    mode_list: list = ["General Chat", "Link Reader", "Translator"]
    mode: str = st.selectbox("Mode", mode_list, 0, key="mode", disabled=st.session_state.msg!=[])

    clear_btn: bool = st.button("Clear", "clear", type="primary", use_container_width=True, disabled=st.session_state.msg==[])
    undo_btn: bool = st.button("Undo", "undo", use_container_width=True, disabled=st.session_state.msg==[])
    retry_btn: bool = st.button("Retry", "retry", use_container_width=True, disabled=st.session_state.retry_switch)

    if mode == "General Chat":
        model_list: list = modelList(mode)
        model: str = st.selectbox("Model", model_list, 0, key="model", disabled=st.session_state.msg!=[])

        st.session_state.sys = general_system_prompt()
        system_prompt: str = st.text_area("System Prompt", st.session_state.sys, key="system_prompt", disabled=st.session_state.msg!=[])
        st.session_state.sys = system_prompt

        with st.expander("Parameter Settings"):
            max_tokens: int = st.slider("Max Tokens", 1, 4096, st.session_state.token, 1, key="max_tokens", disabled=st.session_state.msg!=[])
            temperature: float = st.slider("Temperature", 0.00, 2.00, st.session_state.temp, 0.01, key="temperature", disabled=st.session_state.msg!=[])
            top_p: float = st.slider("Top P", 0.00, 1.00, st.session_state.topp, 0.01, key="top_p", disabled=st.session_state.msg!=[])
            frequency_penalty: float = st.slider("Frequency Penalty", -2.00, 2.00, st.session_state.freq, 0.01, key="frequency_penalty", disabled=st.session_state.msg!=[])
            presence_penalty: float = st.slider("Presence Penalty", -2.00, 2.00, st.session_state.pres, 0.01, key="presence_penalty", disabled=st.session_state.msg!=[])
            st.session_state.token = max_tokens
            st.session_state.temp = temperature
            st.session_state.topp = top_p
            st.session_state.freq = frequency_penalty
            st.session_state.pres = presence_penalty
        
        if clear_btn:
            st.session_state.sys = general_system_prompt()
            st.session_state.msg = []
            st.session_state.mem = []
            st.session_state.token = 4096
            st.session_state.temp = 0.70
            st.session_state.topp = 0.70
            st.session_state.freq = 0.00
            st.session_state.pres = 0.00
            st.rerun()
    
    elif mode == "Link Reader":
        model_list: list = modelList(mode)
        model: str = st.selectbox("Model", model_list, 0, key="model", disabled=st.session_state.msg!=[])

        max_tokens: int = 4096
        temperature: float = 0.50
        top_p: float = 0.70
        frequency_penalty: float = 0.00
        presence_penalty: float = 0.00

        if clear_btn:
            st.session_state.msg = []
            st.session_state.mem = []
            st.rerun()
    
    elif mode == "Translator":
        model_list: list = modelList(mode)
        model: str = st.selectbox("Model", model_list, 0, key="model", disabled=st.session_state.msg!=[])

        max_tokens: int = 4096
        temperature: float = 0.70
        top_p: float = 0.70
        frequency_penalty: float = 0.00
        presence_penalty: float = 0.00

        if clear_btn:
            st.session_state.msg = []
            st.session_state.mem = []
            st.rerun()

if password == pass_word:
    st.session_state.login = True
    c = Chat(api_key, base_url)
else:
    st.session_state.login = False

def check_is_url(text: str) -> bool:
    is_url = text.startswith("http") or text.startswith("https")
    return is_url

for i in st.session_state.mem:
    with st.chat_message(i["role"]):
        st.markdown(i["content"])

if query := st.chat_input("Say something...", key="query", disabled=not st.session_state.login):
    if mode == "General Chat":
        st.session_state.msg.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
        
        messages: list = [{"role": "system", "content": system_prompt}] + st.session_state.msg
    
    elif mode == "Translator":
        st.session_state.msg.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
        
        st.session_state.sys = translation_system_prompt()

        messages: list = [{"role": "system", "content": st.session_state.sys}, {"role": "user", "content": query}]
    
    elif mode == "Link Reader":
        st.session_state.sys = link_reader_system(model)
        if st.session_state.msg == []:
            is_url: bool = check_is_url(query)
            if is_url:
                with st.spinner("Getting content..."):
                    user_prompt: str = link_reader_prompt(query, model)
                    if user_prompt:
                        st.session_state.msg.append({"role": "user", "content": user_prompt})
                with st.chat_message("user"):
                    st.markdown(st.session_state.msg[-1]["content"])
            else:
                st.error("Please enter a valid URL.")
                reset_btn: bool = st.button("Reset", "reset")
                if reset_btn:
                    st.rerun()
                st.stop()

        elif st.session_state.msg != []:
            st.session_state.msg.append({"role": "user", "content": query})
            with st.chat_message("user"):
                st.markdown(query)
        
        messages: list = [{"role": "system", "content": st.session_state.sys}] + st.session_state.msg

    with st.chat_message("assistant"):
        response = c.general_chat(model, messages, max_tokens, temperature, top_p, frequency_penalty, presence_penalty)
        result: str = st.write_stream(chunk.choices[0].delta.content for chunk in response if chunk.choices[0].delta.content is not None)

    st.session_state.msg.append({"role": "assistant", "content": result})
    st.session_state.mem = st.session_state.msg
    st.rerun()

if undo_btn:
    if mode != "Translator":
        del st.session_state.msg[-1]
        del st.session_state.mem[-1]
        st.rerun()
    else:
        st.info("Translator mode does not support undo.")

if retry_btn:
    if mode != "Translator":
        st.session_state.msg.pop()
        st.session_state.mem = []
        st.session_state.retry_state = True
        st.rerun()
    else:
        st.info("Translator mode does not support retry.")
if st.session_state.retry_state:
    for i in st.session_state.msg:
        with st.chat_message(i["role"]):
            st.markdown(i["content"])
    
    if mode != "Link Reader":
        messages: list = [{"role": "system", "content": system_prompt}] + st.session_state.msg
    else:
        st.session_state.sys = link_reader_system(model)
        messages: list = [{"role": "system", "content": st.session_state.sys}] + st.session_state.msg
    
    with st.chat_message("assistant"):
        response = c.general_chat(model, messages, max_tokens, temperature, top_p, frequency_penalty, presence_penalty)
        result: str = st.write_stream(chunk.choices[0].delta.content for chunk in response if chunk.choices[0].delta.content is not None)

    st.session_state.msg.append({"role": "assistant", "content": result})
    st.session_state.mem = st.session_state.msg
    st.session_state.retry_state = False
    st.rerun()