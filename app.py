import streamlit as st
from PIL import Image
import qrcode
import os
import cv2
import webbrowser
import logging
from pathlib import Path
from io import BytesIO

# Configuración inicial de la página
st.set_page_config(page_title="Generador QRGB", page_icon=":barcode:", layout="wide")

# Configuración de paths
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
FOLDER_PATH = os.path.join(BASE_PATH, 'qrgb_files')
LOG_PATH = os.path.join(FOLDER_PATH, 'qrgb.log')
os.makedirs(FOLDER_PATH, exist_ok=True)

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Estilos CSS mejorados
st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    .title {
        font-size: 42px;
        font-weight: 900;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 40px;
        letter-spacing: 1px;
    }
    .subtitle {
        font-size: 28px;
        font-weight: 800;
        color: #34495e;
        margin: 40px 0;
    }
    .stButton>button {
        border-radius: 15px !important;
        font-size: 24px !important;
        font-weight: 800 !important;
        padding: 25px 40px !important;
        width: 100% !important;
        border: none !important;
        transition: all 0.3s ease !important;
        min-height: 80px;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    .btn-encode {
        background-color: #3498db !important;
        color: white !important;
    }
    .btn-encode:hover {
        background-color: #2980b9 !important;
        transform: scale(1.02) !important;
    }
    .btn-decode {
        background-color: #2ecc71 !important;
        color: white !important;
    }
    .btn-decode:hover {
        background-color: #27ae60 !important;
        transform: scale(1.02) !important;
    }
    .btn-back {
        background-color: #95a5a6 !important;
        color: white !important;
    }
    .btn-back:hover {
        background-color: #7f8c8d !important;
        transform: scale(1.02) !important;
    }
    .btn-red {
        background-color: #e74c3c !important;
        color: white !important;
    }
    .btn-green {
        background-color: #2ecc71 !important;
        color: white !important;
    }
    .btn-blue {
        background-color: #3498db !important;
        color: white !important;
    }
    .stTextInput>label, .stFileUploader>label {
        font-size: 22px !important;
        font-weight: 700 !important;
        color: #2c3e50 !important;
    }
    .result-box {
        background-color: #f8f9fa;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        margin: 30px 0;
    }
    .color-text {
        font-size: 24px !important;
        font-weight: 700 !important;
        margin: 15px 0 !important;
    }
    .color-red {
        color: #e74c3c !important;
    }
    .color-green {
        color: #2ecc71 !important;
    }
    .color-blue {
        color: #3498db !important;
    }
    .symbol {
        font-size: 32px !important;
        margin-right: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Funciones de QR (sin cambios)
def create_qr_with_logo(data, color, logo_path, qr_version=10, box_size=10):
    qr = qrcode.QRCode(version=qr_version, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=box_size, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=color, back_color="white").convert('RGBA')
    if not os.path.exists(logo_path):
        raise FileNotFoundError(f"Logo file not found: {logo_path}")
    logo = Image.open(logo_path).convert("RGBA")
    basewidth = img.size[0] // 4
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.LANCZOS)
    pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
    img.paste(logo, pos, logo)
    return img

def combine_qr_images(img1, img2, img3, logo_path):
    size = img1.size
    if img2.size != size or img3.size != size:
        raise ValueError("All QR images must be the same size")
    final_image = Image.new("RGBA", size, "black")
    data_red, data_green, data_blue = img1.getdata(), img2.getdata(), img3.getdata()
    new_data = []
    for i in range(len(data_red)):
        r1, g1, b1, a1 = data_red[i]
        red_pixel = (r1, g1, b1) != (255, 255, 255)
        r2, g2, b2, a2 = data_green[i]
        green_pixel = (r2, g2, b2) != (255, 255, 255)
        r3, g3, b3, a3 = data_blue[i]
        blue_pixel = (r3, g3, b3) != (255, 255, 255)
        if red_pixel and green_pixel and blue_pixel:
            new_data.append((255, 255, 255, 255))
        elif red_pixel and green_pixel:
            new_data.append((255, 255, 0, 255))
        elif red_pixel and blue_pixel:
            new_data.append((255, 0, 255, 255))
        elif green_pixel and blue_pixel:
            new_data.append((0, 255, 255, 255))
        elif red_pixel:
            new_data.append((255, 0, 0, 255))
        elif green_pixel:
            new_data.append((0, 255, 0, 255))
        elif blue_pixel:
            new_data.append((0, 0, 255, 255))
        else:
            new_data.append((0, 0, 0, 255))
    final_image.putdata(new_data)
    logo = Image.open(logo_path).convert("RGBA")
    basewidth = final_image.size[0] // 4
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.LANCZOS)
    pos = ((final_image.size[0] - logo.size[0]) // 2, (final_image.size[1] - logo.size[1]) // 2)
    final_image.paste(logo, pos, logo)
    return final_image

def generate_qrgb(red_data, green_data, blue_data, logo_path, mode):
    qr_version = 10 if mode == 'link' else 3
    box_size = 10 if mode == 'link' else 20
    img_red = create_qr_with_logo(red_data, "red", logo_path, qr_version, box_size)
    img_green = create_qr_with_logo(green_data, "green", logo_path, qr_version, box_size)
    img_blue = create_qr_with_logo(blue_data, "blue", logo_path, qr_version, box_size)
    combined_img = combine_qr_images(img_red, img_green, img_blue, logo_path)
    combined_img.save(os.path.join(FOLDER_PATH, "superposed_qr.png"))
    return combined_img

def read_qr(filename):
    img = cv2.imread(filename)
    detector = cv2.QRCodeDetector()
    data, vertices_array, _ = detector.detectAndDecode(img)
    return data if vertices_array is not None else None

def manual_decode_superposed_qr(filename):
    superposed_img = Image.open(filename)
    superposed_data = superposed_img.getdata()
    size = superposed_img.size
    red_data = [(255, 255, 255, 255)] * len(superposed_data)
    green_data = [(255, 255, 255, 255)] * len(superposed_data)
    blue_data = [(255, 255, 255, 255)] * len(superposed_data)
    for i in range(len(superposed_data)):
        r, g, b, a = superposed_data[i]
        if r != 0: red_data[i] = (0, 0, 0, 255)
        if g != 0: green_data[i] = (0, 0, 0, 255)
        if b != 0: blue_data[i] = (0, 0, 0, 255)
    red_img, green_img, blue_img = Image.new("RGBA", size), Image.new("RGBA", size), Image.new("RGBA", size)
    red_img.putdata(red_data)
    green_img.putdata(green_data)
    blue_img.putdata(blue_data)
    red_img.save(os.path.join(FOLDER_PATH, "decoded_red.png"))
    green_img.save(os.path.join(FOLDER_PATH, "decoded_green.png"))
    blue_img.save(os.path.join(FOLDER_PATH, "decoded_blue.png"))
    data_red = read_qr(os.path.join(FOLDER_PATH, "decoded_red.png"))
    data_green = read_qr(os.path.join(FOLDER_PATH, "decoded_green.png"))
    data_blue = read_qr(os.path.join(FOLDER_PATH, "decoded_blue.png"))
    return data_red, data_green, data_blue

# Interfaz principal
def main():
    if 'page' not in st.session_state:
        st.session_state.page = "inicio"
        
    if st.session_state.page == "inicio":
        st.markdown('<div class="title">🔳 Generador QRGB</div>', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center; font-size:24px; margin-bottom:50px;">Crea y decodifica códigos QRGB profesionales</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("🔷 Codificar QRGB", 
                     key="encode_btn",
                     help="Crear nuevo código QRGB",
                     on_click=lambda: st.session_state.update(page="codificar"),
                     type="primary")
        with col2:
            st.button("🔶 Decodificar QRGB", 
                     key="decode_btn",
                     help="Leer código QRGB existente",
                     on_click=lambda: st.session_state.update(page="decodificar"),
                     type="secondary")

    elif st.session_state.page == "codificar":
        st.markdown('<div class="subtitle">🔷 Codificar QRGB</div>', unsafe_allow_html=True)
        st.markdown('<div class="color-text">Ingresa los datos para cada capa:</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            red_data = st.text_input("🔴 Capa Roja", placeholder="Texto/URL para capa roja", key="red_input")
            green_data = st.text_input("🟢 Capa Verde", placeholder="Texto/URL para capa verde", key="green_input")
            blue_data = st.text_input("🔵 Capa Azul", placeholder="Texto/URL para capa azul", key="blue_input")
        with col2:
            logo_file = st.file_uploader("📁 Subir Logo", type=['png', 'jpg', 'jpeg'], key="logo_upload")
        
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            if st.button("🚀 Generar QRGB", 
                        key="generate_btn",
                        help="Generar código QRGB",
                        type="primary"):
                if logo_file and all([red_data, green_data, blue_data]):
                    try:
                        logo_path = os.path.join(FOLDER_PATH, "temp_logo.png")
                        with open(logo_path, "wb") as f:
                            f.write(logo_file.getbuffer())
                        mode = 'link' if any('http' in text.lower() for text in [red_data, green_data, blue_data]) else 'text'
                        combined_img = generate_qrgb(red_data, green_data, blue_data, logo_path, mode)
                        st.image(combined_img, caption="Tu QRGB Generado", width=400)
                        st.success("¡QRGB creado con éxito!")
                        buf = BytesIO()
                        combined_img.save(buf, format="PNG")
                        byte_im = buf.getvalue()
                        st.download_button("💾 Descargar QRGB", 
                                         data=byte_im, 
                                         file_name="qrgb.png",
                                         mime="image/png",
                                         use_container_width=True)
                        os.remove(logo_path)
                    except Exception as e:
                        logger.error(f"Error: {str(e)}")
                        st.error(f"Error: {str(e)}")
                else:
                    st.error("⚠️ Completa todos los campos y sube un logo")
        
        with col_btn2:
            st.button("↩️ Volver al Inicio", 
                     key="back_encode_btn",
                     help="Regresar a la pantalla principal",
                     type="secondary")

    elif st.session_state.page == "decodificar":
        st.markdown('<div class="subtitle">🔶 Decodificar QRGB</div>', unsafe_allow_html=True)
        st.markdown('<div class="color-text">Sube tu código QRGB:</div>', unsafe_allow_html=True)
        
        qr_file = st.file_uploader("📁 Subir QRGB", type=['png'], key="qr_upload")
        
        if qr_file:
            col_btn1, col_btn2 = st.columns([1, 1])
            with col_btn1:
                if st.button("🔍 Analizar QRGB", 
                            key="decode_qr_btn",
                            help="Decodificar el archivo subido",
                            type="primary"):
                    try:
                        qr_path = os.path.join(FOLDER_PATH, "temp_qr.png")
                        with open(qr_path, "wb") as f:
                            f.write(qr_file.getbuffer())
                        data_red, data_green, data_blue = manual_decode_superposed_qr(qr_path)
                        st.image(qr_path, caption="QRGB Analizado", width=400)
                        
                        with st.container():
                            st.markdown('<div class="result-box">', unsafe_allow_html=True)
                            st.markdown("### 📊 Resultados:")
                            
                            # Capa Roja
                            st.markdown(f'<div class="color-text color-red">🔴 Capa Roja: {data_red}</div>', unsafe_allow_html=True)
                            if data_red and ('http' in data_red):
                                st.button("🌐 Abrir URL Roja", 
                                        key="url_red_btn",
                                        on_click=lambda: webbrowser.open(data_red),
                                        type="primary",
                                        help="Abrir enlace de la capa roja")
                            
                            # Capa Verde
                            st.markdown(f'<div class="color-text color-green">🟢 Capa Verde: {data_green}</div>', unsafe_allow_html=True)
                            if data_green and ('http' in data_green):
                                st.button("🌐 Abrir URL Verde", 
                                        key="url_green_btn",
                                        on_click=lambda: webbrowser.open(data_green),
                                        type="primary",
                                        help="Abrir enlace de la capa verde")
                            
                            # Capa Azul
                            st.markdown(f'<div class="color-text color-blue">🔵 Capa Azul: {data_blue}</div>', unsafe_allow_html=True)
                            if data_blue and ('http' in data_blue):
                                st.button("🌐 Abrir URL Azul", 
                                        key="url_blue_btn",
                                        on_click=lambda: webbrowser.open(data_blue),
                                        type="primary",
                                        help="Abrir enlace de la capa azul")
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                        os.remove(qr_path)
                    except Exception as e:
                        st.error(f"❌ Error al decodificar: {str(e)}")
            
            with col_btn2:
                st.button("↩️ Volver al Inicio", 
                         key="back_decode_btn",
                         help="Regresar a la pantalla principal",
                         type="secondary")

if __name__ == '__main__':
    main()
