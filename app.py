import streamlit as st
from PIL import Image
import qrcode
import os
import cv2
import webbrowser
import logging
from pathlib import Path
from io import BytesIO

# Configuración inicial de la página (DEBE SER LO PRIMERO)
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

# Estilos CSS para una interfaz profesional
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f6fa;
        font-family: 'Arial', sans-serif;
    }
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 20px;
    }
    .subtitle {
        font-size: 24px;
        color: #34495e;
        margin-top: 30px;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 8px;
        font-size: 16px;
        padding: 10px 20px;
        width: 100%;
        border: none;
    }
    .stButton>button:hover {
        background-color: #2980b9;
    }
    .stTextInput>label {
        font-size: 16px;
        color: #2c3e50;
    }
    .stFileUploader>label {
        font-size: 16px;
        color: #2c3e50;
    }
    .result-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
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
    img_red.save(os.path.join(FOLDER_PATH, "qr_red.png"))
    img_green.save(os.path.join(FOLDER_PATH, "qr_green.png"))
    img_blue.save(os.path.join(FOLDER_PATH, "qr_blue.png"))
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
    # Pantalla inicial
    if 'page' not in st.session_state:
        st.session_state.page = "inicio"

    if st.session_state.page == "inicio":
        st.markdown('<div class="title">Generador QRGB</div>', unsafe_allow_html=True)
        st.write("Crea y decodifica códigos QR RGB con un diseño profesional y minimalista.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Codificar QR", key="encode_btn"):
                st.session_state.page = "codificar"
        with col2:
            if st.button("Decodificar QR", key="decode_btn"):
                st.session_state.page = "decodificar"

    # Codificar QR
    elif st.session_state.page == "codificar":
        st.markdown('<div class="subtitle">Codificar QR RGB</div>', unsafe_allow_html=True)
        st.write("Ingresa los datos y sube un logo para generar tu QR personalizado.")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            red_data = st.text_input("Capa Roja", placeholder="Texto o URL", key="red_input")
            green_data = st.text_input("Capa Verde", placeholder="Texto o URL", key="green_input")
            blue_data = st.text_input("Capa Azul", placeholder="Texto o URL", key="blue_input")
        with col2:
            logo_file = st.file_uploader("Cargar Logo", type=['png', 'jpg', 'jpeg'], key="logo_upload")

        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            if st.button("Generar QR", key="generate_btn"):
                if logo_file and all([red_data, green_data, blue_data]):
                    try:
                        logo_path = os.path.join(FOLDER_PATH, "temp_logo.png")
                        with open(logo_path, "wb") as f:
                            f.write(logo_file.getbuffer())
                        mode = 'link' if any('http' in text.lower() for text in [red_data, green_data, blue_data]) else 'text'
                        combined_img = generate_qrgb(red_data, green_data, blue_data, logo_path, mode)
                        st.image(combined_img, caption="QR RGB Generado", width=400)
                        st.success("¡QR generado con éxito!")

                        # Descarga
                        buf = BytesIO()
                        combined_img.save(buf, format="PNG")
                        byte_im = buf.getvalue()
                        st.download_button(label="Descargar QR", data=byte_im, file_name="qrgb.png", mime="image/png", key="download_btn")
                        os.remove(logo_path)
                    except Exception as e:
                        logger.error(f"Error generating QRGB: {str(e)}")
                        st.error(f"Error: {str(e)}")
                else:
                    st.error("Completa todos los campos y sube un logo.")
        with col_btn2:
            if st.button("Volver", key="back_encode_btn"):
                st.session_state.page = "inicio"

    # Decodificar QR
    elif st.session_state.page == "decodificar":
        st.markdown('<div class="subtitle">Decodificar QR RGB</div>', unsafe_allow_html=True)
        st.write("Sube un QR RGB para extraer la información de cada capa.")

        qr_file = st.file_uploader("Cargar QR RGB", type=['png'], key="qr_upload")
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            if qr_file and st.button("Decodificar QR", key="decode_qr_btn"):
                try:
                    qr_path = os.path.join(FOLDER_PATH, "temp_qr.png")
                    with open(qr_path, "wb") as f:
                        f.write(qr_file.getbuffer())
                    data_red, data_green, data_blue = manual_decode_superposed_qr(qr_path)
                    
                    st.image(qr_path, caption="QR RGB Cargado", width=400)
                    with st.container():
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        st.write("**Resultados:**")
                        st.markdown(f"- **Capa Roja:** {data_red}")
                        if data_red and ('http://' in data_red or 'https://' in data_red):
                            if st.button("Abrir URL Roja", key="url_red_btn"): webbrowser.open(data_red)
                        st.markdown(f"- **Capa Verde:** {data_green}")
                        if data_green and ('http://' in data_green or 'https://' in data_green):
                            if st.button("Abrir URL Verde", key="url_green_btn"): webbrowser.open(data_green)
                        st.markdown(f"- **Capa Azul:** {data_blue}")
                        if data_blue and ('http://' in data_blue or 'https://' in data_blue):
                            if st.button("Abrir URL Azul", key="url_blue_btn"): webbrowser.open(data_blue)
                        st.markdown('</div>', unsafe_allow_html=True)
                    os.remove(qr_path)
                except Exception as e:
                    st.error(f"Error al decodificar: {str(e)}")
        with col_btn2:
            if st.button("Volver", key="back_decode_btn"):
                st.session_state.page = "inicio"

if __name__ == '__main__':
    main()
