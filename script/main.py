import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.cluster import KMeans
import cv2 as cv
from rembg import remove
import io
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Pixcraft - Image Processing Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for high-contrast dark studio dashboard layout
st.markdown("""
    <style>
    /* Force main container to use a dark dashboard theme */
    .stApp {
        background-color: #121620 !important;
    }
    
    .main {
        background-color: #121620 !important;
        padding: 1.5rem;
    }
    
    /* Content container framing - matching the dark background cleanly */
    .block-container {
        background: #121620 !important;
        padding: 2rem !important;
    }
    
    /* Elegant Dark Sidebar styling overrides */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a202c 0%, #0d1117 100%) !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #e2e8f0 !important;
    }
    
    /* Purple Header Banner Text Alignment */
    .purple-banner h1 {
        color: #ffffff !important;
        font-family: 'Inter', -apple-system, sans-serif;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Fix typography visibility issues across dark canvas */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, p {
        color: #f1f5f9 !important;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Fix tab selection text contrast completely */
    button[data-baseweb="tab"] p {
        color: #94a3b8 !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #6366f1 !important; /* Indigo for selected active tab */
    }
    
    /* Drag & Drop File Uploader custom skin */
    [data-testid="stFileUploader"] {
        background: #1e2538 !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        border: 2px dashed #6366f1 !important;
    }
    
    [data-testid="stFileUploader"] label {
        color: #a5b4fc !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    
    /* Standard interactive buttons styling */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.8rem !important;
        font-weight: 600 !important;
        transition: all 0.25s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.35) !important;
    }
    
    /* High-contrast Action download button wrappers */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.8rem !important;
        font-weight: 600 !important;
        transition: all 0.25s ease !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35) !important;
    }
    
    /* Border layouts around images */
    img {
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
        border: 1px solid #2d3748 !important;
    }
    
    /* Feature information panels inside sidebar */
    .feature-card {
        background: rgba(255, 255, 255, 0.04) !important;
        border-radius: 8px !important;
        padding: 0.85rem !important;
        margin: 0.6rem 0 !important;
        border-left: 3px solid #6366f1 !important;
    }
    
    .feature-title {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    .feature-desc {
        color: #94a3b8 !important;
        font-size: 0.85rem !important;
        line-height: 1.4 !important;
    }
    </style>
""", unsafe_allow_html=True)


