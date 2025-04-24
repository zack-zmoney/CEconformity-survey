#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import os

CSV_PATH = "survey_results.csv"

# Show reset button in the sidebar
if st.sidebar.button("🔄 Reset Responses"):
    df = pd.DataFrame(columns=["initial_correct", "conformed"])
    df.to_csv(CSV_PATH, index=False)
    st.sidebar.success("Responses have been reset.")

# Load CSV only AFTER potential reset
if os.path.exists(CSV_PATH):
    df = pd.read_csv(CSV_PATH)
else:
    df = pd.DataFrame(columns=["initial_correct", "conformed"])

st.write("📄 Data currently loaded:", df)

#Set the name of the survey
st.title("Counterfeit Emotions Survey")
st.subheader("Which line matches the target line in length?")

# --- File setup ---
CSV_PATH = "survey_results.csv"
expected_columns = ["initial_correct", "conformed"]

# Create or fix CSV with proper columns
if not os.path.exists(CSV_PATH):
    pd.DataFrame(columns=expected_columns).to_csv(CSV_PATH, index=False)
else:
    # Ensure columns are as expected
    df = pd.read_csv(CSV_PATH)
    if list(df.columns) != expected_columns:
        df = pd.DataFrame(columns=expected_columns)
        df.to_csv(CSV_PATH, index=False)

# --- Visual lines ---
st.markdown("### Target Line")
st.progress(50, text="Target")

st.markdown("### Options")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**A**")
    st.progress(30)
with col2:
    st.markdown("**B**")
    st.progress(70)
with col3:
    st.markdown("**C**")
    st.progress(50)

# --- Initialize session state ---
if 'answered' not in st.session_state:
    st.session_state.answered = False
if 'show_followup' not in st.session_state:
    st.session_state.show_followup = False
if 'initial_correct' not in st.session_state:
    st.session_state.initial_correct = False

# --- User selection ---
user_choice = st.radio("Select the matching line:", ["A", "B", "C"])

# --- Submit button ---
if st.button("Submit Answer") and not st.session_state.answered:
    st.session_state.answered = True
    if user_choice == "C":
        st.session_state.initial_correct = True
        st.session_state.show_followup = True
    else:
        st.success("Thank you for participating!")
        df = pd.read_csv(CSV_PATH)
        new_row = pd.DataFrame([[False, False]], columns=expected_columns)
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(CSV_PATH, index=False)

# --- Follow-up for correct answers ---
if st.session_state.show_followup:
    st.warning("100% of the other CEO's answered B. Would you like to change your answer?")
    change_answer = st.radio("Would you like to change your answer to B?", ["Yes", "No"])

    if st.button("Confirm Final Answer"):
        conformed = (change_answer == "Yes")
        df = pd.read_csv(CSV_PATH)
        new_row = pd.DataFrame([[True, conformed]], columns=expected_columns)
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(CSV_PATH, index=False)
        st.session_state.followup_answered = True
        st.success("Thank you for participating!")
        st.session_state.show_followup = False

# Show live results only after the full interaction is complete
if (
    st.session_state.get("answered", False)
    and (
        not st.session_state.get("initial_correct", False)
        or st.session_state.get("followup_answered", False)
    )
):
    df = pd.read_csv(CSV_PATH)
    if not df.empty:
        total_correct = df["initial_correct"].sum()
        total_conformed = df["conformed"].sum()
        if total_correct > 0:
            conformity_percent = (total_conformed / total_correct) * 100
            st.markdown("### 📊 Live Results")
            st.markdown(f"**{conformity_percent:.1f}%** of users who initially answered correctly later changed their answer after the prompt.")
        else:
            st.markdown("### 📊 Live Results")
            st.markdown("No correct answers recorded yet.")


# In[ ]:




