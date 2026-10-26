from PIL import Image
from pathlib import Path
import matplotlib.pyplot as plt

#Menyiapkan folder hasil
folder_hasil = Path("hasil")
folder_hasil.mkdir(exist_ok=True)

#Membuka gambar sumber
img = Image.open("input.jpg").convert("RGB")

print("Gambar berhasil dibuka")
print("Dimensi gambar:", img.size)
print("Mode warna:", img.mode)

#Konversi model warna
rgb = img
grayscale = img.convert("L")
hsv = img.convert("HSV")

#Menyimpan hasil konversi
rgb.save(folder_hasil / "gambar_rgb.png")
grayscale.save(folder_hasil / "gambar_grayscale.png")

# Konversi kembali ke RGB agar bisa disimpan sebagai PNG
hsv.convert("RGB").save(folder_hasil / "gambar_hsv.png")

print("Semua hasil konversi berhasil disimpan.")

#Menampilkan dan menyimpan perbandingan model warna
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

axes[0].imshow(rgb)
axes[0].set_title("RGB")

axes[1].imshow(grayscale, cmap="gray")
axes[1].set_title("Grayscale")

axes[2].imshow(hsv.convert("RGB"))
axes[2].set_title("HSV")

for ax in axes:
    ax.axis("off")

plt.tight_layout()

# Simpan visualisasi, lalu tutup agar program berlanjut
fig.savefig(folder_hasil / "perbandingan_warna.png")
plt.close(fig)

print("Visualisasi perbandingan warna berhasil disimpan.")

#Kompresi gambar ke format JPEG
print("\nMULAI KOMPRESI JPEG")

for kualitas in [10, 50, 90]:
    nama_file = folder_hasil / f"jpeg_{kualitas}.jpeg"

    img.save(
        nama_file,
        format="JPEG",
        quality=kualitas
    )

    ukuran = nama_file.stat().st_size

    print(f"Berhasil: {nama_file.name}")
    print(f"Ukuran file: {ukuran} byte")

print("\nSemua proses selesai.")

# Kompresi ke format PNG
nama_png = folder_hasil / "gambar.png"

img.save(nama_png, format="PNG")

print(f"Berhasil: {nama_png.name}")
print(f"Ukuran: {nama_png.stat().st_size} byte")

# Kompresi ke format WebP
print("\nMULAI KOMPRESI WEBP")

for kualitas in [10, 50, 90]:
    nama_file = folder_hasil / f"webp_{kualitas}.webp"

    img.save(
        nama_file,
        format="WEBP",
        quality=kualitas
    )

    ukuran = nama_file.stat().st_size

    print(f"Berhasil: {nama_file.name}")
    print(f"Ukuran file: {ukuran} byte")
    
    # Tabel perbandingan ukuran file dan kualitas
print("\nTABEL PERBANDINGAN UKURAN FILE DAN KUALITAS")
print("-" * 65)
print(f"{'Nama File':<25} {'Kualitas':<15} {'Ukuran (byte)':>18}")
print("-" * 65)

for file in sorted(folder_hasil.iterdir()):
    if file.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]:
        nama = file.name.lower()
        kualitas = "-"

        if nama.startswith("jpeg_"):
            kualitas = nama.split("_")[1].split(".")[0]
        elif nama.startswith("webp_"):
            kualitas = nama.split("_")[1].split(".")[0]
        elif file.suffix.lower() == ".png":
            kualitas = "Lossless"

        print(
            f"{file.name:<25} "
            f"{kualitas:<15} "
            f"{file.stat().st_size:>18,}"
        )

print("-" * 65)
print("Semua proses kompresi selesai.")

    # ==========================================
# 3. VISUALISASI HISTOGRAM RGB
# ==========================================

print("\nMEMBUAT HISTOGRAM RGB")

warna = ["red", "green", "blue"]

fig, ax = plt.subplots(figsize=(10, 5))

for i, nama_warna in enumerate(warna):
    kanal = img.getchannel(i)
    histogram = kanal.histogram()

    ax.plot(histogram, color=nama_warna, label=nama_warna)

ax.set_title("Histogram RGB Gambar Asli")
ax.set_xlabel("Nilai Intensitas Piksel")
ax.set_ylabel("Jumlah Piksel")
ax.legend()
plt.tight_layout()

fig.savefig(folder_hasil / "histogram_rgb.png")
plt.close(fig)

print("Histogram RGB berhasil disimpan.")


