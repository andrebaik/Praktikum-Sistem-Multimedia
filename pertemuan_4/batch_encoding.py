import subprocess
from pathlib import Path

# Folder tempat skrip dan file audio berada
folder = Path(".")

# Daftar file audio sumber
daftar_file = [
    "kerja-bagus-ff.wav",
    "maju3.wav",
    "Minecraft Fall Damage (Crack) - Sound Effect (HD) (320 kbps).wav",
    "poco-x3-phone.wav",
    "what-the-hellllllllllll.wav"
]

print("=" * 45)
print("BATCH ENCODING AUDIO KE MP3 128 KBPS")
print("=" * 45)

# Inisialisasi penghitung
berhasil = 0
gagal = 0

# Siapkan folder output
folder_output = folder / "audio_mp3"
folder_output.mkdir(exist_ok=True)

# Proses encoding setiap file audio
for nama_file in daftar_file:
    sumber = folder / nama_file
    hasil = folder_output / f"{sumber.stem}_128k.mp3"

    print(f"\nMemproses: {nama_file}")

    # Periksa keberadaan file sumber
    if not sumber.exists():
        print(f"Gagal: File {nama_file} tidak ditemukan")
        gagal += 1
        continue

    # Perintah FFmpeg
    perintah = [
        "ffmpeg", "-y",
        "-i", str(sumber),
        "-c:a", "libmp3lame",
        "-b:a", "128k",
        str(hasil)
    ]

    # Jalankan FFmpeg tanpa menampilkan log panjang
    proses = subprocess.run(
        perintah,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Periksa hasil proses encoding
    if proses.returncode == 0 and hasil.exists():
        print(f"Berhasil: {hasil.name}")
        berhasil += 1
    else:
        print(f"Gagal: {nama_file}")
        gagal += 1

# Ringkasan hasil encoding
print("\n" + "=" * 45)
print("RINGKASAN PROSES ENCODING")
print("=" * 45)
print(f"Jumlah file diproses : {berhasil + gagal}")
print(f"Berhasil             : {berhasil}")
print(f"Gagal                : {gagal}")
print("=" * 45)