class Main:
    def process_image(self, img_np, choice, settings):
        """Processes a numpy RGB image based on the selected service tool."""
        if choice == "Remove Background":
            return remove(img_np)
            
        elif choice == "Blur Image":
            ksize = settings.get("blur_strength", 15)
            return cv.GaussianBlur(img_np, (ksize, ksize), 0)
            
        elif choice == "Color Quantization":
            clusters = settings.get("quant_colors", 16)
            h, w, c = img_np.shape
            image_2d = img_np.reshape((h * w, c))
            model = KMeans(n_clusters=clusters, random_state=42)
            labels = model.fit_predict(image_2d)
            rgb_codes = model.cluster_centers_.round(0).astype(np.uint8)
            return np.reshape(rgb_codes[labels], (h, w, c))
            
        elif choice == "Gray Scale":
            gray = cv.cvtColor(img_np, cv.COLOR_RGB2GRAY)
            return cv.cvtColor(gray, cv.COLOR_GRAY2RGB)
            
        elif choice == "Black & White":
            gray = cv.cvtColor(img_np, cv.COLOR_RGB2GRAY)
            _, bw = cv.threshold(gray, settings.get("bw_threshold", 127), 255, cv.THRESH_BINARY)
            return cv.cvtColor(bw, cv.COLOR_GRAY2RGB)
            
        return img_np

    def main(self):
        # Header display with structural text baseline nested neatly within the purple block
        st.markdown("""
            <div class="purple-banner" style="text-align: center; padding: 2.5rem 1rem; background: #6366f1; border-radius: 16px; margin-bottom: 1.5rem;">
                <h1>✨ PIXCRAFT STUDIO: BATCH PROCESSING TERMINAL</h1>
                <p style="color: #e0e7ff !important; font-size: 1.1rem; margin-top: 0.5rem; margin-bottom: 0;">
                    High-Fidelity Automated Image Processing Suite
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Multi-file batch uploader array setup
        col1, col2, col3 = st.columns([1, 4, 1])
        with col2:
            uploaded_files = st.file_uploader(
                label="📸 Batch Workspace: Select & Upload Images (Max 5 items)",
                key="batch_uploader",
                type=["jpg", "jpeg", "png"],
                accept_multiple_files=True,
                help="Upload up to 5 images to run unique parallel workflows simultaneously in jpg, jpeg, png format."
            )
            
        if uploaded_files:
            if len(uploaded_files) > 5:
                st.error("⚠️ Maximum of 5 images can be loaded concurrently. Please trim your selections.")
                return

            st.markdown("<br><h2 style='font-size:1.8rem;'>🛠️ Working Workspace Array</h2>", unsafe_allow_html=True)
            
            # Dynamic high-contrast tab construction mapping
            tab_labels = [f"📄 {file.name[:18]}..." for file in uploaded_files]
            tabs = st.tabs(tab_labels)
            
            for index, file in enumerate(uploaded_files):
                with tabs[index]:
                    try:
                        pil_img = Image.open(file).convert("RGB")
                        image_np = np.array(pil_img)
                    except Exception as e:
                        st.error(f"Failed parsing image file source format: {e}")
                        continue
                    
                    workspace_col_1, workspace_col_2 = st.columns([2, 3])
                    
                    with workspace_col_1:
                        st.markdown("#### Dynamic Pipeline Configuration")
                        
                        service_options = ["Original (No Action)", "Remove Background", "Blur Image", "Color Quantization", "Gray Scale", "Black & White"]
                        choice = st.selectbox(
                            f"Execution Pipeline Logic Assignment:",
                            service_options,
                            key=f"choice_{file.name}_{index}"
                        )
                        
                        current_settings = {}
                        if choice == "Blur Image":
                            current_settings["blur_strength"] = st.slider(
                                "Blur Intensity Radius", 3, 151, 15, step=2, key=f"blur_{file.name}_{index}"
                            )
                        elif choice == "Color Quantization":
                            st.info("💡 Tip: Larger target palette matrices optimize accuracy scales vs execution timings.")
                            current_settings["quant_colors"] = st.slider(
                                "Target Color Clusters (k-Means)", 2, 64, 16, key=f"quant_{file.name}_{index}"
                            )
                        elif choice == "Black & White":
                            current_settings["bw_threshold"] = st.slider(
                                "Binarization Boundary Threshold", 0, 255, 127, key=f"bw_{file.name}_{index}"
                            )
                            
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown(f"""
                            <div style="background-color: #1e2538; padding: 1rem; border-radius: 8px; border-left: 3px solid #6366f1;">
                                <span style="font-size:0.85rem; color:#94a3b8; font-weight:600;">METRICS DIMENSIONS</span><br>
                                <span style="font-size:1.1rem; color:#f1f5f9; font-weight:700;">{image_np.shape[1]}w × {image_np.shape[0]}h px</span>
                            </div>
                        """, unsafe_allow_html=True)
                        
                    with workspace_col_2:
                        st.markdown("#### Real-time Verification Node")
                        
                        if choice != "Original (No Action)":
                            with st.spinner("Processing structural matrix color arrays..."):
                                try:
                                    processed_np = self.process_image(image_np, choice, current_settings)
                                    
                                    view_col1, view_col2 = st.columns(2)
                                    with view_col1:
                                        st.image(image_np, caption="Source Input Viewport", use_container_width=True)
                                    with view_col2:
                                        st.image(processed_np, caption=f"Pipeline Output: {choice}", use_container_width=True)
                                        
                                    out_pil = Image.fromarray(processed_np)
                                    buf = io.BytesIO()
                                    out_pil.save(buf, format="PNG")
                                    byte_data = buf.getvalue()
                                    
                                    st.markdown("<br>", unsafe_allow_html=True)
                                    st.download_button(
                                        label="📥 Download Output Artifact",
                                        data=byte_data,
                                        file_name=f"pixcraft_{index}_{choice.lower().replace(' ', '_')}.png",
                                        mime="image/png",
                                        key=f"dl_{file.name}_{index}",
                                        use_container_width=True
                                    )
                                except Exception as e:
                                    st.error(f"Pipeline running exception fault mapped: {e}")
                        else:
                            st.image(image_np, caption="Source Preview Rendering Mode Active", use_container_width=True)
        else:
            st.markdown("""
                <div style="text-align: center; padding: 4rem; background: #1e2538; 
                border-radius: 12px; border: 2px dashed #475569; margin: 2rem 0;">
                    <h3 style="color: #94a3b8 !important; margin-bottom: 0.5rem;">📥 Digital Darkroom Sandbox Offline</h3>
                    <p style="color: #64748b !important; font-size: 1rem; max-width: 500px; margin: 0 auto;">
                        Please upload digital image assets into the batch configuration portal layout window above to activate rendering engines.
                    </p>
                </div>
            """, unsafe_allow_html=True)


class App(Main):
    def app(self):
        st.sidebar.markdown("""
            <div style="text-align: center; padding: 1.5rem 0 1rem 0;">
                <h2 style="font-size: 2rem; background: linear-gradient(135deg, #a5b4fc 0%, #e0e7ff 100%);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; margin: 0;">
                    Pixcraft Engine ✨
                </h2>
                <p style="color: #64748b !important; margin-top: 0.2rem; font-size: 0.85rem; letter-spacing: 1px;">
                    STUDIO DASHBOARD
                </p>
            </div>
            <hr style="border: 0; height: 1px; background: rgba(255,255,255,0.1); margin: 1rem 0;">
        """, unsafe_allow_html=True)
        
        st.sidebar.markdown("<p style='color: #94a3b8; font-weight:600; font-size:0.9rem; margin-left:5px;'>PIPELINE DOCUMENTATION</p>", unsafe_allow_html=True)
        
        services = [
            ("1️⃣ Background Stripping", "Leverages transparent multi-pass AI masking nodes to cleanly extract central visual focal subjects."),
            ("2️⃣ Adaptive Spatial Blur", "Applies uniform variable-width parametric Gaussian smoothing arrays across image pixels."),
            ("3️⃣ Quantization Vectoring", "Downsamples pixel arrays using adaptive multi-dimensional Euclidean k-Means clustering centroids."),
            ("4️⃣ Grayscale Extraction", "Converts individual luminous channels systematically down to a balanced gray balance spectrum."),
            ("5️⃣ High-Contrast Thresholding", "Splits channels into pure binary black & white scales against targeted luminosity limits.")
        ]
        
        for title, desc in services:
            st.sidebar.markdown(f"""
                <div class="feature-card">
                    <div class="feature-title">{title}</div>
                    <div class="feature-desc">{desc}</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.sidebar.markdown("""
            <div style="margin-top: 2rem; padding: 0.75rem; background: rgba(239, 68, 68, 0.15); border-left: 3px solid #ef4444; border-radius: 6px;">
                <span style="color: #fca5a5 !important; font-size: 0.85rem; font-weight: bold;">⚠️ Memory Constraints Bounds</span><br>
                <span style="color: #f87171 !important; font-size: 0.8rem;">Batch operations are natively capped explicitly to a safe parallel capacity limit of 5 concurrent loaded images.</span>
            </div>
            <div style="text-align: center; margin-top: 3rem; color: #475569 !important; font-size: 0.75rem;">
                <p>© 2026 Pixcraft Architecture Platform</p>
            </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    obj = App()
    obj.app()
    obj.main()