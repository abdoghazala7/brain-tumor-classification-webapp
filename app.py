import streamlit as st
from PIL import Image
import requests

API_URL = "https://abdoghazala7-brain-tumor-classification-api.hf.space/predict"

# --- Page Configuration ---
st.set_page_config(
    page_title="NeuroScan AI | Brain Tumor Detection",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS (Styling) ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stFileUploaderFile"] {display: none;}
    
    .result-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
    }
    .result-title { font-size: 18px; color: #555; margin-bottom: 5px; }
    .result-value { font-size: 32px; font-weight: bold; color: #2c3e50; margin: 0; }
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #4caf50, #8bc34a); }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.freepik.com/premium-photo/doctor-examining-brain-scan-smartphone-hospital_116317-58405.jpg", width=200)
    st.title("NeuroScan AI")
    st.markdown("---")
    
    try:
        health_check = requests.get("https://abdoghazala7-brain-tumor-classification-api.hf.space/")
        if health_check.status_code == 200:
            st.success("🟢 API System Online")
        else:
            st.error("🔴 API Error")
    except:
        st.error("🔴 API Offline")
    
    st.markdown("---")
    st.markdown("Created by **Abdo Ghazala**")

# --- Main App Logic ---
st.write("# 🧠 Brain Tumor Classification System")
st.markdown("Upload a brain MRI scan to detect and classify potential tumors via our Secure API.")
st.markdown("---")

col1, col2 = st.columns([1, 1.5], gap="large")

with col1:
    st.subheader("📤 Image Upload")
    uploaded_file = st.file_uploader(
        "Drag and drop or click to upload", 
        type=["jpg", "jpeg", "png", "bmp", "webp", "tiff"]
    )
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="MRI Scan Preview", use_container_width=True)

with col2:
    st.subheader("📊 Diagnostic Results")
    
    if uploaded_file:
        with st.spinner("📡 Sending data to AI Server..."):
            try:
                # Prepare file for API
                uploaded_file.seek(0)
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                
                # Call the API
                response = requests.post(API_URL, files=files)
                
                # Process Response
                if response.status_code == 200:
                    result = response.json()
                    predicted_class = result['prediction']
                    probabilities = result['confidence_scores']
                    
                    # --- Result Card ---
                    st.markdown(f"""
                    <div class="result-card">
                        <p class="result-title">AI Diagnosis</p>
                        <p class="result-value">{predicted_class.capitalize()}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # --- Probabilities ---
                    st.write("### Confidence Analysis")
                    sorted_probs = sorted(probabilities.items(), key=lambda item: item[1], reverse=True)
                    
                    for label, score in sorted_probs:
                        c1, c2, c3 = st.columns([2, 5, 1.5])
                        with c1:
                            if label == predicted_class: st.markdown(f"**{label.capitalize()}**")
                            else: st.markdown(f"{label.capitalize()}")
                        with c2: st.progress(score)
                        with c3: st.markdown(f"**{score*100:.1f}%**")
                    
                    # --- Warnings ---
                    st.markdown("---")
                    if predicted_class == "notumor":
                        st.success("✅ No tumor patterns detected.")
                    else:
                        st.warning(f"⚠️ Potential {predicted_class} detected.")
                        
                else:
                    st.error(f"Server Error: {response.status_code}")
                    st.json(response.json())

            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to the API Server.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    
    else:
        st.info("👈 Waiting for image upload...")

# --- Footer ---
st.markdown("---")
st.caption("⚠️ Medical Disclaimer: For educational purposes only.")