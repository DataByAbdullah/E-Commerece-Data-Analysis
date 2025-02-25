import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("Sample - Superstore.csv")  # Ensure dataset.csv exists

df = load_data()

# Sidebar Filters
st.sidebar.header("🔍 Filters")
selected_segment = st.sidebar.multiselect("Select Customer Segment", df['Segment'].unique(), default=df['Segment'].unique())

# Filter data based on selection
filtered_df = df[df['Segment'].isin(selected_segment)]

# KPI Metrics
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

# Animated Background & Custom Styling
st.markdown("""
    <style>
        /* Set Animated Background with GIF */
            
       
        .background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('https://media.giphy.com/media/26AHONQ79FdWZhAI0/giphy.gif') no-repeat center center fixed;
            background-size: cover;
            z-index: -1;
        }

        /* Gradient Text Background */
        .gradient-text {
            background: linear-gradient(45deg, #ff416c, #ff4b2b, #ff8c00, #ff416c);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 40px;
            font-weight: bold;
            text-align: center;
        }

        /* KPI Cards */
        .metric-box {
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #76c7c0, #ffb347);
            color: white;
            border-radius: 15px;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.3);
            transition: transform 0.3s;
        }

        .metric-box:hover {
            transform: scale(1.05);
        }

        /* Profile Animation */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .profile-section {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            margin-bottom: 20px;
            animation: fadeIn 2s ease-in-out;
        }

        .profile-img {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            border: 3px solid white;
            box-shadow: 0px 4px 8px rgba(255,255,255,0.4);
        }

        .profile-name {
            font-size: 24px;
            font-weight: bold;
            color: white;
            margin-top: 10px;
        }

        /* Footer */
        .footer {
            text-align: center;
            margin-top: 20px;
            padding: 10px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border-radius: 10px;
        }
    </style>
    
    <!-- Background -->
    <div class="background"></div>
""", unsafe_allow_html=True)

# Animated Profile Section
st.markdown("""
    <div class="profile-section">
        <img class="profile-img" src="https://avatars.githubusercontent.com/u/583231?v=4">
        <div class="profile-name"> Abdullah The analyst </div>
    </div>
""", unsafe_allow_html=True)

# Dashboard Layout
st.markdown('<h1 class="gradient-text">✨ Business Sales & Profit Dashboard</h1>', unsafe_allow_html=True)
st.markdown("#### 📊 Interactive visualization of sales and profit insights")

# KPI Metrics with Animated Cards
col1, col2, col3 = st.columns(3)
col1.markdown(f"<div class='metric-box'>💰 <b>Total Sales:</b> ${total_sales:,.2f}</div>", unsafe_allow_html=True)
col2.markdown(f"<div class='metric-box'>📈 <b>Total Profit:</b> ${total_profit:,.2f}</div>", unsafe_allow_html=True)
col3.markdown(f"<div class='metric-box'>📊 <b>Profit Margin : <br> </b> {profit_margin:.2f}%</div>", unsafe_allow_html=True)

# Sales & Profit by Segment
st.subheader(" Sales and Profit by Customer Segment")
segment_fig = px.bar(
    filtered_df.groupby("Segment")[["Sales", "Profit"]].sum().reset_index().melt(id_vars="Segment"),
    x="Segment", y="value", color="variable",
    barmode="group", title="Sales vs Profit by Segment",
    color_discrete_map={"Sales": "#76c7c0", "Profit": "#e0b656"}
)
st.plotly_chart(segment_fig)

# Sales to Profit Ratio
st.subheader(" Sales to Profit Ratio")
df_ratio = filtered_df.groupby("Segment")[["Sales", "Profit"]].sum()
df_ratio["Sales_to_Profit_Ratio"] = df_ratio["Sales"] / df_ratio["Profit"]
ratio_fig = px.bar(df_ratio.reset_index(), x="Segment", y="Sales_to_Profit_Ratio", color="Segment", title="Sales to Profit Ratio", color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(ratio_fig)

# Pie Chart for Profit Distribution
st.subheader(" Profit Distribution by Category")
profit_fig = px.pie(filtered_df.groupby("Category")["Profit"].sum().reset_index(), names="Category", values="Profit", title="Profit Share by Category", color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(profit_fig)

# Download Report
st.sidebar.subheader("📥 Download Report")
st.sidebar.download_button("Download CSV", df.to_csv(index=False), "sales_report.csv", "text/csv")

# Footer
st.markdown('<div class="footer">🔹 Built with <b>Streamlit</b> | 🚀 Created for Public Insights</div>', unsafe_allow_html=True)
