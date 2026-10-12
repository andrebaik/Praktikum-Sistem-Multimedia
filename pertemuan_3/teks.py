#Implementasi Program Huffman
from collections import Counter
import heapq

def build_huffman_tree(data):
    frekuensi = Counter(data)

    heap = [[jumlah, simbol] for simbol, jumlah in frekuensi.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        kiri = heapq.heappop(heap)
        kanan = heapq.heappop(heap)

        gabungan = [
            kiri[0] + kanan[0],
            kiri,
            kanan
        ]

        heapq.heappush(heap, gabungan)

    return heap[0]

#Membuat Kode dari Huffman Tree
def build_codes(tree, kode="", codes=None):
    if codes is None:
        codes = {}

    if len(tree) == 2:
        simbol = tree[1]
        codes[simbol] = kode or "0"
        return codes
    
    build_codes(tree[1], kode + "0", codes)
    build_codes(tree[2], kode + "1", codes)

    return codes

data = "AAAAABBBC"

tree = build_huffman_tree(data)
codes = build_codes(tree)

print(codes)

#Proses Encode
def encode(data, codes):
    return ''.join(codes[karakter] for karakter in data)
encoded = encode(data, codes)

print("Data asli   :", data)
print("Hasil encode:", encoded)

#Proses Decode
def decode(encoded, tree):
    hasil = []
    node = tree

    for bit in encoded:
        node = node[1] if bit == "0" else node[2]

        if len(node) == 2:
            hasil.append(node[1])
            node = tree

    return ''.join(hasil)
decoded = decode(encoded, tree)

print("Hasil decode:", decoded)

#Verifikasi Hasil Decode
print("Data asli  :", data)
print("Hasil decode:", decoded)
print("Identik    :", data == decoded)