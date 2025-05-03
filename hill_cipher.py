import numpy as np

# ==========================
# 1. Fungsi bantu
# ==========================
def char_to_num(c):
    return ord(c.upper()) - 64  # A = 1, ..., Z = 26

def num_to_char(n):
    n = n % 26
    return chr(64 + (26 if n == 0 else n))  # 0 jadi Z

def preprocess_plaintext(plaintext, m):
    plaintext = plaintext.upper().replace(" ", "")
    nums = [char_to_num(c) for c in plaintext]
    
    # Tambahkan padding jika tidak habis dibagi
    while len(nums) % m != 0:
        nums.append(char_to_num('X'))  # padding dengan 'X'
    
    # Bentuk ke blok matriks
    blocks = [nums[i:i+m] for i in range(0, len(nums), m)]
    return np.array(blocks)

# ==========================
# 2. Input data dari pengguna
# ==========================
# Fungsi untuk membaca ukuran matriks
def read_matrix_size():
    size_input = input("Masukkan ukuran matriks kunci (m x m) atau (m*m): ").replace(' ', '')
    size_input = size_input.replace('x', '*')  # Mengganti x menjadi *
    
    try:
        m, n = map(int, size_input.split('*'))  # Mengambil angka sebelum dan sesudah '*'
        if m == n:
            return m
        else:
            print("Matriks harus berbentuk persegi (m x m), dimana m = n.")
            return read_matrix_size()  # Jika tidak persegi, minta input ulang
    except ValueError:
        print("Input tidak valid! Gunakan format 'm x m' atau 'm*m'.")
        return read_matrix_size()

# ==========================
# 2. Input data dari pengguna
# ==========================
# Matriks Kunci K (m x m)
m = read_matrix_size()
K = []

print(f"Masukkan elemen-elemen matriks kunci ({m} x {m}):")
for i in range(m):
    row = list(map(int, input(f"Masukkan elemen baris ke-{i+1} (spasi antar elemen): ").split()))
    K.append(row)

K = np.array(K)  # Matriks Kunci

# Plainteks
plaintext = input("Masukkan plainteks: ")

# ==========================
# 3. Proses Enkripsi
# ==========================
print("\nProses Enkripsi:")
print(f"Plaintext: {plaintext}")

# Preprocess
P_blocks = preprocess_plaintext(plaintext, m)
print("Blok plainteks (numeric):")
print(P_blocks)

# Transpose Pᵗ (m x q)
P_t = P_blocks.T
print("Transpose Pᵗ (m x q):")
print(P_t)

# Hitung Cᵗ = K x Pᵗ  (mod 26)
C_t = np.dot(K, P_t) % 26
print("Hasil Cᵗ = K x Pᵗ (mod 26):")
print(C_t)

# Transpose kembali Cᵗᵗ → C
C = C_t.T
print("C hasil akhir (tiap blok):")
print(C)

# Ubah ke huruf
cipher_chars = [num_to_char(num) for row in C for num in row]
cipher_text = ''.join(cipher_chars)
print("\nCipherteks: ", cipher_text)

# ==========================
# Rapi dan format output
# ==========================
def print_matrix(matrix, title):
    print(f"\n{title}:")
    for row in matrix:
        print(" ".join(f"{int(x):2d}" for x in row))

# Menampilkan hasil enkripsi yang lebih rapi
print_matrix(P_blocks, "Blok plainteks (numeric)")
print_matrix(P_t, "Transpose Pᵗ (m x q)")
print_matrix(C_t, "Hasil Cᵗ = K x Pᵗ (mod 26)")
print_matrix(C, "C hasil akhir (tiap blok)")

# Ciphertext yang lebih rapi
print("\nCipherteks:")
for i in range(0, len(cipher_text), 5):  # menampilkan 5 karakter per baris
    print(cipher_text[i:i+5])
