
import streamlit as st
import pandas as pd
import numpy as np
import pickle

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("🏢 Building Energy Efficiency Predictor")
st.markdown("Predict heating load and energy class for any building.")

st.sidebar.header("Building Parameters")
compactness = st.sidebar.slider("Relative Compactness", 0.62, 0.98, 0.75)
surface_area = st.sidebar.slider("Surface Area (m²)", 514.0, 808.0, 660.0)
wall_area = st.sidebar.slider("Wall Area (m²)", 245.0, 416.5, 318.0)
roof_area = st.sidebar.slider("Roof Area (m²)", 110.0, 220.0, 147.0)
height = st.sidebar.slider("Overall Height (m)", 3.5, 7.0, 5.25)
glazing_area = st.sidebar.slider("Glazing Area", 0.0, 0.4, 0.1)
orientation = st.sidebar.selectbox("Orientation", [2, 3, 4, 5])
glazing_dist = st.sidebar.selectbox("Glazing Distribution", [0, 1, 2, 3, 4, 5])

glazing_ratio = glazing_area / surface_area
volume_proxy = surface_area * height
wall_surface_ratio = wall_area / surface_area

def energy_class(load):
    if load < 10: return 'A ✅ Excellent'
    elif load < 20: return 'B 🟢 Good'
    elif load < 30: return 'C 🟡 Average'
    elif load < 40: return 'D 🟠 Below Average'
    else: return 'E 🔴 Poor — Retrofit Needed!'

features = ['relative_compactness','surface_area','wall_area','roof_area',
            'overall_height','orientation','glazing_area','glazing_distribution',
            'glazing_ratio','volume_proxy','wall_surface_ratio']

input_data = pd.DataFrame([[compactness, surface_area, wall_area, roof_area,
                            height, orientation, glazing_area, glazing_dist,
                            glazing_ratio, volume_proxy, wall_surface_ratio]],
                          columns=features)

if st.button("🔍 Predict Energy Load"):
    pred = model.predict(input_data)[0]
    label = energy_class(pred)
    col1, col2 = st.columns(2)
    col1.metric("Heating Load", f"{pred:.2f} kWh/m²")
    col2.metric("Energy Class", label)
    if pred > 30:
        st.warning("⚠️ This building is a strong candidate for energy retrofit!")
    else:
        st.balloons()
        st.success("✅ This building has good energy performance!")
