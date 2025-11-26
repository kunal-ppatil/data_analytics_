# 📊 Customer Segmentation & Churn Prediction Dashboard

An interactive Streamlit + Plotly dashboard to analyze customer transactions using **RFM segmentation**, **clustering**, and **churn prediction**. Built for marketing and business strategy teams to understand customer behavior, identify valuable segments, and reduce churn.

---

## 🚀 Features

* 🔍 **RFM Analysis**: Calculate Recency, Frequency, and Monetary value for each customer.
* 🔄 **Customer Segmentation**: Cluster customers using K-Means.
* ⚠️ **Churn Prediction**: Predict churn risk using a machine learning model.
* 🌐 **Interactive Dashboard**: View insights, filter segments, and simulate churn.

---

## 📂 Folder Structure

```
Customer_Segmentation_Sales_Analytics/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   ├── 1_data_cleaning.ipynb
│   ├── 2_rfm_segmentation.ipynb
│   ├── 3_clustering.ipynb
│   └── 4_churn_prediction.ipynb
├── model/
│   └── churn_prediction_model.pkl
├── streamlit_app.py
└── README.md
```

---

## 🛠️ Technologies Used

* **Python** (Pandas, Scikit-learn, Matplotlib, Seaborn)
* **Machine Learning**: K-Means, Logistic Regression
* **Visualization**: Plotly, Streamlit

---

## 📈 How to Run

### 1. Clone the repository:

```bash
git clone https://github.com/your-username/customer-segmentation-churn-dashboard.git
cd customer-segmentation-churn-dashboard
```

### 2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies:

```bash
pip install -r requirements.txt
```

### 4. Launch the Streamlit app:

```bash
streamlit run streamlit_app.py
```

---

## 📌 Dashboard Sections

* **Introduction**: Overview of goals and dataset
* **Overview**: KPIs and churn stats
* **RFM Analysis**: Distribution plots
* **Clusters**: Segment insights
* **Churn Analysis**: Risk visualizations
* **Predict Churn**: User input + model output

---

## 📊 Dataset

This project uses a public e-commerce transactions dataset with \~25,000 records:

* `InvoiceNo`, `CustomerID`, `InvoiceDate`, `Quantity`, `UnitPrice`, `Country`

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🙋‍♀️ Author

**Kunal Patil**

---

*Made with ❤️ using Streamlit and Plotly.*
