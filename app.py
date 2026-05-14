import streamlit as st
import cv2
import numpy as np
import paho.mqtt.client as mqtt

# Configuración Pro
st.set_page_config(page_title="PetGuard Lite", page_icon="🐈")

st.markdown("""
    <style>
    .stApp { background-color: #f5f7f9; }
    .status-card { padding: 20px; background: white; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# Conexión MQTT
MQTT_BROKER = "broker.hivemq.com"
client = mqtt.Client()
try:
    client.connect(MQTT_BROKER, 1883, 60)
except:
    st.error("Error de conexión MQTT")

st.title("🐾 PetGuard Lite")

col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("📸 Captura de Mascota")
    # Usamos el componente nativo de Streamlit (más estable)
    img_file = st.camera_input("Toma una foto de tu mascota")

    if img_file:
        # Convertir imagen a formato OpenCV
        file_bytes = np.asarray(bytearray(img_file.read()), dtype=uint8)
        frame = cv2.imdecode(file_bytes, 1)
        
        # Aquí simulamos la detección rápida
        # En una versión Pro usaríamos un CascadeClassifier de OpenCV
        st.success("✅ Foto recibida. Analizando...")
        
        # Botón para confirmar que es un gato (Manual para este prototipo rápido)
        if st.button("Confirmar Gato 🐈"):
            client.publish("petguard/detection", "CAT_DETECTED")
            st.toast("Señal enviada a Wokwi!")

with col2:
    st.markdown('<div class="status-card">', unsafe_allow_html=True)
    st.subheader("🚪 Control Puerta")
    
    if st.button("🔓 ABRIR PISTÓN", use_container_width=True):
        client.publish("petguard/door", "OPEN")
        st.balloons()
        
    if st.button("🔒 CERRAR PISTÓN", use_container_width=True):
        client.publish("petguard/door", "CLOSE")
    st.markdown('</div>', unsafe_allow_html=True)
