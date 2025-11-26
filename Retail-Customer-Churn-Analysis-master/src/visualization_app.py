import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set Streamlit page configuration
st.set_page_config(layout="wide", page_title="Retail Customer Churn Analysis Dashboard")

# --- Function to Load Data and Model ---
@st.cache_data # Cache data loading for performance
def load_data():
    """Loads the feature-engineered data with predictions."""
    try:
        df = pd.read_csv(r'data\processed\customer_churn_predictions.csv')
        return df
    except FileNotFoundError:
        st.error("Error: 'customer_churn_predictions.csv' not found. Please ensure 02_feature_engineering.ipynb and 04_dashboard_insights.ipynb were run.")
        return pd.DataFrame() # Return empty DataFrame
    except Exception as e:
        st.error(f"Error loading customer churn predictions data: {e}")
        return pd.DataFrame()

@st.cache_resource # Cache model loading (for large models)
def load_model():
    """Loads the best trained churn prediction model."""
    try:
        model = joblib.load(r'models\best_churn_model.joblib')
        return model
    except FileNotFoundError:
        st.error("Error: 'best_churn_model.joblib' not found. Please ensure 03_model_training_and_evaluation.ipynb was run and the model was saved.")
        return None
    except Exception as e:
        st.error(f"Error loading churn prediction model: {e}")
        return None

# Load data and model
df_features = load_data()
model = load_model()

# Check if data and model loaded successfully
if df_features.empty or model is None:
    st.stop() # Stop the app if essential components are missing

# --- Function to get Feature Importances (from the loaded model) ---
# This function is crucial for displaying churn drivers dynamically
def get_feature_importances(model, feature_columns):
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        feature_importance_df = pd.DataFrame({
            'Feature': feature_columns,
            'Importance': importances
        }).sort_values(by='Importance', ascending=False)
        return feature_importance_df
    elif hasattr(model, 'coef_'): # For linear models like Logistic Regression (if used instead)
        importances = model.coef_[0]
        feature_importance_df = pd.DataFrame({
            'Feature': feature_columns,
            'Importance': np.abs(importances) # Use absolute value for coefficients
        }).sort_values(by='Importance', ascending=False)
        return feature_importance_df
    return pd.DataFrame()


# Prepare X for feature importance (drop non-feature columns)
X_for_importance = df_features.drop(['Customer ID', 'is_churned', 'churn_probability', 'predicted_churn', 'PrimaryCountry_Grouped_Original'], axis=1, errors='ignore')
feature_importance_df = get_feature_importances(model, X_for_importance.columns)


# --- Dashboard Layout and Content ---

st.title("🛍️ Retail Customer Churn Analysis Dashboard")
st.markdown("This interactive dashboard helps to predict customer churn and understand key influencing factors, enabling targeted retention strategies.")

# Overview Metrics
st.header("📈 Overall Churn Insights")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_customers = df_features['Customer ID'].nunique()
    st.metric(label="Total Customers", value=f"{total_customers:,}")

with col2:
    actual_churn_rate = df_features['is_churned'].mean() * 100
    st.metric(label="Actual Churn Rate", value=f"{actual_churn_rate:.2f}%")

with col3:
    predicted_churn_rate = df_features['predicted_churn'].mean() * 100
    st.metric(label="Predicted Churn Rate", value=f"{predicted_churn_rate:.2f}%")

with col4:
    # Example: Number of customers predicted to churn
    predicted_churners = df_features['predicted_churn'].sum()
    st.metric(label="Predicted Churners", value=f"{predicted_churners:,}")


st.markdown("---")

# --- Churn Drivers and Segmentation ---
st.header("📊 Churn Drivers & Customer Segmentation")

tab1, tab2 = st.tabs(["Key Churn Drivers", "Churn by Country"])

with tab1:
    st.subheader("Top Features Influencing Churn")
    if not feature_importance_df.empty:
        fig_importance = px.bar(feature_importance_df.head(10), x='Importance', y='Feature', orientation='h',
                                title='Top 10 Feature Importances',
                                color='Importance', color_continuous_scale=px.colors.sequential.Viridis)
        fig_importance.update_layout(yaxis={'categoryorder':'total ascending'}) # Sort from smallest to largest on chart
        st.plotly_chart(fig_importance, use_container_width=True)
    else:
        st.warning("Feature importance data not available for the loaded model.")

with tab2:
    st.subheader("Churn Rate by Country Group")
    churn_by_country = df_features.groupby('PrimaryCountry_Grouped_Original')['is_churned'].mean().sort_values(ascending=False).reset_index()
    churn_by_country['is_churned'] = churn_by_country['is_churned'] * 100 # Convert to percentage

    fig_country_churn = px.bar(churn_by_country, x='PrimaryCountry_Grouped_Original', y='is_churned',
                               title='Churn Rate by Country Group',
                               labels={'is_churned': 'Churn Rate (%)', 'PrimaryCountry_Grouped_Original': 'Country Group'},
                               color='is_churned', color_continuous_scale=px.colors.sequential.Plasma)
    fig_country_churn.update_layout(xaxis_title="Country Group", yaxis_title="Churn Rate (%)")
    st.plotly_chart(fig_country_churn, use_container_width=True)


st.markdown("---")

# --- At-Risk Customer List ---
st.header("🎯 At-Risk Customers")

st.markdown("Identify customers with a high probability of churning for targeted retention efforts.")

# Slider for churn probability threshold
churn_threshold = st.slider(
    "Select Churn Probability Threshold:",
    min_value=0.0,
    max_value=1.0,
    value=0.5, # Default threshold
    step=0.01,
    help="Customers with a predicted churn probability above this threshold are considered 'at-risk'."
)

at_risk_customers_filtered = df_features[df_features['churn_probability'] >= churn_threshold].sort_values(by='churn_probability', ascending=False)

st.info(f"Showing {len(at_risk_customers_filtered):,} customers with churn probability >= {churn_threshold:.2f}")

if not at_risk_customers_filtered.empty:
    # Select columns to display in the table for at-risk customers
    display_cols = [
        'Customer ID', 'churn_probability', 'predicted_churn',
        'Recency', 'Frequency', 'Monetary', 'Tenure', 'PrimaryCountry_Grouped_Original'
    ]
    st.dataframe(at_risk_customers_filtered[display_cols].head(500), # Show top 500 or adjust as needed
                 hide_index=True,
                 column_config={
                     "churn_probability": st.column_config.ProgressColumn(
                         "Churn Probability",
                         help="Predicted probability of customer churning",
                         format="%.2f",
                         min_value=0,
                         max_value=1,
                     ),
                     "Recency": st.column_config.NumberColumn("Recency (Days)"),
                     "Frequency": st.column_config.NumberColumn("Frequency (Transactions)"),
                     "Monetary": st.column_config.NumberColumn("Monetary (£)", format="£%.2f"),
                     "Tenure": st.column_config.NumberColumn("Tenure (Days)"),
                     "predicted_churn": st.column_config.CheckboxColumn("Predicted Churn")
                 })
else:
    st.write("No customers identified as 'at-risk' with the current threshold.")


st.markdown("---")
st.info("💡 **Insights:** Analyze the characteristics (Recency, Frequency, Monetary, Tenure) of at-risk customers and the top churn drivers to develop targeted retention strategies. For instance, customers with high Recency (haven't purchased recently) and low Frequency might be prime candidates for re-engagement campaigns.")

# --- End of Streamlit App ---
