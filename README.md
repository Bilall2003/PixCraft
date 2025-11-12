# PixCraft
Interactive Streamlit dashboard to remove backgrounds, blur images, and apply color quantization — built with Python, OpenCV, and scikit-learn.

# Features

✅ Upload Images:
Easily upload .jpg or .png images from your computer.

✅ Remove Background:
Uses the rembg library (powered by ONNX models) to automatically detect and remove image backgrounds with precision.
Perfect for product photos, portraits, or transparent PNG generation.

✅ Blur Images:
Applies a Gaussian blur using OpenCV — great for hiding sensitive content or adding a cinematic depth-of-field effect.
You can control the blur intensity with a simple slider.

✅ Color Quantization:
Reduces the number of colors in your image using K-Means clustering (via scikit-learn).
Ideal for artistic effects, image compression, or simplifying color palettes.

✅ Instant Downloads:
All processed images can be downloaded with a single click — no external tools required.

✅ Streamlit UI:
Beautiful, minimal interface with sidebar explanations and custom CSS styling.

# Tech Stack

| Technology                | Purpose                         |
| ------------------------- | ------------------------------- |
| **Python 3.x**            | Core programming language       |
| **Streamlit**             | Web UI framework                |
| **OpenCV (cv2)**          | Image processing                |
| **Matplotlib**            | Visualization and saving images |
| **scikit-learn (KMeans)** | Color quantization              |
| **rembg**                 | Background removal              |
| **Pillow (PIL)**          | Image handling                  |
| **NumPy**                 | Array and pixel manipulation    |

