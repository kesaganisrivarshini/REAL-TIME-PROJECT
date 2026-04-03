import streamlit as st
import joblib
import pandas as pd

# Load model and columns
model = joblib.load("accident_model.pkl")
columns = joblib.load("feature_columns.pkl")

# Title
st.title("🚦 Traffic Accident Prediction")

# ---------------- INPUTS ----------------
speed = st.number_input("Enter Speed (km/h)", min_value=0, max_value=150)

weather = st.selectbox("Weather", ["Sunny", "Rainy"])
traffic = st.selectbox("Traffic", ["Low", "High"])

# ---------------- SPEED RISK INDICATOR ----------------
if speed > 80:
    st.error("🚨 High Risk Speed")
elif speed > 50:
    st.warning("⚠️ Moderate Risk Speed")
else:
    st.success("✅ Safe Speed")

# ---------------- PREDICTION ----------------
if st.button("Predict"):

    # Input dictionary (MATCH dataset column names)
    input_data = {
        "speed": speed,
        "weather": weather,
        "traffic": traffic
    }

    # Convert to DataFrame
    input_df = pd.DataFrame([input_data])

    # Apply same preprocessing
    input_df = pd.get_dummies(input_df)

    # Match training columns
    input_df = input_df.reindex(columns=columns, fill_value=0)

    # Model prediction
    result = model.predict(input_df)

    # ---------------- FINAL OUTPUT ----------------
    
    # 🔥 Combine ML + Real-world logic
    if speed > 90:
        st.error("🚨 Very High Chance of Accident")
    
    elif speed > 70 and traffic == "High":
        st.error("🚨 Accident Likely (High Speed + Traffic)")
    
    elif speed > 50:
        st.warning("⚠️ Moderate Risk of Accident")
    
    else:
        if result[0] == 1:
            st.error("🚨 Accident Likely")
        else:
            st.success("✅ No Accident")

    # ---------------- ANALYSIS ----------------
    st.subheader("📊 Risk Analysis")

    if speed < 30:
        st.write("Low risk due to low speed.")
    elif speed < 60:
        st.write("Moderate risk. Stay alert.")
    else:
        st.write("High risk. Accidents are more severe at high speeds.")