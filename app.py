import streamlit as st
import numpy as np
import pandas as pd
import pickle
import os
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import plotly.express as px

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="House Price Predictor", page_icon="🏡", layout="wide")

# -------------------------------
# PREMIUM CSS
# -------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #1d2671, #c33764);
    color: white;
}
.card {
    background: rgba(255,255,255,0.1);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    margin-bottom: 20px;
}
.title {
    text-align: center;
    font-size: 50px;
    font-weight: bold;
    color: #00FFD1;
}
.subtitle {
    text-align: center;
    font-size: 20px;
    color: #ddd;
}
.stButton>button {
    background: linear-gradient(90deg, #00FFD1, #00C9A7);
    color: black;
    font-size: 20px;
    border-radius: 12px;
}
.stButton>button:hover {
    transform: scale(1.08);
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #141E30, #243B55);
    color: white;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# LOAD MODEL
# -------------------------------
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model', 'model.pkl'))

if not os.path.exists(model_path):
    st.error("Model not found!")
    st.stop()

with open(model_path, 'rb') as f:
    model = pickle.load(f)

# -------------------------------
# HEADER
# -------------------------------
st.markdown("<div class='title'>🏡 House Price Predictor</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>✨ AI + Geospatial Intelligence</div>", unsafe_allow_html=True)

st.markdown("---")

# -------------------------------
# SIDEBAR INPUT
# -------------------------------
st.sidebar.header("🏠 Enter Details")

overall_qual = st.sidebar.slider("Overall Quality", 1, 10, 5)
gr_liv_area = st.sidebar.number_input("Living Area", 500, 5000, 1500)
garage_cars = st.sidebar.slider("Garage Cars", 0, 5, 1)

st.sidebar.header("🌍 Location")
lat = st.sidebar.number_input("Latitude", 40.0, 42.0, 41.0)
lon = st.sidebar.number_input("Longitude", -94.0, -92.0, -93.0)

# -------------------------------
# METRICS
# -------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<div class='card'>🏠 Quality<br><h2>{overall_qual}</h2></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='card'>📏 Area<br><h2>{gr_liv_area}</h2></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='card'>🚗 Garage<br><h2>{garage_cars}</h2></div>", unsafe_allow_html=True)

# -------------------------------
# MAP
# -------------------------------
st.markdown("<div class='card'><h3>📍 Location Map</h3></div>", unsafe_allow_html=True)

m = folium.Map(location=[lat, lon], zoom_start=12)
folium.Marker([lat, lon], popup="Your Property").add_to(m)
st_folium(m, width=800, height=400)

# -------------------------------
# HEATMAP
# -------------------------------
@st.cache_data
def heat(lat, lon):
    return [[lat + np.random.uniform(-0.02,0.02),
             lon + np.random.uniform(-0.02,0.02),
             np.random.randint(100000,500000)] for _ in range(50)]

st.markdown("<div class='card'><h3>🌡️ Price Heatmap</h3></div>", unsafe_allow_html=True)

m2 = folium.Map(location=[lat, lon], zoom_start=12)
HeatMap(heat(lat, lon)).add_to(m2)
st_folium(m2, width=800, height=400)

# -------------------------------
# MARKERS
# -------------------------------
@st.cache_data
def markers(lat, lon):
    return [(lat + np.random.uniform(-0.01,0.01),
             lon + np.random.uniform(-0.01,0.01),
             np.random.randint(100000,500000)) for _ in range(10)]

st.markdown("<div class='card'><h3>📍 Nearby Houses</h3></div>", unsafe_allow_html=True)

m3 = folium.Map(location=[lat, lon], zoom_start=12)
for p in markers(lat, lon):
    folium.Marker([p[0], p[1]], popup=f"₹ {p[2]}").add_to(m3)

st_folium(m3, width=800, height=400)

# -------------------------------
# ANALYTICS CHARTS
# -------------------------------
st.markdown("<div class='card'><h3>📊 Market Insights</h3></div>", unsafe_allow_html=True)

@st.cache_data
def generate_data():
    return pd.DataFrame({
        "Area": np.random.randint(500, 4000, 100),
        "Quality": np.random.randint(1, 10, 100),
        "Price": np.random.randint(100000, 500000, 100)
    })

df_chart = generate_data()

col1, col2 = st.columns(2)

with col1:
    fig1 = px.scatter(df_chart, x="Area", y="Price", title="Price vs Area", color="Price")
    st.plotly_chart(fig1, width='stretch')

with col2:
    fig2 = px.box(df_chart, x="Quality", y="Price", title="Price by Quality")
    st.plotly_chart(fig2, width='stretch')

# -------------------------------
# PREDICTION
# -------------------------------
st.markdown("---")

if st.button("🔮 Predict Price"):
    with st.spinner("Calculating..."):
        input_data = pd.DataFrame({
            'OverallQual': [overall_qual],
            'GrLivArea': [gr_liv_area],
            'GarageCars': [garage_cars]
        })

        prediction = model.predict(input_data)

        st.markdown(
            f"<div class='card'><h2>💰 ₹ {prediction[0]:,.0f}</h2></div>",
            unsafe_allow_html=True
        )

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("<center>🚀 Built with ❤️ | Premium AI Project</center>", unsafe_allow_html=True)