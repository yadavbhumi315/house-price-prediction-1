import streamlit as st
import numpy as np
import pandas as pd
import pickle
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import plotly.express as px
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Real Estate Advisor", layout="wide")

# ---------------- UI ----------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #667eea, #764ba2);
}
.block-container {
    background: rgba(255,255,255,0.95);
    padding: 2rem;
    border-radius: 20px;
}
h1, h2, h3, h4, h5, h6, p, label {
    color: black !important;
    font-weight: bold;
}
.stButton>button {
    background: linear-gradient(to right, #ff416c, #ff4b2b);
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 18px;
}
.kpi {
    background: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    font-size: 20px;
    color: black !important;
    font-weight: bold;
}
.kpi small {
    color: #555 !important;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
import os
import pickle
import streamlit as st

try:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    st.write("📂 BASE_DIR:", BASE_DIR)  # debug
    st.write("📁 Files in root:", os.listdir(BASE_DIR))  # debug
    
    model_path = os.path.join(BASE_DIR, "model", "model.pkl")
    st.write("🔍 Model path:", model_path)  # debug

    if not os.path.exists(model_path):
        st.error("❌ Model NOT FOUND")
        st.stop()

    model = pickle.load(open(model_path, "rb"))
    st.success("✅ Model Loaded Successfully")

except Exception as e:
    st.error(f"❌ Error: {e}")
    st.stop()
# ---------------- LOAD DATA ----------------
df = pd.read_csv("data/train.csv")

if 'lat' not in df.columns:
    df['lat'] = np.random.uniform(40, 42, len(df))
    df['lon'] = np.random.uniform(-94, -92, len(df))

# ---------------- TITLE ----------------
st.markdown("<h1>🏡 AI Real Estate Investment Advisor</h1>", unsafe_allow_html=True)
st.success("✨ Predict • Analyze • Decide")

# ---------------- INPUT ----------------
col1, col2 = st.columns(2)

with col1:
    overall_qual = st.slider("Quality", 1, 10, 5)
    gr_liv_area = st.number_input("Area (sq ft)", 500, 5000, 1500)
    garage_cars = st.slider("Garage", 0, 5, 1)

with col2:
    lat = st.number_input("Latitude", 40.0, 42.0, 41.0)
    lon = st.number_input("Longitude", -94.0, -92.0, -93.0)

# ---------------- MAP ----------------
st.subheader("📍 Location")
m = folium.Map(location=[lat, lon], zoom_start=12)
folium.Marker([lat, lon]).add_to(m)
st_folium(m, width=600, height=400, returned_objects=[])

# ---------------- CHART ----------------
st.subheader("📊 Market Analysis")
fig = px.scatter(df, x="GrLivArea", y="SalePrice")
st.plotly_chart(fig, width='stretch')

# ---------------- HEATMAP ----------------
st.subheader("🌡️ Price Heatmap")

@st.cache_resource
def create_heatmap(data):
    base_map = folium.Map(location=[41, -93], zoom_start=10)
    HeatMap(data, radius=8).add_to(base_map)
    return base_map

heat_data = df[['lat','lon','SalePrice']].dropna().values.tolist()
heat_map = create_heatmap(heat_data)
st_folium(heat_map, width=600, height=400, returned_objects=[])

# ---------------- PREDICTION ----------------
if st.button("🔮 Predict Price"):

    with st.spinner("🤖 Analyzing property..."):
        time.sleep(1)

        try:
            input_data = np.array([[overall_qual, gr_liv_area, garage_cars]])
            prediction = model.predict(input_data)
            price = float(prediction[0])

            st.success(f"💰 Estimated Price: ₹ {price:,.0f}")

            # ---------------- KPI ----------------
            st.subheader("📊 Key Insights")
            c1, c2, c3 = st.columns(3)

            c1.markdown(f"<div class='kpi'><small>💰 Price</small><br>₹ {price:,.0f}</div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='kpi'><small>🏠 Quality</small><br>{overall_qual}/10</div>", unsafe_allow_html=True)
            c3.markdown(f"<div class='kpi'><small>📐 Area</small><br>{gr_liv_area} sq ft</div>", unsafe_allow_html=True)

            # ---------------- SMART REPORT ----------------
            st.subheader("📄 Smart Property Report")
            price_per_sqft = price / gr_liv_area

            st.markdown(f"""
            - 💰 Price: ₹ {price:,.0f}  
            - 📐 Price/sqft: ₹ {price_per_sqft:,.2f}  
            - ⭐ Quality: {overall_qual}/10  
            """)

            # ---------------- LOCATION SCORE ----------------
            st.subheader("📍 Location Score")
            score = max(0, 100 - (abs(lat-41)*50 + abs(lon+93)*50))
            st.progress(score/100)
            st.write(f"Score: {int(score)}/100")

            # ---------------- PRICE COMPARISON ----------------
            st.subheader("📊 Price Comparison")
            avg_price = df['SalePrice'].mean()

            if price > avg_price:
                st.warning("Above market price")
            else:
                st.success("Below market price")

            # ---------------- AI RECOMMENDATION ----------------
            st.subheader("🧠 AI Recommendation")

            if price < avg_price and overall_qual >= 6:
                st.success("Great deal! Good quality at lower price.")
            elif price > avg_price and overall_qual < 5:
                st.error("Overpriced for its quality.")
            else:
                st.info("Balanced property.")

            # ---------------- DOWNLOAD ----------------
            report = f"Price: {price}, Area: {gr_liv_area}, Quality: {overall_qual}"
            st.download_button("📥 Download Report", report, file_name="report.txt")

        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")

# ---------------- FILTER ----------------
st.subheader("🔍 Explore Properties")

min_price = int(df['SalePrice'].min())
max_price = int(df['SalePrice'].max())

price_range = st.slider("Select Price Range", min_price, max_price, (min_price, max_price))
filtered = df[(df['SalePrice'] >= price_range[0]) & (df['SalePrice'] <= price_range[1])]

st.dataframe(filtered.head(20))

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("<center>🚀 Final Year AI Project - Production Ready</center>", unsafe_allow_html=True)