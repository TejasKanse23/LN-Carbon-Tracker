import streamlit as st
import requests

def show():
    st.title("🚗 Predict Emission")
    st.markdown("Enter the shipment details below to predict the carbon emissions using the backend API.")
    
    with st.form("predict_emission_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            origin = st.text_input("Origin", placeholder="e.g., Mumbai")
            destination = st.text_input("Destination", placeholder="e.g., Pune")
            
        with col2:
            vehicle_number = st.text_input("Vehicle Number", placeholder="e.g., MP-53-LM-3543")
            
        submit_button = st.form_submit_button("Predict Emission")
        
    if submit_button:
        if not origin or not destination or not vehicle_number:
            st.warning("Please fill in all the fields.")
            return
            
        payload = {
            "origin": origin.strip(),
            "destination": destination.strip(),
            "vehicle_number": vehicle_number.strip()
        }
        
        api_url = "http://localhost:8000/predict-emission"
        
        with st.spinner("Predicting emission..."):
            try:
                response = requests.post(api_url, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    emission = data.get("predicted_emission_kg_co2e")
                    
                    if emission is not None:
                        st.success("Prediction Successful!")
                        
                        st.metric(
                            label="Predicted Emission (kg CO₂e)",
                            value=f"{emission:.2f}"
                        )
                    else:
                        st.error("Invalid response format from API.")
                        st.write("Response:", data)
                        
                else:
                    st.error(f"API Request Failed with status code: {response.status_code}")
                    st.write("Response:", response.text)
                    
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the API: {e}")
                st.info("Ensure that the backend API is running at `http://localhost:8000`.")
