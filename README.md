# ✨ Pixcraft Studio: Batch Image Processing Engine

Pixcraft Studio is a professional, high-contrast digital darkroom dashboard built with Streamlit, OpenCV, and scikit-learn. It allows users to upload up to 5 images simultaneously and assign individual, parallel image-processing workflows to each image via an elegant, tabbed workspace interface.

---

## 🚀 Features

- **⚡ Concurrent Batch Processing:** Upload and manipulate up to 5 images concurrently without resetting state arrays.
- **🎨 Isolated Workspace Nodes:** Utilize a distinct tabbed interface to configure individual pipeline logic per uploaded image.
- **🖼️ Real-Time Preview Matrix:** Instantly view side-by-side comparative graphics of your original vs. processed images before exporting.
- **🎛️ Parametric Control Sliders:** Finetune properties seamlessly using high-precision responsive thresholds.

### Supported Micro-Services
1. **Background Stripping:** Cleanly extracts focal foreground subjects using layered masking algorithms.
2. **Adaptive Spatial Blur:** Applies dynamic Gaussian smoothing arrays across customizable radii.
3. **Quantization Vectoring:** Compresses structural color profiles via multi-dimensional Euclidean $k$-Means clustering centroids.
4. **Grayscale Extraction:** Restructures luminance mapping to transform colors down to a balanced gray balance spectrum.
5. **High-Contrast Thresholding:** Splits pixel values into pure binary black and white spaces matching specified brightness cutoffs.

---

## 🛠️ Tech Stack & Dependencies

Pixcraft Studio is powered by a robust backend vector processing array:

- **Frontend Interface:** [Streamlit](https://streamlit.io/)
- **Computer Vision Framework:** [OpenCV (cv2)](https://opencv.org/)
- **Machine Learning Core:** [scikit-learn (KMeans)](https://scikit-learn.org/)
- **Image Segregation Utility:** [rembg](https://github.com/danielgatis/rembg)
- **Data & Array Manipulation:** `numpy`, `pandas`, `Pillow (PIL)`
- **Rendering Visualization Engine:** `matplotlib`

---

## 📦 Installation & Setup

Follow these quick implementation phases to launch your local Pixcraft Studio node instance:

### 1. Clone the Repository

git clone [https://github.com/yourusername/pixcraft-studio.git](https://github.com/yourusername/pixcraft-studio.git)
cd pixcraft-studio

2. Install Required Dependencies
Ensure you have Python 3.8+ installed, then run:

pip install numpy pandas matplotlib streamlit scikit-learn opencv-python rembg Pillow

📖 How To Use
Upload Assets: Drag and drop or browse up to 5 images (.jpg, .jpeg, .png) inside the primary batch synchronization terminal dashboard.

Select Target Tab: Click on the dedicated file tab corresponding to the image you want to edit.

Configure Logic Array: Open the dropdown selector menu and choose your target utility (e.g., Color Quantization).

Fine-tune Sliders: Adjust parameters such as Blur Intensity Radius or Target Color Clusters to fit your project constraints.

Download Artifacts: Tap the high-contrast green Download Output Artifact button to export your rendering safely as a standalone .png asset.

⚠️ Allocation Boundaries & Constraints
Batch Size Limit: The sandboxed workspace is restricted to processing 5 parallel image uploads max per transactional workflow loop to protect local memory bounds.

Color Model: Images are automatically standardized into 3-channel RGB matrix profiles for stable uniform manipulation.
