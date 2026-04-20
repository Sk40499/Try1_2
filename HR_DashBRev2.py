#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("HR Analytics Dashboard")

# Upload
file = st.file_uploader("Upload JSON or Excel", type=["json", "xlsx"])

def parse_date(x):
    try:
        return pd.to_datetime(x, errors='coerce')
    except:
        return None

if file:
    # Read file
    if file.name.endswith(".json"):
        df = pd.read_json(file)
    else:
        df = pd.read_excel(file)

    st.subheader("Data Preview")
    st.dataframe(df)

    # Clean dates
    df["VISA EXPIRY"] = df["VISA EXPIRY"].apply(parse_date)
    df["CICPA EXPIRY"] = df["CICPA EXPIRY"].apply(parse_date)

    # KPIs
    total = len(df)
    active = df["CURRENT STATUS"].str.contains("Active", na=False).sum()
    inactive = total - active

    today = datetime.today()
    soon = today + timedelta(days=90)

    visa_exp = df[df["VISA EXPIRY"] < soon]
    cicpa_exp = df[df["CICPA EXPIRY"] < soon]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total", total)
    col2.metric("Active", active)
    col3.metric("Inactive", inactive)
    col4.metric("Visa Expiring (90d)", len(visa_exp))

    # Filters
    status = st.selectbox("Filter by Status", ["All", "Active", "Inactive"])

    if status != "All":
        df = df[df["CURRENT STATUS"].str.contains(status, na=False)]

    # Charts
    st.subheader("Employee Status")
    st.bar_chart(df["CURRENT STATUS"].value_counts())

    st.subheader("Department Distribution")
    st.bar_chart(df["DEPARTMENT"].value_counts())

    st.subheader("Nationality Distribution")
    st.bar_chart(df["NATIONALITY"].value_counts())

    # Alerts
    st.subheader("⚠ Visa Expiring Soon")
    st.dataframe(visa_exp[["NAME", "VISA EXPIRY"]])

    st.subheader("⚠ Security Pass Expiring Soon")
    st.dataframe(cicpa_exp[["NAME", "CICPA EXPIRY"]])

