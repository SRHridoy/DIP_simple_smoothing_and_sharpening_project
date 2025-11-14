

# Digital Image Processing Project

## Image Smoothing and Sharpening Using Spatial Filters

### 1. Project Overview

This project is a small web application (built with **Python** and **Streamlit**) that demonstrates basic **spatial filters** in Digital Image Processing:

* **Smoothing (low-pass filtering)** – reduces noise and blurs the image
* **Sharpening (high-pass filtering)** – enhances edges and fine details

The app allows the user to:

1. Upload an image
2. Choose **Smoothing** or **Sharpening**
3. Select a filter and an **intensity level** (1–10)
4. Click **Apply Filter**
5. View **original and filtered images side by side**
6. Download the filtered image as a PNG file

---

### 2. Technologies Used

* **Python 3**
* **Streamlit** – web UI
* **OpenCV (cv2)** – image processing operations
* **NumPy** – array operations on images
* **Pillow (PIL)** – loading and saving images

Main file:

* `image_filters_app.py` – complete Streamlit application

---

### 3. Installation and Running

1. (Optional) Create and activate a virtual environment.

2. Install required libraries:

```bash
pip install streamlit opencv-python pillow numpy
```

3. Run the app:

```bash
streamlit run image_filters_app.py
```

4. A browser tab will open (usually at `http://localhost:8501`) showing the interface.

---

### 4. How to Use the App

1. **Upload an Image**

   * Click **“Step 1 — Upload an image”** and select a `PNG / JPG / JPEG / BMP / TIF` file.
   * The original image is displayed.

2. **Choose Operation**

   * Under **“Filter settings”**, choose:

     * `Smoothing (Low-pass)` or
     * `Sharpening (High-pass)`

3. **Choose Filter Method**

   * If **Smoothing** is selected:

     * `Average blur`
     * `Gaussian blur`
     * `Median blur`
   * If **Sharpening** is selected:

     * `Simple sharpening kernel`
     * `Unsharp masking`

4. **Set Intensity Level**

   * Use the slider: **1 = lower effect, 10 = higher effect**.
   * The app internally maps this to kernel size and sharpening strength.

5. **Apply Filter**

   * Click **“Apply Filter”**.
   * The app processes the image and shows:

     * Original image (left)
     * Filtered image (right)

6. **See Details and Download**

   * Under **“Filter details”**, the app shows:

     * Filter family and name
     * Kernel size, sigma, amount, etc. (depending on filter)
   * Click **“Download filtered image”** to save the result.

---

### 5. Smoothing Filters (Low-Pass)

Smoothing filters remove rapid intensity changes and reduce noise, producing a blurred image.

#### 5.1 Average Blur (Mean Filter)

* Each output pixel is the average of its neighbors.
* For a 3×3 example, the kernel is:

[
\begin{bmatrix}
1/9 & 1/9 & 1/9 \
1/9 & 1/9 & 1/9 \
1/9 & 1/9 & 1/9 \
\end{bmatrix}
]

* In the code, the kernel size depends on intensity (3×3, 5×5, 7×7, …).

#### 5.2 Gaussian Blur

* Uses a Gaussian-shaped kernel: center pixel has the highest weight.
* Example of a normalized 3×3 Gaussian kernel:

[
\begin{bmatrix}
1/16 & 2/16 & 1/16 \
2/16 & 4/16 & 2/16 \
1/16 & 2/16 & 1/16 \
\end{bmatrix}
]

* In the app, both kernel size and sigma (spread) increase with intensity.

#### 5.3 Median Blur

* Non-linear filter (does not use a kernel matrix).
* For each pixel, the neighborhood values are sorted and the **median** value is taken.
* Very effective against **salt-and-pepper noise**.
* Neighborhood size (3×3, 5×5, 7×7, …) grows with intensity.

---

### 6. Sharpening Filters (High-Pass)

Sharpening filters highlight edges and small details by emphasizing intensity changes.

#### 6.1 Simple Sharpening Kernel

* Uses a fixed 3×3 high-pass kernel:

[
\begin{bmatrix}
0 & -1 & 0 \
-1 & 5 & -1 \
0 & -1 & 0 \
\end{bmatrix}
]

* This increases the contribution of the center pixel and subtracts neighbors.
* In the app, the result of this kernel is blended with the original image; the blend strength increases with intensity.

#### 6.2 Unsharp Masking

* Steps:

  1. Blur the original image (Gaussian blur).
  2. Subtract the blurred image from the original to get a **mask** (edges).
  3. Add a scaled version of this mask back to the original.

* This is equivalent to applying a sharpening kernel whose strength depends on the chosen **amount** and blur parameters.

* In the app, the blur size and sharpening amount both increase with intensity.

---

### 7. Intensity Control

The **Intensity level** slider (1–10) controls:

* **Smoothing filters**

  * Size of the neighborhood (kernel size)
  * Sigma for Gaussian blur
* **Sharpening filters**

  * Strength of blending between original and sharpened image
  * Blur size and sharpening amount for unsharp masking

Higher intensity → larger kernels / stronger sharpening.

---

### 8. Possible Extensions

* Add more spatial filters (e.g., Laplacian, Sobel, custom kernels).
* Show histograms before and after filtering.
* Add frequency-domain filtering using Fourier transforms.

---

### 9. Conclusion

This project demonstrates how simple spatial filters can be used to:

* Smooth images (remove noise and fine details)
* Sharpen images (enhance edges and focus)

The interactive Streamlit interface makes it easy to experiment with different filters and intensities and visually understand their effects on a real image.
