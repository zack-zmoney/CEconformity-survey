#!/usr/bin/env python
# coding: utf-8

# In[33]:


import streamlit as st
import pandas as pd
import os

# ⬇️ Add this block to hide the sidebar toggle arrow
hide_sidebar_style = """
    <style>
        /* Hide sidebar collapse/expand button across all screen sizes */
        [data-testid="collapsedControl"] {
            display: none !important;
        }

        /* On mobile, also remove the sidebar entirely if needed */
        @media (max-width: 768px) {
            section[data-testid="stSidebar"] {
                display: none !important;
            }
        }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

CSV_PATH = "survey_results.csv"
EXPECTED_COLUMNS = ["initial_correct", "conformed"]

# --- CSV Setup ---
if not os.path.exists(CSV_PATH):
    pd.DataFrame(columns=EXPECTED_COLUMNS).to_csv(CSV_PATH, index=False)
df = pd.read_csv(CSV_PATH)

# --- Sidebar reset button ---
if st.sidebar.button("🔄 Reset Responses"):
    pd.DataFrame(columns=EXPECTED_COLUMNS).to_csv(CSV_PATH, index=False)
    st.sidebar.success("Responses have been reset.")
    st.stop()

# --- Session state defaults ---
for key in ["answered", "initial_correct", "show_followup", "followup_answered"]:
    if key not in st.session_state:
        st.session_state[key] = False

# --- Title ---
st.title("Counterfeit Emotions Survey")

# --- Initial Question ---
def submit_initial_answer():
    st.session_state.answered = True
    choice = st.session_state.user_choice
    if choice == "C":
        st.session_state.initial_correct = True
        st.session_state.show_followup = True
    else:
        new_row = pd.DataFrame([[False, False]], columns=EXPECTED_COLUMNS)
        updated_df = pd.concat([df, new_row], ignore_index=True)
        updated_df.to_csv(CSV_PATH, index=False)
        st.session_state.followup_answered = True  # Skip follow-up for incorrect answers

if not st.session_state.answered:
    st.subheader("Which line matches the target line in length?")
    st.markdown("### Target Line")
    st.progress(50, text="Target")

    st.markdown("### Options")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**A**")
        st.progress(42)
    with col2:
        st.markdown("**B**")
        st.progress(58)
    with col3:
        st.markdown("**C**")
        st.progress(50)

    st.radio("Select the matching line:", ["A", "B", "C"], key="user_choice")
    st.button("Submit Answer", on_click=submit_initial_answer)

# --- Follow-up Question ---
def submit_followup():
    conformed = st.session_state.change_to_b == "Yes"
    new_row = pd.DataFrame([[True, conformed]], columns=EXPECTED_COLUMNS)
    updated_df = pd.concat([df, new_row], ignore_index=True)
    updated_df.to_csv(CSV_PATH, index=False)
    st.session_state.followup_answered = True

if st.session_state.show_followup and not st.session_state.followup_answered:
    st.warning("100% of others answered B. Would you like to change your answer?")
    st.radio("Would you like to change your answer to B?", ["Yes", "No"], key="change_to_b")
    st.button("Confirm Final Answer", on_click=submit_followup)

# --- Live Results ---
if st.session_state.answered and st.session_state.followup_answered:
    df = pd.read_csv(CSV_PATH)
    st.markdown("### 📊 Live Results")
    total_correct = df["initial_correct"].sum()
    total_conformed = df["conformed"].sum()
    if total_correct > 0:
        percent = (total_conformed / total_correct) * 100
        st.markdown(f"**{percent:.1f}%** of users who answered correctly later changed their answer.")
    else:
        st.markdown("No correct answers recorded yet.")


# In[ ]:




