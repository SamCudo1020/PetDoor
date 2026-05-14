import streamlit as st
import cv2
import numpy as np
import paho.mqtt.client as mqtt

# Configuración de la interfaz
st.set_page_config(page_title="PetGuard Hub", page_icon="🐾", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main-card {
        padding: 30px;
        background-color: white;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center;
    }
    .stButton>button {
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Lógica MQTT
MQTT_BROKER = "broker.hivemq.com"
client = mqtt.Client()
try:
    client.connect(MQTT_BROKER, 1883, 60)
except:
    st.error("Error de conexión con el servidor MQTT")

st.title("🐾 PetGuard Pro")
st.write("Control inteligente de acceso para tu mascota")

# --- SECCIÓN DE CÁMARA ---
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("📸 Escáner de Mascota")
    
    # Este componente es mágico: abre la cámara del móvil automáticamente
    foto = st.camera_input("Captura a tu mascota en la puerta")

    if foto:
        st.success("✅ ¡Imagen capturada!")
        # Botón para simular que la IA confirmó que es un gato
        if st.button("🐈 VALIDAR GATO Y ENVIAR A WOKWI"):
            client.publish("petguard/detection", "CAT_DETECTED")
            st.toast("Señal enviada a la matriz LED", icon="✨")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("#")

# --- SECCIÓN DE CONTROL ---
col1, col2 = st.columns(2)

with col1:
    if st.button("🔓 ABRIR PUERTA", use_container_width=True):
        client.publish("petguard/door", "OPEN")
        st.balloons()
        st.toast("Pistón activado", icon="🔓")

with col2:
    if st.button("🔒 CERRAR PUERTA", use_container_width=True):
        client.publish("petguard/door", "CLOSE")
        st.toast("Puerta bloqueada", icon="🔒")
