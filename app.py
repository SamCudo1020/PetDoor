import streamlit as st
from streamlit_webrtc import webrtc_streamer
import paho.mqtt.client as mqtt
import cv2
import numpy as np

# Configuración de página
st.set_page_config(page_title="PetGuard Hub", page_icon="🐾", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #4CAF50; color: white; }
    .status-box { padding: 20px; border-radius: 15px; background: white; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🐾 PetGuard: Detector de Mascotas")

# --- LÓGICA MQTT ---
MQTT_BROKER = "broker.hivemq.com" # Broker público para pruebas
TOPIC_DETECTION = "petguard/detection"
TOPIC_DOOR = "petguard/door"

client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 60)

# --- INTERFAZ ---
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="status-box"><h3>Cámara en Vivo</h3></div>', unsafe_allow_html=True)
    # Aquí se integraría el modelo de detección (YOLO/Mediapipe)
    webrtc_streamer(key="pet-detector")

with col2:
    st.markdown('<div class="status-box"><h3>Estado de la Puerta</h3></div>', unsafe_allow_html=True)
    
    if st.button("Detectar Gato (Simulado)"):
        client.publish(TOPIC_DETECTION, "CAT_DETECTED")
        st.success("¡Gato detectado! Enviando señal a Wokwi...")

    st.write("---")
    
    col_open, col_close = st.columns(2)
    if col_open.button("🔓 ABRIR"):
        client.publish(TOPIC_DOOR, "OPEN")
        st.info("Abriendo pistón...")
        
    if col_close.button("🔒 CERRAR"):
        client.publish(TOPIC_DOOR, "CLOSE")
        st.warning("Cerrando pistón...")
