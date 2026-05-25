import streamlit as st
import json

from src.multilingual.run import run as run_gemma
from src.english.run_per_sentence import run as run_en_sent
from src.french.run_per_sentence import run as run_fr_sent
from src.english.run import run as run_en
from src.french.run import run as run_fr
from src.common import get_text_input
from src.config import (
    EMOTIONS, PROJECT_DIR, DEFAULT_LANG
)

def get_n_emotions() -> str:
    if ss.language == "en":
        return ss.n_emotions
    else:
        return ""

st.set_page_config(page_title="Sentiment Analysis", layout="wide")
st.title("Sentiment Analysis Interface")

ss = st.session_state

# --- SESSION STATE INITIALIZATION ---
if "language" not in ss:
    ss["language"] = DEFAULT_LANG

if "n_emotions" not in ss:
    ss["n_emotions"] = "7"

if "method" not in ss:
    ss["method"] = "Encoder"

if not "per_sentence" in ss:
    ss["per_sentence"] == "False"

if "emotions_fr" not in ss:
    ss["emotions_fr"] = EMOTIONS["fr"]

if "emotions_en" not in ss:
    ss["emotions_en"] = EMOTIONS["en"]

if "emotion_definitions_fr" not in ss:
    ss["emotion_definitions_fr"] = EMOTIONS["definitions_fr"]

if "emotion_definitions_en" not in ss:
    ss["emotion_definitions_en"] = EMOTIONS["definitions_en"]

if "user_input" not in ss:
    ss["user_input"] = get_text_input()

if "result" not in ss:
    ss["result"] = None

if "reasoning" not in ss:
    ss["reasoning"] = None

if "stats" not in ss:
    ss["stats"] = None


# --- SIDEBAR ---
st.sidebar.header("Configuration")

st.sidebar.selectbox("Language", ["en", "fr"], key="language")

if ss.language == "en":
    st.sidebar.selectbox("Number of emotions", ["7", "28"], key="n_emotions")

st.sidebar.selectbox("Method", ["Encoder", "Decoder"], key="method")

if ss.method == "Encoder":
    st.sidebar.selectbox("Analysis per sentence", ["True", "False"], key="per_sentence")

if ss.method == "Decoder":
    if ss.language == "en":
        st.sidebar.multiselect(
            "Select Elements", 
            options=ss.emotions_en,
            help="Add or remove elements from the list",
            key="emotions_en"
        )
    elif ss.language == "fr":
        st.sidebar.multiselect(
            "Select Elements", 
            options=ss.emotions_fr, # Fixed: added missing comma
            help="Add or remove elements from the list",
            key="emotions_fr"
        )

    if ss.language == "fr":
        st.sidebar.text_area("Optional emotion definitions", key="emotion_definitions_fr", height=400)
    elif ss.language == "en":
        st.sidebar.text_area("Optional emotion definitions", key="emotion_definitions_en", height=400)


# --- MAIN PANEL ---
st.text_area("Input Text", placeholder="Enter the text you wish to process here...", height=400, key="user_input")

if st.button("Run Function"):
    if not ss.user_input.strip():
        st.warning("Please enter some text before running the function.")
        ss.result = ""
        ss.stats = ""
        ss.reasoning = ""
    else:
        with open(PROJECT_DIR / "text_input.txt", "w") as f_:
            f_.write(ss.user_input)

        # Logic to build the correct key based on current UI state
        if ss.method == "Encoder":
            caller_str = f"{ss.language}_{ss.method}_{ss.per_sentence}_{get_n_emotions()}"
        else:
            caller_str = f"{ss.language}_{ss.method}"

        # Dynamically define methods so kwargs use the LATEST session_state values
        current_definitions = ss.emotion_definitions_en if ss.language == "en" else ss.emotion_definitions_fr

        methods = {
            "fr_Encoder_True_": {
                "func": run_fr_sent,
                "kwargs": {},
                "res_path": PROJECT_DIR / "response" / "response_per_sentence__emotion_french.json",
                "stats_path": PROJECT_DIR / "response" / "stats_response_per_sentence__emotion_french.json"
            },
            "fr_Encoder_False_": {
                "func": run_fr,
                "kwargs": {},
                "res_path": PROJECT_DIR / "response" / "response_emotion_french.json",
            },
            "fr_Decoder": {
                "func": run_gemma,
                "kwargs": {"lang": "fr", "definitions": current_definitions},
                "res_path": PROJECT_DIR / "response" / "response_Gemma_4_E2B.json",
                "reasoning_path": PROJECT_DIR / "response" / "reasoning_Gemma_4_E2B.txt",
            },
            "en_Encoder_True_7": {
                "func": run_en_sent,
                "kwargs": {"mode" : "7"},
                "res_path": PROJECT_DIR / "response" / "response_per_sentence__emotion_english.json",
                "stats_path": PROJECT_DIR / "response" / "stats_response_per_sentence__emotion_english.json"
            },
            "en_Encoder_True_28": {
                "func": run_en_sent,
                "kwargs": {"mode" : "28"},
                "res_path": PROJECT_DIR / "response" / "response_per_sentence__emotion_english.json",
                "stats_path": PROJECT_DIR / "response" / "stats_response_per_sentence__emotion_english.json"
            },
            "en_Encoder_False_7": {
                "func": run_en_sent,
                "kwargs": {"mode" : "7"},
                "res_path": PROJECT_DIR / "response" / "response_emotion_english_distilroberta.json"
            },
            "en_Encoder_False_28": {
                "func": run_en_sent,
                "kwargs": {"mode" : "28"},
                "res_path": PROJECT_DIR / "response" / "response_roberta_go_emotions.json"
            },
            "en_Decoder": {
                "func": run_gemma,
                "kwargs": {"lang": "en", "definitions": current_definitions},
                "res_path": PROJECT_DIR / "response" / "response_Gemma_4_E2B.json",
                "reasoning_path": PROJECT_DIR / "response" / "reasoning_Gemma_4_E2B.txt",
            }
        }

        if caller_str not in methods:
            st.error(f"Invalid Configuration: '{caller_str}' not found in methods mapping.")
        else:
            with st.spinner("Processing..."):
                method_params = methods[caller_str]
                func = method_params["func"]
                kwargs = method_params["kwargs"]

                # Execute the function
                func(**kwargs)

                # Load results from files
                if "res_path" in method_params:
                    with open(str(method_params["res_path"]), "r") as f_:
                        ss.result = f_.read()

                if "reasoning_path" in method_params:
                    with open(str(method_params["reasoning_path"]), "r") as f_:
                        ss.reasoning = f_.read()

                if "stats_path" in method_params:
                    with open(str(method_params["stats_path"]), "r") as f_:
                        ss.stats = f_.read()

# --- DISPLAY TABS ---
tabs = st.tabs(["result", "prompt & reasoning", "stats summary"])

with tabs[0]:
    if ss.result:
        with st.container(height=400):
            st.markdown(ss.result)

with tabs[1]:
    if ss.reasoning:
        with st.container(height=400):
            st.markdown(ss.reasoning)

with tabs[2]:
    if ss.stats:
        with st.container(height=400):
            st.markdown(ss.stats)