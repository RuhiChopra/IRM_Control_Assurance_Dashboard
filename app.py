import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_generator import generate_dr_data

# Page Configuration
st.set_page_config(page_title="Manulife IRM: DR Compliance Dashboard", layout="wide")

# --- LOAD DATA ---
df = generate_dr_data(60)

# --- HEADER ---
st.title("🛡️ IT Disaster Recovery (DR) Control Assurance Dashboard")
st.markdown("""
**Objective:** Monitor compliance with ISO 27001/NIST frameworks regarding IT Service Continuity.
**Key Metrics:** Recovery Time Actuals vs. Targets, Remediation Ticket Aging, and Asset Criticality.
""")
st.markdown("---")

# --- KPI ROW ---
total_apps = len(df)
failed_tests = len(df[df['Test Status'] == 'Fail'])
compliance_rate = ((total_apps - failed_tests) / total_apps) * 100
open_tickets = len(df[df['Ticket Status'].isin(['Open', 'Overdue'])])
avg_ticket_age = df[df['Ticket Age (Days)'] > 0]['Ticket Age (Days)'].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Applications Assessed", total_apps)
col2.metric("DR Compliance Rate", f"{compliance_rate:.1f}%", delta_color="normal")
col3.metric("Active Remediation Tickets", open_tickets, delta="-High Risk" if open_tickets > 5 else "Normal")
col4.metric("Avg Ticket Age (Days)", f"{avg_ticket_age:.0f} Days")

st.markdown("---")

# --- CHARTS ROW 1 ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("📊 RTO Adherence: Target vs. Actual")
    # Filter for Tier 1 apps only for cleaner view
    tier1_df = df[df['Criticality Tier'] == 'Tier 1 (Critical)']
    
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=tier1_df['Application Name'], y=tier1_df['Target RTO (Hrs)'],
        name='Target RTO', marker_color='lightgrey'
    ))
    fig_bar.add_trace(go.Bar(
        x=tier1_df['Application Name'], y=tier1_df['Actual RTO (Hrs)'],
        name='Actual RTO', marker_color='#00b050' # Manulife Green-ish
    ))
    fig_bar.update_layout(barmode='group', title="Tier 1 Critical Apps - Recovery Time Performance")
    # FIXED: Removed use_container_width to fix warning
    st.plotly_chart(fig_bar)

with c2:
    st.subheader("⚠️ Risk Distribution by Department")
    # Count fails by department
    fail_counts = df[df['Test Status'] == 'Fail']['Department'].value_counts().reset_index()
    fail_counts.columns = ['Department', 'Failed Tests']
    
    fig_pie = px.pie(fail_counts, values='Failed Tests', names='Department', 
                     title="Departments with Highest DR Control Failures",
                     color_discrete_sequence=px.colors.sequential.RdBu)
    # FIXED: Removed use_container_width to fix warning
    st.plotly_chart(fig_pie)

# --- CHARTS ROW 2 ---
c3, c4 = st.columns([2, 1])

with c3:
    st.subheader("📋 Remediation Ticket Aging")
    
    # Scatter plot: Ticket Age vs Application
    ticket_df = df[df['Ticket Status'] != 'N/A']
    fig_scatter = px.scatter(ticket_df, x='Ticket Age (Days)', y='Application Name',
                             color='Criticality Tier', size='Ticket Age (Days)',
                             color_discrete_map={'Tier 1 (Critical)': 'red', 'Tier 2 (High)': 'orange', 'Tier 3 (Standard)': 'blue'},
                             title="Aging of Open DR Remediation Tickets")
    # FIXED: Removed use_container_width to fix warning
    st.plotly_chart(fig_scatter)

with c4:
    st.subheader("🔍 Non-Compliant Assets")
    # FIXED: Corrected the column name below from 'Ticket ID' to 'Remediation Ticket ID'
    failed_apps = df[df['Test Status'] == 'Fail'][['Application Name', 'Criticality Tier', 'Remediation Ticket ID']]
    st.dataframe(failed_apps, hide_index=True)

# --- FOOTER ---
st.markdown("---")
st.caption("Created by Ruhi Chopra | Tech Stack: Python, Pandas, Plotly (Designed to simulate Power BI reporting flow)")