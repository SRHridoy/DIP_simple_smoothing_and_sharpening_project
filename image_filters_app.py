import streamlit as st
import numpy as np
import cv2
from PIL import Image
from io import BytesIO

# ---------- Helper functions ----------

def load_image(uploaded_file):
    img = Image.open(uploaded_file).convert("RGB")
    return np.array(img)

def apply_smoothing_filter(img, method, intensity):
    intensity = max(1, min(intensity, 10))
    ksize = 2 * intensity + 1  # 3,5,7,...,21

    info = {
        "Filter family": "Smoothing (Low-pass)",
        "Filter used": method,
        "Intensity level": f"{intensity}/10",
        "Kernel size": f"{ksize} x {ksize}"
    }

    if method == "Average blur":
        filtered = cv2.blur(img, (ksize, ksize))

    elif method == "Gaussian blur":
        sigma = intensity / 2.0
        filtered = cv2.GaussianBlur(img, (ksize, ksize), sigmaX=sigma)
        info["Sigma"] = f"{sigma:.2f}"

    elif method == "Median blur":
        filtered = cv2.medianBlur(img, ksize)

    else:
        filtered = img

    return filtered, info

def apply_sharpening_filter(img, method, intensity):
    intensity = max(1, min(intensity, 10))
    info = {
        "Filter family": "Sharpening (High-pass)",
        "Filter used": method,
        "Intensity level": f"{intensity}/10"
    }

    if method == "Simple sharpening kernel":
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        base_sharp = cv2.filter2D(img, ddepth=-1, kernel=kernel)

        amount = 0.2 * intensity   # 0.2–2.0
        filtered = cv2.addWeighted(img, 1.0, base_sharp, amount, 0)

        info["Kernel"] = "[[0, -1, 0], [-1, 5, -1], [0, -1, 0]]"
        info["Amount (weight)"] = f"{amount:.2f}"

    elif method == "Unsharp masking":
        ksize = 2 * intensity + 1
        sigma = intensity / 2.0
        amount = intensity / 2.0

        blurred = cv2.GaussianBlur(img, (ksize, ksize), sigmaX=sigma)
        filtered = cv2.addWeighted(img, 1 + amount, blurred, -amount, 0)

        info["Blur kernel size"] = f"{ksize} x {ksize}"
        info["Sigma"] = f"{sigma:.2f}"
        info["Amount"] = f"{amount:.2f}"

    else:
        filtered = img

    return filtered, info

def get_image_download_bytes(filtered_img, filename="filtered_image.png"):
    pil_img = Image.fromarray(filtered_img)
    buf = BytesIO()
    pil_img.save(buf, format="PNG")
    return buf.getvalue(), filename

def info_dict_to_string(info):
    return "\n".join([f"- **{k}**: {v}" for k, v in info.items()])


# ---------- Streamlit UI ----------

st.set_page_config(page_title="Image Sharpening & Smoothing", page_icon="🧮", layout="wide")

st.title("Image Sharpening & Smoothing")
st.write("Upload an image, choose smoothing or sharpening, set the intensity, then click **Apply Filter**.")

# Session state for keeping last result
if "filtered_img" not in st.session_state:
    st.session_state.filtered_img = None
if "filter_info" not in st.session_state:
    st.session_state.filter_info = None
if "last_filename" not in st.session_state:
    st.session_state.last_filename = None

# 1. Upload
uploaded_file = st.file_uploader(
    "Step 1 — Upload an image",
    type=["png", "jpg", "jpeg", "bmp", "tif", "tiff"]
)

if uploaded_file is None:
    st.info("Please upload an image to start.")
    st.stop()

# If user uploads a new file, clear old result
if uploaded_file.name != st.session_state.last_filename:
    st.session_state.filtered_img = None
    st.session_state.filter_info = None
    st.session_state.last_filename = uploaded_file.name

img = load_image(uploaded_file)

st.markdown("## Filter settings")

# 2. Filter controls (NO form – updates immediately)
filter_family = st.radio(
    "Operation",
    ["Smoothing (Low-pass)", "Sharpening (High-pass)"],
    horizontal=True
)

# Options change depending on selected operation
if filter_family == "Smoothing (Low-pass)":
    filter_method = st.selectbox(
        "Smoothing method",
        ["Average blur", "Gaussian blur", "Median blur"]
    )
else:
    filter_method = st.selectbox(
        "Sharpening method",
        ["Simple sharpening kernel", "Unsharp masking"]
    )

intensity = st.slider(
    "Intensity level (1 = lower effect, 10 = higher effect)",
    1, 10, 5
)

apply_button = st.button("Apply Filter")

# 3. Apply filter when button pressed, store in session_state
if apply_button:
    if filter_family == "Smoothing (Low-pass)":
        filtered_img, info = apply_smoothing_filter(img, filter_method, intensity)
    else:
        filtered_img, info = apply_sharpening_filter(img, filter_method, intensity)

    st.session_state.filtered_img = filtered_img
    st.session_state.filter_info = info

st.markdown("## Result")

# 4. Show side-by-side only if we have a filtered image
if st.session_state.filtered_img is not None:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original")
        st.image(img, use_column_width=True)
    with col2:
        st.subheader("Filtered")
        st.image(st.session_state.filtered_img, use_column_width=True)

    st.markdown("### Filter details")
    st.markdown(info_dict_to_string(st.session_state.filter_info))

    st.markdown("### Download")
    img_bytes, filename = get_image_download_bytes(
        st.session_state.filtered_img,
        filename=f"{filter_family.split()[0].lower()}_{filter_method.lower().replace(' ', '_')}_int{intensity}.png"
    )
    st.download_button(
        "Download filtered image",
        data=img_bytes,
        file_name=filename,
        mime="image/png"
    )
else:
    # First time: just show original
    st.image(img, caption="Original image (no filter applied yet)", use_column_width=True)
