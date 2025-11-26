# streamlit_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv(r"/Users/priyankamalavade/Desktop/Customer_Segmentation_Sales_Analytics/data/processed/clustered_customers.csv")
    df['Churn'] = (df['Recency'] > 180).astype(int)
    return df

rfm = load_data()

# Load Model
model = joblib.load(r"/Users/priyankamalavade/Desktop/Customer_Segmentation_Sales_Analytics/model/churn_prediction_model.pkl")

# Use the full dataset as filtered_rfm for simplicity
filtered_rfm = rfm.copy()

# Page Config
st.set_page_config(page_title="Customer Dashboard", layout="wide")

# Sidebar - Navigation
st.sidebar.title("📁 Dashboard Navigation")
section = st.sidebar.radio("Go to Section", ["Introduction", "Overview", "RFM Analysis", "Clusters", "Churn Analysis", "Predict Churn"])

# Header
st.markdown("""
    <style>
        .big-font { font-size:32px !important; font-weight: bold; color: #4F8BF9; }
        .section-header { font-size:24px !important; color: #444; margin-top: 30px; }
        .metric-style .metric-label { font-size:16px; color: #555; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<p class='big-font'>📊 Customer Segmentation & Churn Dashboard</p>", unsafe_allow_html=True)

# Introduction Section
if section == "Introduction":
    st.markdown("---")
    st.markdown("""
        ## 🧾 Project Introduction

        This interactive dashboard helps businesses understand customer behavior using:

        - 📦 **RFM Analysis**: Measures Recency, Frequency, and Monetary value of customers
        - 🧠 **Customer Segmentation**: Groups customers based on purchasing behavior
        - 🔮 **Churn Prediction**: Uses a machine learning model to predict if a customer is at risk of churning

        ### 💡 Objectives:
        - Improve customer retention strategies
        - Tailor marketing based on segment behavior
        - Identify at-risk customers early

        ### 📂 Dataset Overview:
        - Transactions from an e-commerce platform
        - ~25,000 purchases with Customer ID, Purchase Date, and Product Details

        👉 Use the navigation sidebar to explore sections and insights.
    """)

# Overview Section
elif section == "Overview":
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🧑‍🤝‍🧑 Total Customers", f"{filtered_rfm['CustomerID'].nunique()}")
    with col2:
        st.metric("💰 Total Revenue", f"₹{filtered_rfm['Monetary'].sum():,.0f}")
    with col3:
        st.metric("⏱️ Avg Recency", f"{filtered_rfm['Recency'].mean():.0f} days")
    with col4:
        churn_rate = filtered_rfm['Churn'].mean() * 100
        st.metric("⚠️ Churn Rate", f"{churn_rate:.2f}%")

    st.markdown("<p class='section-header'>📌 Use the sidebar to explore detailed views.</p>", unsafe_allow_html=True)

# RFM Analysis Section
elif section == "RFM Analysis":
    st.markdown("---")
    st.markdown("<p class='section-header'>📦 RFM Metric Distributions</p>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    with c1:
        fig = px.histogram(filtered_rfm, x="Recency", nbins=30, color_discrete_sequence=["#00bcd4"])
        fig.update_layout(title="Recency", height=300)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.histogram(filtered_rfm, x="Frequency", nbins=30, color_discrete_sequence=["#8bc34a"])
        fig.update_layout(title="Frequency", height=300)
        st.plotly_chart(fig, use_container_width=True)

    with c3:
        fig = px.histogram(filtered_rfm, x="Monetary", nbins=30, color_discrete_sequence=["#ff7043"])
        fig.update_layout(title="Monetary", height=300)
        st.plotly_chart(fig, use_container_width=True)

# Cluster Section
elif section == "Clusters":
    st.markdown("---")
    st.markdown("<p class='section-header'>🧠 Customer Segment Overview</p>", unsafe_allow_html=True)

    cluster_counts = filtered_rfm['Cluster'].value_counts().sort_index().reset_index()
    cluster_counts.columns = ['Cluster', 'Customer Count']
    fig = px.bar(cluster_counts, x='Cluster', y='Customer Count',
                 color='Cluster', color_discrete_sequence=px.colors.sequential.Teal,
                 title="Customer Count by Cluster")
    st.plotly_chart(fig, use_container_width=True)

    cluster_means = filtered_rfm.groupby('Cluster')[['Recency', 'Frequency', 'Monetary']].mean().reset_index()
    fig = px.bar(cluster_means, x='Cluster', y=['Recency', 'Frequency', 'Monetary'],
                 barmode='group', title='Average RFM by Cluster',
                 color_discrete_sequence=px.colors.qualitative.Dark24)
    st.plotly_chart(fig, use_container_width=True)

# Churn Section
elif section == "Churn Analysis":
    st.markdown("---")
    st.markdown("<p class='section-header'>🔮 Churn Insights</p>", unsafe_allow_html=True)

    churn_by_cluster = filtered_rfm.groupby('Cluster')['Churn'].mean().reset_index()
    churn_by_cluster['Churn Rate (%)'] = churn_by_cluster['Churn'] * 100
    fig = px.bar(churn_by_cluster, x='Cluster', y='Churn Rate (%)',
                 color='Cluster', text_auto='.2f',
                 color_discrete_sequence=px.colors.sequential.Sunset,
                 title="Churn Rate by Cluster")
    st.plotly_chart(fig, use_container_width=True)

    fig = px.box(filtered_rfm, x='Churn', y='Recency', color='Churn',
                 color_discrete_map={0: 'green', 1: 'red'},
                 title="Recency by Churn Status")
    fig.update_layout(xaxis=dict(tickvals=[0, 1], ticktext=["Not Churned", "Churned"]))
    st.plotly_chart(fig, use_container_width=True)

# Predict Churn Section
elif section == "Predict Churn":
    st.markdown("---")
    st.markdown("<p class='section-header'>📈 Predict Customer Churn</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        recency = st.number_input("Recency (days)", min_value=0, max_value=365, value=90)
    with col2:
        frequency = st.number_input("Frequency", min_value=1, max_value=100, value=10)
    with col3:
        monetary = st.number_input("Monetary", min_value=1, max_value=10000, value=500)

    if st.button("Predict Churn", use_container_width=True):
        input_df = pd.DataFrame([[recency, frequency, monetary]], columns=["Recency", "Frequency", "Monetary"])
        prediction = model.predict(input_df)[0]
        result = "🟢 Not Likely to Churn" if prediction == 0 else "🔴 At Risk of Churning"
        st.success(f"Prediction Result: {result}")

# Footer
st.markdown("---")
st.caption("Made with ❤️ by Priyanka | Powered by Streamlit + Plotly")
