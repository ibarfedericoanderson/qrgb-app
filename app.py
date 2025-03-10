
import streamlit as st
from PIL import Image
import qrcode
import os
import cv2
import logging
from io import BytesIO
import tempfile
import numpy as np
import base64

# Configuración inicial de la página
st.set_page_config(
    page_title="Generador QRGB Online",
    page_icon="🔶",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Configuración de paths y directorios temporales
if not os.path.exists('qrgb_files'):
    os.makedirs('qrgb_files', exist_ok=True)
FOLDER_PATH = 'qrgb_files'

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
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
        font-size: 20px;
        font-weight: 700;
        padding: 15px 30px;
        width: 100%;
        border: none;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 60px;
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
    .stTextInput>label, .stFileUploader>label {
        font-size: 20px;
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
        font-size: 20px;
    }
    .color-green {
        color: #2ecc71;
        font-weight: 700;
        font-size: 20px;
    }
    .color-blue {
        color: #3498db;
        font-weight: 700;
        font-size: 20px;
    }
    .symbol {
        font-size: 24px;
        margin-right: 10px;
    }
    .url-button {
        background-color: #3498db;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        text-decoration: none;
        display: inline-block;
        margin-top: 10px;
        transition: all 0.3s ease;
    }
    .url-button:hover {
        opacity: 0.9;
    }
    .url-button-red {
        background-color: #e74c3c;
    }
    .url-button-green {
        background-color: #2ecc71;
    }
    .url-button-blue {
        background-color: #3498db;
    }
    /* Animaciones y efectos */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .fade-in {
        animation: fadeIn 0.5s ease-in-out;
    }
    .stMarkdown p {
        font-size: 18px;
        line-height: 1.6;
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #eaeaea;
        color: #7f8c8d;
    }
    /* Mejoras para dispositivos móviles */
    @media (max-width: 768px) {
        .title {
            font-size: 36px;
        }
        .subtitle {
            font-size: 28px;
        }
        .stButton>button {
            font-size: 16px;
            height: 50px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Sección de presentación del creador
def show_creator_profile():
    st.markdown('<div class="profile-box fade-in">', unsafe_allow_html=True)
    st.markdown('<h2>👤 Autor:</h2>', unsafe_allow_html=True)
    st.markdown('<p>© 2025 <strong>Ibar Federico Anderson, Ph.D., Master, Industrial Designer</strong>. All rights reserved.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            '<p>'
            '🎓 <strong>Google Scholar:</strong> <a href="https://scholar.google.com/citations?user=mXD4RFUAAAAJ&hl=en" target="_blank">Visite Perfil</a>'
            '</p>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<p>'
            '<img src="https://upload.wikimedia.org/wikipedia/commons/0/06/ORCID_iD.svg" width="20" height="20" style="vertical-align: middle; margin-right: 10px;">'
            '<strong>ORCID:</strong> <a href="https://orcid.org/0000-0002-9732-3660" target="_blank">Visite Perfil</a>'
            '</p>',
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            '<p>'
            '<img src="https://upload.wikimedia.org/wikipedia/commons/5/5e/ResearchGate_icon_SVG.svg" width="20" height="20" style="vertical-align: middle; margin-right: 10px;">'
            '<strong>Research Gate:</strong> <a href="https://www.researchgate.net/profile/Ibar-Anderson" target="_blank">Visite Perfil</a>'
            '</p>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<p>'
            '📖 <strong>Creative Commons:</strong> This work is licensed under the <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank">CC BY 4.0 License</a>.'
            '</p>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

# Función para convertir imagen a base64 para descarga directa
def get_image_download_link(img, filename, text):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{img_str}" download="{filename}" class="url-button">{text}</a>'
    return href

# Funciones de QR mejoradas para mayor rendimiento y fiabilidad
def create_qr(data, color, qr_version=10, box_size=10):
    # Validar datos de entrada
    if not data:
        return None
    
    try:
        qr = qrcode.QRCode(
            version=qr_version,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=box_size,
            border=4
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Mapeo de colores
        color_map = {
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "black": (0, 0, 0)
        }
        
        # Usar color en formato RGB si está en el mapa, o usar el color directamente
        fill_color = color_map.get(color, color)
        
        img = qr.make_image(fill_color=fill_color, back_color="white").convert('RGBA')
        return img
    except Exception as e:
        logger.error(f"Error creating QR code: {str(e)}")
        return None

def create_qr_with_logo(data, color, logo_file=None, qr_version=10, box_size=10):
    img = create_qr(data, color, qr_version, box_size)
    if img is None:
        return None
    
    if logo_file is not None:
        try:
            # Crear archivo temporal para el logo
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_logo:
                temp_logo.write(logo_file.getvalue())
                logo_path = temp_logo.name
            
            logo = Image.open(logo_path).convert("RGBA")
            
            # Redimensionar el logo a un tamaño proporcional
            basewidth = img.size[0] // 4
            wpercent = (basewidth / float(logo.size[0]))
            hsize = int((float(logo.size[1]) * float(wpercent)))
            logo = logo.resize((basewidth, hsize), Image.LANCZOS)
            
            # Posicionar el logo en el centro
            pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
            
            # Crear una máscara para suavizar los bordes del logo
            mask = logo.split()[3] if logo.mode == 'RGBA' else None
            
            # Pegar el logo en el QR code
            img.paste(logo, pos, mask)
            
            # Eliminar el archivo temporal
            try:
                os.unlink(logo_path)
            except:
                pass
                
        except Exception as e:
            logger.error(f"Error adding logo to QR: {str(e)}")
    
    return img

def combine_qr_images(img1, img2, img3, logo_file=None):
    # Verificar que todas las imágenes son válidas
    if any(img is None for img in [img1, img2, img3]):
        logger.error("One or more QR images are invalid")
        return None
    
    try:
        # Asegurar que todas las imágenes tengan el mismo tamaño
        size = img1.size
        if img2.size != size:
            img2 = img2.resize(size, Image.LANCZOS)
        if img3.size != size:
            img3 = img3.resize(size, Image.LANCZOS)
        
        # Crear imagen final
        final_image = Image.new("RGBA", size, "black")
        
        # Obtener datos de píxeles de cada imagen
        data_red = img1.getdata()
        data_green = img2.getdata()
        data_blue = img3.getdata()
        
        # Combinar datos para crear la imagen final
        new_data = []
        for i in range(len(data_red)):
            r1, g1, b1, a1 = data_red[i]
            red_pixel = (r1, g1, b1) != (255, 255, 255)
            
            r2, g2, b2, a2 = data_green[i]
            green_pixel = (r2, g2, b2) != (255, 255, 255)
            
            r3, g3, b3, a3 = data_blue[i]
            blue_pixel = (r3, g3, b3) != (255, 255, 255)
            
            # Determinar el color basado en la combinación de píxeles
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
        
        # Añadir logo si se proporciona
        if logo_file is not None:
            try:
                # Crear archivo temporal para el logo
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_logo:
                    temp_logo.write(logo_file.getvalue())
                    logo_path = temp_logo.name
                
                logo = Image.open(logo_path).convert("RGBA")
                
                # Redimensionar el logo
                basewidth = final_image.size[0] // 4
                wpercent = (basewidth / float(logo.size[0]))
                hsize = int((float(logo.size[1]) * float(wpercent)))
                logo = logo.resize((basewidth, hsize), Image.LANCZOS)
                
                # Posicionar el logo en el centro
                pos = ((final_image.size[0] - logo.size[0]) // 2, (final_image.size[1] - logo.size[1]) // 2)
                
                # Crear una máscara para suavizar los bordes del logo
                mask = logo.split()[3] if logo.mode == 'RGBA' else None
                
                # Pegar el logo en el QR code
                final_image.paste(logo, pos, mask)
                
                # Eliminar el archivo temporal
                try:
                    os.unlink(logo_path)
                except:
                    pass
                    
            except Exception as e:
                logger.error(f"Error adding logo to combined QR: {str(e)}")
        
        return final_image
    
    except Exception as e:
        logger.error(f"Error combining QR images: {str(e)}")
        return None

def generate_qrgb(red_data, green_data, blue_data, logo_file=None, mode='link'):
    try:
        # Determinar la configuración óptima según el modo
        qr_version = 10 if mode == 'link' else 3
        box_size = 10 if mode == 'link' else 20
        
        # Generar los QR codes individuales
        img_red = create_qr_with_logo(red_data, "red", logo_file, qr_version, box_size)
        img_green = create_qr_with_logo(green_data, "green", logo_file, qr_version, box_size)
        img_blue = create_qr_with_logo(blue_data, "blue", logo_file, qr_version, box_size)
        
        # Combinar los QR codes
        combined_img = combine_qr_images(img_red, img_green, img_blue, logo_file)
        
        if combined_img:
            # Guardar la imagen combinada
            output_path = os.path.join(FOLDER_PATH, "superposed_qr.png")
            combined_img.save(output_path)
            return combined_img
        else:
            logger.error("Failed to generate combined QR image")
            return None
            
    except Exception as e:
        logger.error(f"Error in generate_qrgb: {str(e)}")
        return None

def manual_decode_superposed_qr(uploaded_file):
    try:
        # Crear archivo temporal para el QR
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_path = temp_file.name
        
        # Abrir la imagen
        superposed_img = Image.open(temp_path).convert("RGBA")
        superposed_data = superposed_img.getdata()
        size = superposed_img.size
        
        # Inicializar imágenes para cada canal
        red_data = [(255, 255, 255, 255)] * len(superposed_data)
        green_data = [(255, 255, 255, 255)] * len(superposed_data)
        blue_data = [(255, 255, 255, 255)] * len(superposed_data)
        
        # Extraer los canales
        for i in range(len(superposed_data)):
            r, g, b, a = superposed_data[i]
            if r > 100:  # Umbral para detectar rojo
                red_data[i] = (0, 0, 0, 255)
            if g > 100:  # Umbral para detectar verde
                green_data[i] = (0, 0, 0, 255)
            if b > 100:  # Umbral para detectar azul
                blue_data[i] = (0, 0, 0, 255)
        
        # Crear imágenes separadas para cada canal
        red_img = Image.new("RGBA", size)
        green_img = Image.new("RGBA", size)
        blue_img = Image.new("RGBA", size)
        
        red_img.putdata(red_data)
        green_img.putdata(green_data)
        blue_img.putdata(blue_data)
        
        # Guardar las imágenes temporalmente para la decodificación
        red_path = os.path.join(FOLDER_PATH, "decoded_red.png")
        green_path = os.path.join(FOLDER_PATH, "decoded_green.png")
        blue_path = os.path.join(FOLDER_PATH, "decoded_blue.png")
        
        red_img.save(red_path)
        green_img.save(green_path)
        blue_img.save(blue_path)
        
        # Decodificar las imágenes usando OpenCV
        data_red = read_qr(red_path)
        data_green = read_qr(green_path)
        data_blue = read_qr(blue_path)
        
        # Limpiar archivos temporales
        try:
            os.unlink(temp_path)
        except:
            pass
        
        return data_red, data_green, data_blue, (red_img, green_img, blue_img)
        
    except Exception as e:
        logger.error(f"Error in manual_decode_superposed_qr: {str(e)}")
        return None, None, None, None

def read_qr(filename):
    try:
        # Leer la imagen
        img = cv2.imread(filename)
        if img is None:
            logger.error(f"Failed to read image: {filename}")
            return None
        
        # Intentar decodificar con diferentes métodos para mayor robustez
        detector = cv2.QRCodeDetector()
        data, vertices_array, _ = detector.detectAndDecode(img)
        
        if vertices_array is not None:
            return data
        
        # Si falló el primer intento, probar con preprocesamiento
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        
        data, vertices_array, _ = detector.detectAndDecode(thresh)
        
        return data if vertices_array is not None else None
        
    except Exception as e:
        logger.error(f"Error reading QR code: {str(e)}")
        return None

# Interfaz principal mejorada con capacidades adicionales
def main():
    # Mostrar perfil del creador
    show_creator_profile()
    
    # Inicializar estado de la sesión
    if 'page' not in st.session_state:
        st.session_state.page = "inicio"
    
    # Pantalla inicial
    if st.session_state.page == "inicio":
        col_logo, col_title = st.columns([1, 3])
        with col_logo:
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/QR_code_for_mobile_English_Wikipedia.svg/1200px-QR_code_for_mobile_English_Wikipedia.svg.png", width=100)
        with col_title:
            st.markdown('<div class="title">Generador QRGB Online</div>', unsafe_allow_html=True)
        
        st.markdown("<p class='fade-in' style='text-align: center; font-size: 20px;'>Codifica tres QR codes en uno solo usando los canales de color RGB.</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔒 Codificar QRGB", help="Codificar un nuevo QRGB", use_container_width=True):
                st.session_state.page = "codificar"
        with col2:
            if st.button("🔓 Decodificar QRGB", help="Decodificar un QRGB existente", use_container_width=True):
                st.session_state.page = "decodificar"
        
        # Información explicativa
        with st.expander("¿Qué es QRGB?"):
            st.markdown("""
            <div class='fade-in'>
            <p>La tecnología QRGB permite combinar tres códigos QR diferentes en una sola imagen, utilizando los canales de color rojo, verde y azul.</p>
            
            <p>Cada canal puede contener información diferente, como:</p>
            <ul>
                <li>URLs a diferentes sitios web</li>
                <li>Información de contacto</li>
                <li>Mensajes cifrados</li>
                <li>Enlaces a redes sociales</li>
            </ul>
            
            <p>Esta tecnología es útil para marketing, compartir múltiples enlaces y aplicaciones que requieren mayor densidad de información en un solo código.</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Codificar QRGB
    elif st.session_state.page == "codificar":
        st.markdown('<div class="subtitle">Codificar QRGB</div>', unsafe_allow_html=True)
        st.markdown("<p>Ingresa los datos y sube un logo (opcional) para generar tu QRGB personalizado.</p>", unsafe_allow_html=True)
        
        # Campos de entrada con mejor organización
        col1, col2 = st.columns([2, 1])
        with col1:
            red_data = st.text_input("🔴 Datos de la Capa Roja:", placeholder="Texto o URL", help="Introduce información para la capa roja del QR")
            green_data = st.text_input("🟢 Datos de la Capa Verde:", placeholder="Texto o URL", help="Introduce información para la capa verde del QR")
            blue_data = st.text_input("🔵 Datos de la Capa Azul:", placeholder="Texto o URL", help="Introduce información para la capa azul del QR")
        
        with col2:
            st.write("🖼️ Logo (Opcional)")
            logo_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], help="Añade un logo en el centro del QR")
            
            # Vista previa del logo
            if logo_file:
                st.image(logo_file, caption="Vista previa del logo", width=150)
        
        # Botones de acción
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            generate_button = st.button("🔄 Generar QRGB", help="Generar el QRGB con los datos proporcionados", use_container_width=True)
        with col_btn2:
            if st.button("🏠 Volver", help="Volver al inicio", use_container_width=True):
                st.session_state.page = "inicio"
        
        # Generar el QRGB
        if generate_button:
            if all([red_data, green_data, blue_data]):
                try:
                    with st.spinner('Generando QRGB...'):
                        # Determinar el modo basado en el contenido
                        mode = 'link' if any('http' in text.lower() for text in [red_data, green_data, blue_data]) else 'text'
                        
                        # Generar el QRGB
                        combined_img = generate_qrgb(red_data, green_data, blue_data, logo_file, mode)
                        
                        if combined_img:
                            # Mostrar las tres capas individuales y la combinada
                            st.subheader("Capas del QRGB")
                            col_r, col_g, col_b, col_rgb = st.columns(4)
                            
                            # Generar QRs individuales para mostrar
                            img_red = create_qr(red_data, "red")
                            img_green = create_qr(green_data, "green")
                            img_blue = create_qr(blue_data, "blue")
                            
                            with col_r:
                                st.image(img_red, caption="Capa Roja", width=150)
                            with col_g:
                                st.image(img_green, caption="Capa Verde", width=150)
                            with col_b:
                                st.image(img_blue, caption="Capa Azul", width=150)
                            with col_rgb:
                                st.image(combined_img, caption="QRGB Combinado", width=150)
                            
                            # Información y descarga
                            st.success("¡QRGB generado con éxito!")
                            
                            # Información sobre las capas
                            st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                            st.markdown("### Información Codificada:")
                            
                            st.markdown(f"<span class='color-red'>🔴 Capa Roja:</span> {red_data}", unsafe_allow_html=True)
                            st.markdown(f"<span class='color-green'>🟢 Capa Verde:</span> {green_data}", unsafe_allow_html=True)
                            st.markdown(f"<span class='color-blue'>🔵 Capa Azul:</span> {blue_data}", unsafe_allow_html=True)
                            
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                            # Opciones de descarga
                            buf = BytesIO()
                            combined_img.save(buf, format="PNG")
                            byte_im = buf.getvalue()
                            
                            col_download, col_info = st.columns([1, 2])
                            with col_download:
                                st.download_button(
                                    label="💾 Descargar QRGB",
                                    data=byte_im,
                                    file_name="qrgb.png",
                                    mime="image/png",
                                    use_container_width=True
                                )
                            with col_info:
                                st.info("Puedes escanear el QRGB con cualquier lector de QR estándar. Cada color mostrará un código diferente.")
                    
                except Exception as e:
                    st.error(f"Error al generar QRGB: {str(e)}")
                    logger.error(f"Error generating QRGB: {str(e)}")
            else:
                st.warning("Por favor, completa todos los campos de texto.")
    
    # Decodificar QRGB
    elif st.session_state.page == "decodificar":
        st.markdown('<div class="subtitle">Decodificar QRGB</div>', unsafe_allow_html=True)
        st.markdown("<p>Sube un QRGB para extraer la información de cada capa de color.</p>", unsafe_allow_html=True)
        
        # Subir QR
        qr_file = st.file_uploader("🔍 Cargar imagen QRGB", type=['png', 'jpg', 'jpeg'], help="Selecciona un archivo QRGB para decodificar")
        
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            decode_button = st.button("🔍 Analizar QRGB", help="Decodificar el QRGB cargado", use_container_width=True)
        with col_btn2:
            if st.button("🏠 Volver", help="Volver al inicio", use_container_width=True):
                st.session_state.page = "inicio"
        
        # Decodificar el QR
        if qr_file and decode_button:
            try:
                with st.spinner('Analizando QRGB...'):
                    # Decodificar la imagen
                    data_red, data_green, data_blue, separated_images = manual_decode_superposed_qr(qr_file)
                    
                    if all(data is not None for data in [data_red, data_green, data_blue]):
                        # Mostrar la imagen original y las capas separadas
                        st.subheader("Análisis del QRGB")
                        
                        col_orig, col_r, col_g, col_b = st.columns(4)
                        with col_orig:
                            st.image(qr_file, caption="QRGB Original", width=150)
                        
                        # Mostrar capas decodificadas si están disponibles
                        if separated_images:
                            red_img, green_img, blue_img = separated_images
                            with col_r:
                                st.image(red_img, caption="Capa Roja", width=150)
                            with col_g:
                                st.image(green_img, caption="Capa Verde", width=150)
                            with col_b:
                                st.image(blue_img, caption="Capa Azul", width=150)
                        
                        # Mostrar resultados
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        st.markdown("### Datos Decodificados:")
                        
                        # Función para mostrar y crear botones de URL
                        def display_layer_data(color_name, color_class, data, emoji):
                            st.markdown(f'<span class="{color_class}"><span class="symbol">{emoji}</span> Capa {color_name}:</span> {data if data else "No se pudo decodificar"}', unsafe_allow_html=True)
                            
                            if data and ('http://' in data or 'https://' in data):
                                st.markdown(f'<a href="{data}" target="_blank" class="url-button url-button-{color_class.split("-")[1]}">{emoji} Abrir URL {color_name}</a>', unsafe_allow_html=True)
                        
                        # Mostrar datos de cada capa
                        display_layer_data("Roja", "color-red", data_red, "🔴")
                        display_layer_data("Verde", "color-green", data_green, "🟢")
                        display_layer_data("Azul", "color-blue", data_blue, "🔵")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.warning("No se pudieron decodificar todas las capas del QRGB. Asegúrate de que la imagen sea un QRGB válido.")
                
            except Exception as e:
                st.error(f"Error al decodificar: {str(e)}")
                logger.error(f"Error decoding QRGB: {str(e)}")
    
    # Pie de página con información de la versión
    st.markdown("""
    <div class="footer">
        <p>QRGB Generator v2.0 | © 2025 All Rights Reserved</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
