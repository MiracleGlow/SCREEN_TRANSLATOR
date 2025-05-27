# 📌 Screen Translator

**Screen Translator** adalah aplikasi desktop berbasis Python yang memungkinkan pengguna untuk menerjemahkan teks dari area tertentu di layar secara real-time. Aplikasi ini sangat berguna untuk menerjemahkan teks dari game, subtitle, atau antarmuka perangkat lunak yang tidak memiliki dukungan bahasa lokal.

---

## 🧰 Fitur Utama

* Pemilihan area layar secara interaktif untuk OCR.
* Pengenalan teks (OCR) menggunakan Tesseract dengan dukungan lebih dari 100 bahasa, termasuk Jepang.
* Penerjemahan otomatis menggunakan Google Translate API.
* Antarmuka pengguna sederhana dengan tampilan hasil asli dan terjemahan.
* Pemrosesan gambar lanjutan untuk meningkatkan akurasi OCR.

---

## 🖥️ Prasyarat

Pastikan Anda telah menginstal perangkat lunak dan pustaka berikut:

1. **Python 3.6 atau lebih baru**

2. **Tesseract OCR**

   * **Windows**: Unduh dan instal dari [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract). Pastikan untuk menambahkan path Tesseract ke variabel lingkungan sistem.
   * **Linux/macOS**: Gunakan manajer paket seperti `apt` atau `brew`.

3. **Pustaka Python**

   Instal pustaka yang diperlukan dengan perintah:

   ```bash
   pip install mss opencv-python pytesseract googletrans==4.0.0-rc1 Pillow numpy
   ```

---

## 📂 Struktur Proyek

```
screen-translator/
├── main.py
├── README.md
└── requirements.txt
```

---

## ⚙️ Konfigurasi

1. **Path Tesseract**

   Pastikan untuk mengatur path ke executable Tesseract dalam kode:

   ```python
   pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
   ```

   Sesuaikan path sesuai dengan lokasi instalasi Tesseract di sistem Anda.

2. **Data Bahasa**

   Pastikan file data bahasa yang diperlukan (misalnya, `jpn.traineddata` untuk bahasa Jepang) tersedia di direktori `tessdata`. Jika belum tersedia, unduh dari [https://github.com/tesseract-ocr/tessdata](https://github.com/tesseract-ocr/tessdata) dan tempatkan di direktori yang sesuai.

---

## 🚀 Cara Menggunakan

1. Jalankan aplikasi dengan perintah:

   ```bash
   python main.py
   ```

2. Klik tombol **"Pilih Area"** untuk memilih area layar yang ingin diterjemahkan.

3. Setelah area dipilih, klik tombol **"Mulai Terjemahan"** untuk memulai proses OCR dan terjemahan secara real-time.

4. Hasil teks asli dan terjemahan akan ditampilkan di antarmuka aplikasi.

---

## 🧪 Pemrosesan Gambar untuk Meningkatkan Akurasi OCR

Untuk meningkatkan akurasi OCR, terutama untuk teks berbahasa Jepang, aplikasi ini menerapkan beberapa teknik pemrosesan gambar:

* **Penskalaan Gambar**: Memperbesar gambar untuk memastikan tinggi karakter mencukupi.
* **Konversi ke Grayscale**: Mengurangi kompleksitas warna.
* **Gaussian Blur**: Mengurangi noise pada gambar.
* **Thresholding Adaptif**: Mengubah gambar ke format biner untuk memudahkan deteksi teks.
* **Operasi Morfologi (Dilasi)**: Memperbaiki struktur teks yang terputus.([Stack Overflow][1])

Teknik-teknik ini membantu dalam meningkatkan kualitas input untuk Tesseract, sehingga hasil OCR menjadi lebih akurat.

---

## 🛠️ Konfigurasi Tesseract

Aplikasi ini menggunakan konfigurasi berikut untuk Tesseract:

* **OEM (OCR Engine Mode)**: `3` (menggunakan LSTM dan legacy engine).
* **PSM (Page Segmentation Mode)**: `6` (mengasumsikan blok teks tunggal).

Konfigurasi ini dipilih untuk keseimbangan antara akurasi dan kecepatan dalam pengenalan teks.

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah [Lisensi MIT](https://opensource.org/licenses/MIT).

---

## 🙏 Kontribusi

Kontribusi sangat diterima! Jika Anda memiliki saran, perbaikan, atau fitur baru yang ingin ditambahkan, silakan buat [Issue](https://github.com/username/screen-translator/issues) atau ajukan [Pull Request](https://github.com/username/screen-translator/pulls).

---

## 📚 Referensi

* [Dokumentasi Resmi Tesseract](https://tesseract-ocr.github.io/)
* [PyTesseract di PyPI](https://pypi.org/project/pytesseract/)
* [Googletrans di PyPI](https://pypi.org/project/googletrans/)
* [OpenCV Dokumentasi](https://docs.opencv.org/)([Tesseract OCR][2])

---

Dengan dokumentasi ini, pengguna dapat dengan mudah memahami, menginstal, dan menggunakan aplikasi Screen Translator untuk kebutuhan penerjemahan teks dari layar secara real-time.

---

[1]: https://stackoverflow.com/questions/28935983/preprocessing-image-for-tesseract-ocr-with-opencv?utm_source=chatgpt.com "Preprocessing image for Tesseract OCR with OpenCV"
[2]: https://tesseract-ocr.github.io/?utm_source=chatgpt.com "Tesseract documentation | Tesseract OCR"
