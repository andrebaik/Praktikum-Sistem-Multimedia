from pathlib import Path
import math
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from skimage.metrics import (
    peak_signal_noise_ratio as psnr_skimage,  # Diubah agar tidak bentrok nama variabel
    structural_similarity as ssim_skimage      # Diubah agar tidak bentrok nama variabel
)

# Menyiapkan folder untuk menyimpan hasil
folder_hasil = Path("hasil")
folder_hasil.mkdir(exist_ok=True)

# Membuka gambar asli (Grayscale)
img_asli = Image.open("input.jpg").convert("L")
arr_asli = np.array(img_asli)

print("Gambar berhasil dibuka")
print("Dimensi gambar asli:", img_asli.size)
print("Mode Warna gambar asli:", img_asli.mode)
print("Bentuk array gambar asli:", arr_asli.shape)

# Fungsi menghitung MSE
def hitung_mse(gambar_asli, gambar_kompresi):
    selisih = (
        gambar_asli.astype(np.float64) -
        gambar_kompresi.astype(np.float64)
    )
    mse = np.mean(selisih ** 2)
    return mse  

# Fungsi menghitung PSNR secara manual
def hitung_psnr_manual(mse, max_pixel=255):
    if mse == 0:
        return float("inf")
    return 10 * math.log10((max_pixel ** 2) / mse)

# Daftar gambar jpeg
daftar_jpeg = {
    "JPEG 10": "hasil/jpeg_10.jpeg",
    "JPEG 50": "hasil/jpeg_50.jpeg",
    "JPEG 90": "hasil/jpeg_90.jpeg"
}

print("\nMULAI PERHITUNGAN MSE, PSNR MANUAL")

for name, nama_file in daftar_jpeg.items():
    img_kompresi = Image.open(nama_file).convert("L")
    arr_kompresi = np.array(img_kompresi)

    # Memastikan dimensi gambar sama
    if arr_asli.shape != arr_kompresi.shape:
        raise ValueError(f"Dimensi gambar tidak sama: {nama_file}")

    # Menghitung MSE & PSNR
    mse = hitung_mse(arr_asli, arr_kompresi)
    nilai_psnr = hitung_psnr_manual(mse)

    print(f"\n{name}")
    print(f"MSE: {mse:.4f}")
    print(f"PSNR: {nilai_psnr:.2f} dB")

print("\nPerbandingan PSNR Manual dan Scikit-image")

for nama, nama_file in daftar_jpeg.items():
    img_kompresi = Image.open(nama_file).convert("L")
    arr_kompresi = np.array(img_kompresi)

    mse = hitung_mse(arr_asli, arr_kompresi)
    psnr_manual = hitung_psnr_manual(mse)

    # Memanggil psnr_skimage dari import alias
    nilai_psnr_skimage = psnr_skimage(
        arr_asli,
        arr_kompresi,
        data_range=255
    )

    print(f"\n{nama}")
    print(f"PSNR Manual  : {psnr_manual:.2f} dB")
    print(f"PSNR Skimage : {nilai_psnr_skimage:.2f} dB")

print("\nPERHITUNGAN SSIM")

for nama, nama_file in daftar_jpeg.items():
    img_kompresi = Image.open(nama_file).convert("L")
    arr_kompresi = np.array(img_kompresi)

    # Memanggil ssim_skimage (tanpa channel_axis untuk gambar Grayscale)
    nilai_ssim = ssim_skimage(
        arr_asli,
        arr_kompresi,
        data_range=255
    )

    print(f"{nama}")
    print(f"SSIM : {nilai_ssim:.4f}\n")

# Daftar gambar JPEG dan WebP
daftar_file = {
    "JPEG 10": "hasil/jpeg_10.jpeg",
    "JPEG 50": "hasil/jpeg_50.jpeg",
    "JPEG 90": "hasil/jpeg_90.jpeg",
    "WebP 10": "hasil/webp_10.webp",
    "WebP 50": "hasil/webp_50.webp",
    "WebP 90": "hasil/webp_90.webp"
}

print("\nPERBANDINGAN JPEG DAN WEBP")

data_hasil = []

for nama, nama_file in daftar_file.items():
    img_kompresi = Image.open(nama_file).convert("L")
    arr_kompresi = np.array(img_kompresi)

    if arr_asli.shape != arr_kompresi.shape:
        raise ValueError(f"Dimensi gambar tidak sama: {nama_file}")

    mse = hitung_mse(arr_asli, arr_kompresi)
    nilai_psnr = hitung_psnr_manual(mse)
    nilai_ssim = ssim_skimage(
        arr_asli,
        arr_kompresi,
        data_range=255
    )
    ukuran_file = Path(nama_file).stat().st_size

    data_hasil.append({
        "nama": nama,
        "ukuran": ukuran_file,
        "psnr": nilai_psnr,
        "ssim": nilai_ssim
    })

# Menampilkan tabel hasil
print("\nTABEL PERBANDINGAN JPEG DAN WEBP")
print("-" * 75)
print(f"{'Format':<15} {'Ukuran (byte)':>15} {'PSNR (dB)':>15} {'SSIM':>12}")
print("-" * 75)

for data in data_hasil:
    print(f"{data['nama']:<15} {data['ukuran']:>15} {data['psnr']:>15.2f} {data['ssim']:>12.4f}")

# Grafik PSNR terhadap ukuran file
plt.figure(figsize=(9, 5))

for format_gambar in ["JPEG", "WebP"]:
    data_format = [
        d for d in data_hasil
        if d["nama"].startswith(format_gambar)
    ]
    plt.plot(
        [d["ukuran"] / 1024 for d in data_format],
        [d["psnr"] for d in data_format],
        marker="o",
        label=format_gambar
    )

plt.title("Perbandingan PSNR terhadap Ukuran File")
plt.xlabel("Ukuran File (KB)")
plt.ylabel("PSNR (dB)")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(folder_hasil / "grafik_psnr.png")
plt.close()

print("\nGrafik PSNR berhasil disimpan.")

# Grafik SSIM terhadap ukuran file
plt.figure(figsize=(9, 5))

for format_gambar in ["JPEG", "WebP"]:
    data_format = [
        d for d in data_hasil
        if d["nama"].startswith(format_gambar)
    ]
    plt.plot(
        [d["ukuran"] / 1024 for d in data_format],
        [d["ssim"] for d in data_format],
        marker="o",
        label=format_gambar
    )

plt.title("Perbandingan SSIM terhadap Ukuran File")
plt.xlabel("Ukuran File (KB)")
plt.ylabel("SSIM")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(folder_hasil / "grafik_ssim.png")
plt.close()

print("Grafik SSIM berhasil disimpan.")