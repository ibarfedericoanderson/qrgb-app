# QRGB Generator
# © 2025 Ibar Federico Anderson, Ph.D. M.Des., Industrial Designer. All rights reserved.
#
# This work is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0).
# To view a copy of this license, visit https://creativecommons.org/licenses/by/4.0/
# 🔗 You are free to:
#    • Share — copy and redistribute the material in any medium or format
#    • Adapt — remix, transform, and build upon the material for any purpose, even commercially.
# Under the following terms:
#    • Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
#    • No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.
#
# Author Profiles:
#    [Icono Google Scholar] Google Scholar - https://scholar.google.com/citations?user=mXD4RFUAAAAJ&hl=en
#    [Icono ORCID] ORCID - https://orcid.org/0000-0002-9732-3660
#    [Icono ResearchGate] ResearchGate - https://www.researchgate.net/profile/Ibar-Anderson
# Symbols: © (Copyright) | CC (Creative Commons) | BY (Attribution)
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
        font-size: 48px;
        font-weight: 700;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 40px;
    }
    .subtitle {
        font-size: 36px;
        font-weight: 700;
        color: #34495e;
        margin-top: 40px;
        margin-bottom: 30px;
    }
    .stButton>button {
        border-radius: 15px;
        font-size: 28px;
        font-weight: 700;
        padding: 25px 50px;
        width: 100%;
        border: none;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 80px;
    }
    .profile-box {
        background-color: #f8f9fa;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-top: 25px;
        margin-bottom: 40px;
    }
    .profile-box h2 {
        font-size: 32px;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 20px;
    }
    .profile-box p {
        font-size: 18px;
        color: #34495e;
        margin-bottom: 10px;
    }
    .profile-box a {
        color: #3498db;
        text-decoration: none;
        font-weight: 700;
    }
    .profile-box a:hover {
        color: #2980b9;
    }
    .symbol {
        font-size: 24px;
        margin-right: 10px;
    }
    /* Botón Codificar QRGB */
    button[kind="encode"] {
        background-color: #3498db !important;
        color: white !important;
    }
    button[kind="encode"]:hover {
        background-color: #2980b9 !important;
    }
    /* Botón Decodificar QRGB */
    button[kind="decode"] {
        background-color: #2ecc71 !important;
        color: white !important;
    }
    button[kind="decode"]:hover {
        background-color: #27ae60 !important;
    }
    /* Botón Generar QRGB */
    button[kind="generate"] {
        background-color: #3498db !important;
        color: white !important;
    }
    button[kind="generate"]:hover {
        background-color: #2980b9 !important;
    }
    /* Botón Analizar QRGB */
    button[kind="analyze"] {
        background-color: #2ecc71 !important;
        color: white !important;
    }
    button[kind="analyze"]:hover {
        background-color: #27ae60 !important;
    }
    /* Botón Descargar QRGB */
    button[kind="download"] {
        background-color: #9b59b6 !important;
        color: white !important;
    }
    button[kind="download"]:hover {
        background-color: #8e44ad !important;
    }
    /* Botón Volver */
    button[kind="back"] {
        background-color: #7f8c8d !important;
        color: white !important;
    }
    button[kind="back"]:hover {
        background-color: #95a5a6 !important;
    }
    /* Botones Abrir URL */
    button[kind="url-red"] {
        background-color: #e74c3c !important;
        color: white !important;
    }
    button[kind="url-red"]:hover {
        background-color: #c0392b !important;
    }
    button[kind="url-green"] {
        background-color: #2ecc71 !important;
        color: white !important;
    }
    button[kind="url-green"]:hover {
        background-color: #27ae60 !important;
    }
    button[kind="url-blue"] {
        background-color: #3498db !important;
        color: white !important;
    }
    button[kind="url-blue"]:hover {
        background-color: #2980b9 !important;
    }
    .stTextInput>label, .stFileUploader>label {
        font-size: 24px;
        font-weight: 700;
        color: #2c3e50;
    }
    .result-box {
        background-color: #f8f9fa;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-top: 25px;
    }
    .color-red {
        color: #e74c3c;
        font-weight: 700;
        font-size: 26px;
    }
    .color-green {
        color: #2ecc71;
        font-weight: 700;
        font-size: 26px;
    }
    .color-blue {
        color: #3498db;
        font-weight: 700;
        font-size: 26px;
    }
    .symbol {
        font-size: 40px;
        margin-right: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Sección de presentación del creador
def show_creator_profile():
    st.markdown('<div class="profile-box">', unsafe_allow_html=True)
    st.markdown('<h2>👤 About the Creator</h2>', unsafe_allow_html=True)
    st.markdown('<p>© 2025 <strong>Ibar Federico Anderson, Ph.D. M.Des., Industrial Designer</strong>. All rights reserved.</p>', unsafe_allow_html=True)
    
    # Google Scholar con emoji de graduación
    st.markdown(
        '<p>'
        '🎓 <strong>Google Scholar:</strong> <a href="https://scholar.google.com/citations?user=mXD4RFUAAAAJ&hl=en" target="_blank">Visit Profile</a>'
        '</p>',
        unsafe_allow_html=True
    )
    
    # ORCID (sin cambios)
    st.markdown(
        '<p>'
        '<img src="https://upload.wikimedia.org/wikipedia/commons/0/06/ORCID_iD.svg" width="20" height="20" style="vertical-align: middle; margin-right: 10px;">'
        '<strong>ORCID:</strong> <a href="https://orcid.org/0000-0002-9732-3660" target="_blank">Visit Profile</a>'
        '</p>',
        unsafe_allow_html=True
    )
    
    # ResearchGate (sin cambios)
    st.markdown(
        '<p>'
        '<img src="https://upload.wikimedia.org/wikipedia/commons/5/5e/ResearchGate_icon_SVG.svg" width="20" height="20" style="vertical-align: middle; margin-right: 10px;">'
        '<strong>ResearchGate:</strong> <a href="https://www.researchgate.net/profile/Ibar-Anderson" target="_blank">Visit Profile</a>'
        '</p>',
        unsafe_allow_html=True
    )
    
    # Creative Commons con emoji de libro abierto
    st.markdown(
        '<p>'
        '📖 <strong>Creative Commons:</strong> This work is licensed under the <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank">CC BY 4.0 License</a>.'
        '</p>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Funciones de QR modificadas para logo opcional
def create_qr(data, color, qr_version=10, box_size=10):
    qr = qrcode.QRCode(version=qr_version, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=box_size, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=color, back_color="white").convert('RGBA')
    return img

def create_qr_with_logo(data, color, logo_path, qr_version=10, box_size=10):
    img = create_qr(data, color, qr_version, box_size)
    if logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        basewidth = img.size[0] // 4
        wpercent = (basewidth / float(logo.size[0]))
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.LANCZOS)
        pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
        img.paste(logo, pos, logo)
    return img

def combine_qr_images(img1, img2, img3, logo_path=None):
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
    if logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        basewidth = final_image.size[0] // 4
        wpercent = (basewidth / float(logo.size[0]))
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.LANCZOS)
        pos = ((final_image.size[0] - logo.size[0]) // 2, (final_image.size[1] - logo.size[1]) // 2)
        final_image.paste(logo, pos, logo)
    return final_image

def generate_qrgb(red_data, green_data, blue_data, logo_path=None, mode='link'):
    qr_version = 10 if mode == 'link' else 3
    box_size = 10 if mode == 'link' else 20
    if logo_path:
        img_red = create_qr_with_logo(red_data, "red", logo_path, qr_version, box_size)
        img_green = create_qr_with_logo(green_data, "green", logo_path, qr_version, box_size)
        img_blue = create_qr_with_logo(blue_data, "blue", logo_path, qr_version, box_size)
    else:
        img_red = create_qr(red_data, "red", qr_version, box_size)
        img_green = create_qr(green_data, "green", qr_version, box_size)
        img_blue = create_qr(blue_data, "blue", qr_version, box_size)
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
    # Mostrar perfil del creador
    show_creator_profile()
    # Pantalla inicial
    if 'page' not in st.session_state:
        st.session_state.page = "inicio"
    if st.session_state.page == "inicio":
        st.markdown('<div class="title">Generador QRGB</div>', unsafe_allow_html=True)
        st.write("Crea y decodifica códigos QRGB con un diseño profesional y minimalista.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔒 Codificar QRGB", key="encode_btn", help="Codificar un nuevo QRGB", type="primary"):
                st.session_state.page = "codificar"
        with col2:
            if st.button("🔓 Decodificar QRGB", key="decode_btn", help="Decodificar un QRGB existente", type="primary"):
                st.session_state.page = "decodificar"
    # Codificar QRGB
    elif st.session_state.page == "codificar":
        st.markdown('<div class="subtitle">Codificar QRGB</div>', unsafe_allow_html=True)
        st.write("Ingresa los datos y sube un logo (opcional) para generar tu QRGB personalizado.")
        col1, col2 = st.columns([2, 1])
        with col1:
            red_data = st.text_input("🔗 Capa Roja", placeholder="Texto o URL", key="red_input")
            green_data = st.text_input("🔗 Capa Verde", placeholder="Texto o URL", key="green_input")
            blue_data = st.text_input("🔗 Capa Azul", placeholder="Texto o URL", key="blue_input")
        with col2:
            logo_file = st.file_uploader("🖼️ Cargar Logo (Opcional)", type=['png', 'jpg', 'jpeg'], key="logo_upload")
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            if st.button("📥 Generar QRGB", key="generate_btn", help="Generar el QRGB con los datos proporcionados", type="primary"):
                if all([red_data, green_data, blue_data]):
                    try:
                        logo_path = None
                        if logo_file:
                            logo_path = os.path.join(FOLDER_PATH, "temp_logo.png")
                            with open(logo_path, "wb") as f:
                                f.write(logo_file.getbuffer())
                        mode = 'link' if any('http' in text.lower() for text in [red_data, green_data, blue_data]) else 'text'
                        combined_img = generate_qrgb(red_data, green_data, blue_data, logo_path, mode)
                        st.image(combined_img, caption="QRGB Generado", width=400)
                        st.success("¡QRGB generado con éxito!")
                        buf = BytesIO()
                        combined_img.save(buf, format="PNG")
                        byte_im = buf.getvalue()
                        st.download_button(label="💾 Descargar QRGB", data=byte_im, file_name="qrgb.png", mime="image/png", key="download_btn", type="primary")
                        if logo_path:
                            os.remove(logo_path)
                    except Exception as e:
                        logger.error(f"Error generating QRGB: {str(e)}")
                        st.error(f"Error: {str(e)}")
                else:
                    st.error("Completa todos los campos de texto.")
        with col_btn2:
            if st.button("🏠 Volver", key="back_encode_btn", help="Volver al inicio", type="primary"):
                st.session_state.page = "inicio"
    # Decodificar QRGB
    elif st.session_state.page == "decodificar":
        st.markdown('<div class="subtitle">Decodificar QRGB</div>', unsafe_allow_html=True)
        st.write("Sube un QRGB para extraer la información de cada capa.")
        qr_file = st.file_uploader("🖼️ Cargar QRGB", type=['png'], key="qr_upload")
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            if qr_file and st.button("🔍 Analizar QRGB", key="decode_qr_btn", help="Decodificar el QRGB cargado", type="primary"):
                try:
                    qr_path = os.path.join(FOLDER_PATH, "temp_qr.png")
                    with open(qr_path, "wb") as f:
                        f.write(qr_file.getbuffer())
                    data_red, data_green, data_blue = manual_decode_superposed_qr(qr_path)
                    st.image(qr_path, caption="QRGB Cargado", width=400)
                    with st.container():
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        st.write("**Resultados:**")
                        st.markdown(f'<span class="color-red"><span class="symbol">🔗</span> Capa Roja:</span> {data_red}', unsafe_allow_html=True)
                        if data_red and ('http://' in data_red or 'https://' in data_red):
                            if st.button("🌐 Abrir URL Roja", key="url_red_btn", help="Abrir la URL de la capa roja", type="primary"):
                                webbrowser.open(data_red)
                        st.markdown(f'<span class="color-green"><span class="symbol">🔗</span> Capa Verde:</span> {data_green}', unsafe_allow_html=True)
                        if data_green and ('http://' in data_green or 'https://' in data_green):
                            if st.button("🌐 Abrir URL Verde", key="url_green_btn", help="Abrir la URL de la capa verde", type="primary"):
                                webbrowser.open(data_green)
                        st.markdown(f'<span class="color-blue"><span class="symbol">🔗</span> Capa Azul:</span> {data_blue}', unsafe_allow_html=True)
                        if data_blue and ('http://' in data_blue or 'https://' in data_blue):
                            if st.button("🌐 Abrir URL Azul", key="url_blue_btn", help="Abrir la URL de la capa azul", type="primary"):
                                webbrowser.open(data_blue)
                        st.markdown('</div>', unsafe_allow_html=True)
                    os.remove(qr_path)
                except Exception as e:
                    st.error(f"Error al decodificar: {str(e)}")
        with col_btn2:
            if st.button("🏠 Volver", key="back_decode_btn", help="Volver al inicio", type="primary"):
                st.session_state.page = "inicio"

if __name__ == '__main__':
    main()
