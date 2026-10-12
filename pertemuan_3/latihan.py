import wave
import heapq
from collections import Counter

# ==================================================
# 1. HUFFMAN CODING
# ==================================================

def huffman_encode(data):
    if not data:
        return "", {}

    frekuensi = Counter(data)
    heap = []
    nomor = 0

    # Memasukkan simbol dan frekuensi ke heap
    for simbol, jumlah in frekuensi.items():
        heapq.heappush(
            heap, (jumlah, nomor, ("leaf", simbol))
        )
        nomor += 1

    # Jika hanya ada satu jenis simbol
    if len(heap) == 1:
        simbol = heap[0][2][1]
        return "0" * len(data), {simbol: "0"}

    # Membentuk Huffman Tree
    while len(heap) > 1:
        frek1, _, kiri = heapq.heappop(heap)
        frek2, _, kanan = heapq.heappop(heap)

        gabungan = ("node", kiri, kanan)

        heapq.heappush(
            heap, (frek1 + frek2, nomor, gabungan)
        )
        nomor += 1

    tree = heap[0][2]
    codes = {}

    # Membuat kode untuk setiap simbol
    def buat_kode(node, kode=""):
        if node[0] == "leaf":
            codes[node[1]] = kode
            return

        buat_kode(node[1], kode + "0")
        buat_kode(node[2], kode + "1")

    buat_kode(tree)

    encoded = "".join(codes[simbol] for simbol in data)

    return encoded, codes


def huffman_decode(encoded, codes):
    if not codes:
        return b""

    # Membalik kode agar bisa digunakan untuk decode
    kode_ke_simbol = {
        kode: simbol for simbol, kode in codes.items()
    }

    hasil = bytearray()
    sementara = ""

    for bit in encoded:
        sementara += bit

        if sementara in kode_ke_simbol:
            hasil.append(kode_ke_simbol[sementara])
            sementara = ""

    return bytes(hasil)


# ==================================================
# 2. RUN-LENGTH ENCODING (RLE)
# ==================================================

def rle_encode(data):
    hasil = []

    if not data:
        return hasil

    simbol = data[0]
    jumlah = 1

    for nilai in data[1:]:
        if nilai == simbol and jumlah < 0xFFFFFFFF:
            jumlah += 1
        else:
            hasil.append((simbol, jumlah))
            simbol = nilai
            jumlah = 1

    hasil.append((simbol, jumlah))

    return hasil


def rle_decode(data):
    hasil = bytearray()

    for simbol, jumlah in data:
        hasil.extend(bytes([simbol]) * jumlah)

    return bytes(hasil)


# ==================================================
# 3. FUNGSI PENGUJIAN DATASET
# ==================================================

def uji_dataset(nama, data):
    if not data:
        print(f"\nDataset {nama} kosong.")
        return None

    # ----- Huffman -----
    encoded_huffman, codes = huffman_encode(data)
    decoded_huffman = huffman_decode(
        encoded_huffman, codes
    )

    ukuran_asli = len(data)

    # Payload Huffman dibulatkan ke byte
    ukuran_huffman = (len(encoded_huffman) + 7) // 8

    # ----- RLE -----
    encoded_rle = rle_encode(data)
    decoded_rle = rle_decode(encoded_rle)

    # Asumsi representasi RLE:
    # 1 byte simbol + 4 byte jumlah pengulangan
    ukuran_rle = len(encoded_rle) * 5

    # ----- Verifikasi -----
    if decoded_huffman != data:
        raise ValueError(f"Decode Huffman gagal pada {nama}")

    if decoded_rle != data:
        raise ValueError(f"Decode RLE gagal pada {nama}")

    # ----- Rasio kompresi -----
    rasio_huffman = (
        ukuran_asli / ukuran_huffman
        if ukuran_huffman > 0 else 0
    )

    rasio_rle = (
        ukuran_asli / ukuran_rle
        if ukuran_rle > 0 else 0
    )

    print(f"\n{'=' * 45}")
    print(f"Dataset: {nama}")
    print(f"Ukuran asli       : {ukuran_asli} byte")
    print(f"Ukuran Huffman    : {ukuran_huffman} byte")
    print(f"Rasio Huffman     : {rasio_huffman:.2f}:1")
    print(f"Jumlah pasangan RLE: {len(encoded_rle)}")
    print(f"Ukuran RLE        : {ukuran_rle} byte")
    print(f"Rasio RLE         : {rasio_rle:.2f}:1")
    print("Decode Huffman identik:", decoded_huffman == data)
    print("Decode RLE identik    :", decoded_rle == data)

    return [
        nama,
        ukuran_asli,
        ukuran_huffman,
        rasio_huffman,
        ukuran_rle,
        rasio_rle
    ]


# ==================================================
# 4. MEMBACA TIGA DATASET
# ==================================================

# Dataset 1: teks alami
with open("t.txt", "rb") as file:
    data_teks = file.read()

# Dataset 2: audio dengan keheningan
with wave.open("hening.wav", "rb") as audio:
    data_audio_senyap = audio.readframes(
        audio.getnframes()
    )

# Dataset 3: audio noise
with wave.open("brisik.wav", "rb") as audio:
    data_noise = audio.readframes(
        audio.getnframes()
    )


# ==================================================
# 5. MENJALANKAN PENGUJIAN
# ==================================================

hasil = []

hasil.append(
    uji_dataset("Teks alami", data_teks)
)

hasil.append(
    uji_dataset("Audio senyap", data_audio_senyap)
)

hasil.append(
    uji_dataset("Audio noise", data_noise)
)


# ==================================================
# 6. MENAMPILKAN TABEL PERBANDINGAN
# ==================================================

print("\n\n========== TABEL PERBANDINGAN ==========")

print(
    f"{'Dataset':<18}"
    f"{'Asli (B)':>12}"
    f"{'Huffman (B)':>15}"
    f"{'Rasio H':>12}"
    f"{'RLE (B)':>12}"
    f"{'Rasio R':>12}"
)

print("-" * 81)

for baris in hasil:
    if baris is not None:
        nama, asli, huffman, rasio_h, rle, rasio_r = baris

        print(
            f"{nama:<18}"
            f"{asli:>12}"
            f"{huffman:>15}"
            f"{rasio_h:>11.2f}:1"
            f"{rle:>12}"
            f"{rasio_r:>11.2f}:1"
        )

print("\nPengujian selesai.")