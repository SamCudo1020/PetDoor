import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import paho.mqtt.client as mqtt
from ultralytics import YOLO
import cv2
import numpy as np

# Configuración de página
st.set_page_config(page_title="PetGuard Pro", page_icon="🐾", layout="wide")

# Estilo Personalizado
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 15px; height: 3.5em; background-color: #4A90E2; color: white; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #357ABD; border: none; }
    .reportview-container .main .block-container { padding-top: 2rem; }
    .status-card { padding: 20px; border-radius: 15px; background: white; box-shadow: 0px 4px 12px rgba(0,0,0,0.08); margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# Inicializar Modelo YOLO (Carga ligera)
@st.cache_resource
def load_model():
    return YOLO('yolov8n.pt')

model = load_model()

# Configuración MQTT
MQTT_BROKER = "broker.hivemq.com"
client = mqtt.Client()

try:
    client.connect(MQTT_BROKER, 1883, 60)
except:
    st.error("Error conectando al servidor MQTT")

# Clase para procesar video y detectar gatos
class CatDetector(VideoTransformerBase):
    def __init__(self):
        self.last_detection = False

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # Predicción de YOLO
        results = model(img, verbose=False)[0]
        detected = False
        
        for box in results.boxes:
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            name = model.names[cls]
            
            # Filtro estricto: Solo gatos con más del 60% de confianza
            if name == "cat" and conf > 0.6:
                detected = True
                # Dibujar recuadro en la pantalla
                b = box.xyxy[0].cpu().numpy().astype(int)
                cv2.rectangle(img, (b[0], b[1]), (b[2], b[3]), (0, 255, 0), 2)
                cv2.putText(img, f"Gato {conf:.2f}", (b[0], b[1]-10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        if detected and not self.last_detection:
            client.publish("petguard/detection", "CAT_DETECTED")
            self.last_detection = True
        elif not detected:
            self.last_detection = False

        return img

# --- INTERFAZ DE USUARIO ---
st.title("🐾 PetGuard Pro: Smart Access")
st.markdown("---")

col_cam, col_ctrl = st.columns([2, 1])

with col_cam:
    st.markdown('<div class="status-card"><h4>📷 Escáner de Entrada</h4>', unsafe_allow_html=True)
    webrtc_streamer(key="cat-scanner", video_transformer_factory=CatDetector)
    st.markdown('</div>', unsafe_allow_html=True)

with col_ctrl:
    st.markdown('<div class="status-card">', unsafe_allow_html=True)
    st.subheader("🛠️ Control de Acceso")
    
    if st.button("🔓 ABRIR PUERTA (PISTÓN)"):
        client.publish("petguard/door", "OPEN")
        st.toast("Puerta abierta con éxito", icon="✅")
        
    st.write("")
    
    if st.button("🔒 BLOQUEAR PUERTA"):
        client.publish("petguard/door", "CLOSE")
        st.toast("Puerta cerrada", icon="🔒")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="status-card">', unsafe_allow_html=True)
    st.info("💡 **Consejo:** Mantén la cámara fija frente a la puerta para una mejor detección.")
    st.markdown('</div>', unsafe_allow_html=True)
