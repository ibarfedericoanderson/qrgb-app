import streamlit as st
from PIL import Image
import qrcode
import os
import cv2
import webbrowser
import logging
from pathlib import Path

# Configuración de paths
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
FOLDER_PATH = os.path.join(BASE_PATH, 'qrgb_files')
LOG_PATH = os.path.join(FOLDER_PATH, 'qrgb.log')
os.makedirs(FOLDER_PATH, exist_ok=True)

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Funciones de generación de QR (sin cambios)
def create_qr_with_logo(data, color, logo_path, qr_version=10, box_size=10):
    qr = qrcode.QRCode(
        version=qr_version,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=4
    )
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

    data_red = img1.getdata()
    data_green = img2.getdata()
    data_blue = img3.getdata()

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
    if vertices_array is not None:
        return data
    return None

def manual_decode_superposed_qr(filename):
    superposed_img = Image.open(filename)
    superposed_data = superposed_img.getdata()

    size = superposed_img.size
    red_data = [(255, 255, 255, 255)] * len(superposed_data)
    green_data = [(255, 255, 255, 255)] * len(superposed_data)
    blue_data = [(255, 255, 255, 255)] * len(superposed_data)

    for i in range(len(superposed_data)):
        r, g, b, a = superposed_data[i]
        if r != 0:
            red_data[i] = (0, 0, 0, 255)
        if g != 0:
            green_data[i] = (0, 0, 0, 255)
        if b != 0:
            blue_data[i] = (0, 0, 0, 255)

    red_img = Image.new("RGBA", size)
    green_img = Image.new("RGBA", size)
    blue_img = Image.new("RGBA", size)

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

# Interfaz de Streamlit
def main():
    st.title("Generador QRGB")

    # Menú principal
    option = st.sidebar.selectbox("Selecciona una opción", ["Codificar QRGB", "Decodificar QRGB"])

    if option == "Codificar QRGB":
        st.header("Codificar QRGB")
        
        red_data = st.text_input("Texto para capa roja")
        green_data = st.text_input("Texto para capa verde")
        blue_data = st.text_input("Texto para capa azul")
        
        logo_file = st.file_uploader("Selecciona el archivo de logo", type=['png', 'jpg', 'jpeg'])
        
        if logo_file is not None and st.button("Generar QRGB"):
            if not all([red_data, green_data, blue_data]):
                st.error("Por favor, completa todos los campos de texto")
            else:
                try:
                    # Guardar el logo temporalmente
                    logo_path = os.path.join(FOLDER_PATH, "temp_logo.png")
                    with open(logo_path, "wb") as f:
                        f.write(logo_file.getbuffer())
                    
                    mode = 'link' if any('http' in text.lower() for text in [red_data, green_data, blue_data]) else 'text'
                    combined_img = generate_qrgb(red_data, green_data, blue_data, logo_path, mode)
                    
                    st.image(combined_img, caption="QRGB Generado", use_column_width=True)
                    st.success(f"QRGB generado correctamente. Guardado en: {FOLDER_PATH}")
                    
                    # Limpiar archivo temporal
                    os.remove(logo_path)
                except Exception as e:
                    logger.error(f"Error generating QRGB: {str(e)}")
                    st.error(f"Error al generar QRGB: {str(e)}")

    elif option == "Decodificar QRGB":
        st.header("Decodificar QRGB")
        
        qr_file = st.file_uploader("Selecciona el archivo QRGB", type=['png'])
        
        if qr_file is not None and st.button("Decodificar"):
            try:
                # Guardar el QR temporalmente
                qr_path = os.path.join(FOLDER_PATH, "temp_qr.png")
                with open(qr_path, "wb") as f:
                    f.write(qr_file.getbuffer())
                
                data_red, data_green, data_blue = manual_decode_superposed_qr(qr_path)
                
                st.image(qr_path, caption="QRGB Cargado", width=200)
                
                # Mostrar resultados
                st.write(f"**Capa Roja:** {data_red}")
                if data_red and ('http://' in data_red or 'https://' in data_red):
                    if st.button("Abrir URL Roja"):
                        webbrowser.open(data_red)
                
                st.write(f"**Capa Verde:** {data_green}")
                if data_green and ('http://' in data_green or 'https://' in data_green):
                    if st.button("Abrir URL Verde"):
                        webbrowser.open(data_green)
                
                st.write(f"**Capa Azul:** {data_blue}")
                if data_blue and ('http://' in data_blue or 'https://' in data_blue):
                    if st.button("Abrir URL Azul"):
                        webbrowser.open(data_blue)
                
                # Limpiar archivo temporal
                os.remove(qr_path)
            except Exception as e:
                st.error(f"Error al decodificar: {str(e)}")

if __name__ == '__main__':
    main()