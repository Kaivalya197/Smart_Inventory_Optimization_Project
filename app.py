import streamlit as st
import joblib
import pandas as pd

# ----------------------------------------
# ✅ Load model and feature names from ONE .pkl file
# ----------------------------------------
model_package = joblib.load("demand_model.pkl")
model = model_package['model']
feature_order = model_package['features']  # exact column order used in training

# ----------------------------------------
# 🧾 App Title and Description
# ----------------------------------------
st.title("📦 Smart Inventory Demand Predictor")
st.markdown("Predict demand for retail products using past inventory, promotions, and conditions.")

# ----------------------------------------
# 📥 Input Fields
# ----------------------------------------
store_id = st.number_input("Store ID", min_value=0, max_value=50, step=1)
product_id = st.number_input("Product ID", min_value=0, max_value=1000, step=1)
category = st.number_input("Category", min_value=0, max_value=20, step=1)
region = st.number_input("Region", min_value=0, max_value=20, step=1)
inventory = st.number_input("Current Inventory Level", min_value=0, max_value=5000, step=100)
units_sold = st.number_input("Units Sold", min_value=0, max_value=1000, step=10)
units_ordered = st.number_input("Units Ordered", min_value=0, max_value=1000, step=10)
price = st.number_input("Price (₹)", min_value=1.0, max_value=1000.0, step=1.0)
discount = st.slider("Discount (%)", 0, 100, 10)
promotion = st.selectbox("Promotion Applied?", [0, 1])
competitor_price = st.number_input("Competitor Price (₹)", min_value=1.0, max_value=1000.0, step=1.0)
epidemic = st.selectbox("Epidemic Active?", [0, 1])
month = st.selectbox("Month", list(range(1, 13)))
day = st.selectbox("Day", list(range(1, 32)))
weekday = st.selectbox("Weekday (0=Mon, 6=Sun)", list(range(0, 7)))

# ----------------------------------------
# ⛅ Weather Checkboxes
# ----------------------------------------
sunny = st.checkbox("Sunny")
rainy = st.checkbox("Rainy")
snowy = st.checkbox("Snowy")

# 🌦️ Seasonal Checkboxes
summer = st.checkbox("Summer")
winter = st.checkbox("Winter")

# ----------------------------------------
# 🛠️ Build input dictionary (All 21 features)
# ----------------------------------------
input_dict = {
    'Store ID': store_id,
    'Product ID': product_id,
    'Category': category,
    'Region': region,
    'Inventory Level': inventory,
    'Units Sold': units_sold,
    'Units Ordered': units_ordered,
    'Price': price,
    'Discount': discount,
    'Promotion': promotion,
    'Competitor Pricing': competitor_price,
    'Epidemic': epidemic,
    'Month': month,
    'Day': day,
    'Weekday': weekday,
    'Weather Condition_Sunny': int(sunny),
    'Weather Condition_Rainy': int(rainy),
    'Weather Condition_Snowy': int(snowy),
    'Seasonality_Summer': int(summer),
    'Seasonality_Winter': int(winter),
    'Seasonality_Spring': 0  # Always include this to match training features
}

# ----------------------------------------
# 📊 Reorder input to match training
# ----------------------------------------
input_df = pd.DataFrame([input_dict])[feature_order]

# ----------------------------------------
# 🔮 Make Prediction
# ----------------------------------------
if st.button("Predict Demand"):
    prediction = model.predict(input_df)[0]
    st.success(f"📦 Predicted Demand: **{int(prediction)} units**")
