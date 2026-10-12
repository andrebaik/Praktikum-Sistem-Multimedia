#Implementasi RLE
data = "AAAAAAABBBCC"
print(data)

def rle_encode(data):
    hasil = []

    if not data:
        return hasil

    jumlah = 1

    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            jumlah += 1
        else:
            hasil.append((data[i - 1], jumlah))
            jumlah = 1

    hasil.append((data[-1], jumlah))

    return hasil

encoded = rle_encode(data)

print(encoded)

#Membuat Fungsi rle_decode
def rle_decode(data):
    hasil = ""

    for simbol, jumlah in data:
        hasil += simbol * jumlah

    return hasil

decoded = rle_decode(encoded)

print(decoded)

#Verifikasi RLE 
print("Data asli   :", data)
print("Hasil decode:", decoded)
print("Identik     :", data == decoded)