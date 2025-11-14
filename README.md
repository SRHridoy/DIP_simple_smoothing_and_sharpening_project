
# Digital Image Processing Project

## Image Smoothing and Sharpening Using Spatial Filters

### 1. Project Overview

This project is a small web application (built with **Python** and **Streamlit**) that demonstrates basic **spatial filtering** operations in Digital Image Processing:

* **Smoothing (low-pass filtering)** to reduce noise / blur the image
* **Sharpening (high-pass filtering)** to enhance edges and details

The app lets the user:

1. Upload an image
2. Choose **Smoothing** or **Sharpening**
3. Select a specific filter and an **intensity level** (1–10)
4. Click **Apply Filter**
5. See the **original and filtered images side by side**
6. Download the filtered image as a PNG file

---

### 2. Technologies Used

* **Python 3**
* **Streamlit** – for the web UI
* **OpenCV (cv2)** – for image filtering operations
* **NumPy** – for numerical operations on images
* **Pillow (PIL)** – for loading and saving images

Main file:

* `image_filters_app.py` – complete Streamlit app

---

### 3. How to Install and Run

1. **Create / activate a virtual environment** (optional but recommended).

2. Install the required libraries:

```bash
pip install streamlit opencv-python pillow numpy
```

3. Place `image_filters_app.py` in a folder and run:

```bash
streamlit run image_filters_app.py
```

4. Your browser will open a local web page (default: `http://localhost:8501`) showing the app.

---

### 4. How to Use the App

1. **Upload Image**

   * Click **“Step 1 — Upload an image”** and choose any `PNG/JPG/JPEG/BMP/TIF` file.
   * The original image is displayed.

2. **Choose Operation**

   * Under **“Filter settings”**, select one of:

     * `Smoothing (Low-pass)`
     * `Sharpening (High-pass)`

3. **Choose Filter Method (changes automatically)**

   * If **Smoothing** is selected, options are:

     * `Average blur`
     * `Gaussian blur`
     * `Median blur`
   * If **Sharpening** is selected, options are:

     * `Simple sharpening kernel`
     * `Unsharp masking`

4. **Set Intensity Level**

   * Use the slider **“Intensity level (1 = lower effect, 10 = higher effect)”**.
   * Higher intensity = stronger smoothing or sharpening.

5. **Apply Filter**

   * Click **“Apply Filter”**.
   * The app computes the filtered image and shows:

     * Original image (left)
     * Filtered image (right)

6. **View Filter Details and Download**

   * Under **“Filter details”**, the app displays:

     * Filter family (Smoothing or Sharpening)
     * Filter used
     * Kernel size, sigma, amount, etc. (depending on the filter)
   * Click **“Download filtered image”** to save the result as a PNG file.

---

### 5. Theory: Smoothing (Low-Pass Filters)

Smoothing filters are used to **reduce high-frequency components** (noise and rapid intensity changes). They blur the image but make it smoother.

#### 5.1 Average Blur (Mean Filter)

* Uses an ( N \times N ) kernel where every value is ( \frac{1}{N^2} ).
* The output pixel is the **average** of its neighbors.

Mathematically, for a kernel size ( N \times N ):

[
g(x, y) = \frac{1}{N^2} \sum_{i=-k}^{k} \sum_{j=-k}^{k} f(x+i, y+j)
]

where ( N = 2k + 1 ).

In the app:

* Kernel size ( N = 2 \times \text{intensity} + 1 ).
* Example: intensity 3 → kernel size 7×7.

#### 5.2 Gaussian Blur

* Weights neighboring pixels using a **Gaussian (normal) distribution**.
* Gives more importance to pixels near the center of the kernel.
* Better at smooth blurring with fewer artifacts.

Gaussian kernel:

[
G(x, y) = \frac{1}{2\pi\sigma^2} e^{-\frac{x^2 + y^2}{2\sigma^2}}
]

In the app:

* Kernel size ( N = 2 \times \text{intensity} + 1 ).
* Standard deviation ( \sigma = \frac{\text{intensity}}{2} ).

#### 5.3 Median Blur

* Non-linear filter.
* Replaces each pixel with the **median** of the pixels in the neighborhood.
* Very effective for removing **salt-and-pepper noise**.

In the app:

* Kernel size ( N = 2 \times \text{intensity} + 1 ) (must be odd).

---

### 6. Theory: Sharpening (High-Pass Filters)

Sharpening filters enhance **edges and fine details** by emphasizing high-frequency components.

#### 6.1 Simple Sharpening Kernel

Uses a fixed 3×3 kernel:

[
K =
\begin{bmatrix}
0 & -1 & 0 \
-1 & 5 & -1 \
0 & -1 & 0
\end{bmatrix}
]

* This kernel subtracts surrounding values and adds more weight to the center, which sharpens edges.

In the app:

1. First, the kernel is applied using convolution.
2. Then the result is combined with the original image:

[
g = \text{original} + \alpha \cdot (\text{sharpened_base})
]

* The parameter (\alpha) (called `amount` in the code) is set to:

[
\alpha = 0.2 \times \text{intensity}
]

Higher intensity ⇒ stronger sharpening.

#### 6.2 Unsharp Masking

Unsharp masking works in three steps:

1. **Blur** the original image (low-pass filter).
2. Compute the **mask** = original − blurred (this contains mostly edges).
3. Add a scaled version of the mask back to the original image.

Formula:

[
g(x, y) = f(x, y) + k \cdot (f(x, y) - f_{\text{blur}}(x, y))
]

where
(f) = original image,
(f_{\text{blur}}) = blurred image,
(k) = amount (sharpening strength).

In the app:

* Blur: Gaussian blur with

  * Kernel size ( N = 2 \times \text{intensity} + 1 )
  * ( \sigma = \frac{\text{intensity}}{2} )
* Amount ( k = \frac{\text{intensity}}{2} )

---

### 7. Intensity Mapping Summary

The **intensity slider** (1–10) controls filter parameters:

#### Smoothing

* **Average blur**

  * Kernel size ( N = 2I + 1 )
* **Gaussian blur**

  * Kernel size ( N = 2I + 1 )
  * Sigma ( \sigma = I / 2 )
* **Median blur**

  * Kernel size ( N = 2I + 1 )

#### Sharpening

* **Simple sharpening kernel**

  * Fixed kernel (3×3)
  * Amount ( \alpha = 0.2I )
* **Unsharp masking**

  * Gaussian blur kernel size ( N = 2I + 1 )
  * Sigma ( \sigma = I / 2 )
  * Amount ( k = I / 2 )

where ( I ) = intensity level from the slider.

---

### 8. Possible Improvements / Future Work

* Add **more filters** (e.g., Laplacian, Sobel edge detection).
* Add **frequency domain** filtering using the Fourier Transform.
* Allow users to specify their **own custom kernel**.
* Add PSNR / MSE calculations to quantitatively compare original and filtered images.

---

### 9. Conclusion

This project demonstrates how basic spatial filters work in digital image processing:

* **Low-pass filters** (average, Gaussian, median) smooth the image and reduce noise.
* **High-pass filters** (sharpening kernel, unsharp masking) enhance edges and detail.

The interactive Streamlit app helps visualize the effect of different filters and intensity levels on real images, making the theoretical concepts easier to understand.