# ==========================================
# HISTOGRAM GRAYSCALE
# ==========================================

print("\nMEMBUAT HISTOGRAM GRAYSCALE")

grayscale = img.convert("L")
histogram_gray = grayscale.histogram()

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(histogram_gray, color="gray")
ax.set_title("Histogram Grayscale Gambar Asli")
ax.set_xlabel("Nilai Intensitas Piksel")
ax.set_ylabel("Jumlah Piksel")

plt.tight_layout()
fig.savefig(folder_hasil / "histogram_grayscale.png")
plt.close(fig)

print("Histogram Grayscale berhasil disimpan.")

# ==========================================
# PERBANDINGAN HISTOGRAM SEBELUM DAN SESUDAH JPEG
# ==========================================

print("\nMEMBANDINGKAN HISTOGRAM JPEG")

file_jpeg = folder_hasil / "jpeg_10.jpeg"

# Pastikan file JPEG tersedia
if file_jpeg.exists():
    # Gambar asli dan hasil JPEG diubah ke Grayscale
    gray_asli = img.convert("L")
    gray_jpeg = Image.open(file_jpeg).convert("L")

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        gray_asli.histogram(),
        label="Gambar Asli"
    )

    ax.plot(
        gray_jpeg.histogram(),
        label="JPEG Kualitas 10"
    )

    ax.set_title("Perbandingan Histogram Sebelum dan Sesudah JPEG")
    ax.set_xlabel("Nilai Intensitas Piksel")
    ax.set_ylabel("Jumlah Piksel")
    ax.legend()

    plt.tight_layout()
    fig.savefig(folder_hasil / "perbandingan_histogram_jpeg.png")
    plt.close(fig)

    print("Perbandingan histogram berhasil disimpan.")
else:
    print("File jpeg_10.jpeg tidak ditemukan. Jalankan kompresi JPEG terlebih dahulu.")
    
    # ==========================================
# 4. ANALISIS EFEK RESIZING
# ==========================================

print("\nMEMULAI ANALISIS RESIZING")

ukuran_asli = img.size
ukuran_file_asli = Path("input.jpg").stat().st_size

print("Dimensi asli:", ukuran_asli)
print("Ukuran file asli:", ukuran_file_asli, "byte")

for persentase in [50, 25, 10]:
    lebar = max(1, int(img.width * persentase / 100))
    tinggi = max(1, int(img.height * persentase / 100))

    hasil_resize = img.resize(
        (lebar, tinggi),
        Image.Resampling.LANCZOS
    )

    nama_file = folder_hasil / f"resize_{persentase}.jpg"

    hasil_resize.save(
        nama_file,
        format="JPEG",
        quality=90
    )

    ukuran_file = nama_file.stat().st_size

    print(f"\nResize {persentase}%")
    print(f"Dimensi: {lebar} x {tinggi}")
    print(f"Ukuran file: {ukuran_file} byte")

print("\nProses resizing selesai.")

# ==========================================
# VISUALISASI PERBANDINGAN RESIZING
# ==========================================

persentase_resize = [50, 25, 10]

fig, axes = plt.subplots(1, 4, figsize=(16, 6))

axes[0].imshow(img)
axes[0].set_title("Gambar Asli")

for ax, persentase in zip(axes[1:], persentase_resize):
    nama_file = folder_hasil / f"resize_{persentase}.jpg"
    gambar = Image.open(nama_file)

    ax.imshow(gambar)
    ax.set_title(f"Resize {persentase}%")

for ax in axes:
    ax.axis("off")

plt.tight_layout()
fig.savefig(folder_hasil / "perbandingan_resizing.png")
plt.close(fig)

print("Perbandingan resizing berhasil disimpan.")

# ==========================================
# TABEL HASIL RESIZING
# ==========================================

print("\nTABEL HASIL RESIZING")
print("-" * 60)
print(f"{'File':<22} {'Dimensi':<18} {'Ukuran (byte)':>15}")
print("-" * 60)

print(
    f"{'input.jpg':<22} "
    f"{img.width} x {img.height:<10} "
    f"{ukuran_file_asli:>15,}"
)

for persentase in [50, 25, 10]:
    nama_file = folder_hasil / f"resize_{persentase}.jpg"
    gambar = Image.open(nama_file)
    ukuran_file = nama_file.stat().st_size

    print(
        f"{nama_file.name:<22} "
        f"{gambar.width} x {gambar.height:<10} "
        f"{ukuran_file:>15,}"
    )

print("-" * 60)