import sqlite3  # Mengimpor modul SQLite untuk mengelola database lokal
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk  # Mengimpor modul Tkinter untuk GUI

# Fungsi untuk membuat database dan tabel
def create_database():
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka/menyambung ke file database SQLite
    cursor = conn.cursor()  # Membuat kursor untuk menjalankan perintah SQL
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    ''')  # Membuat tabel jika belum ada
    conn.commit()  # Menyimpan perubahan ke database
    conn.close()  # Menutup koneksi

# Fungsi untuk mengambil data dari tabel
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa")  # Menjalankan query untuk mengambil semua data
    rows = cursor.fetchall()  # Mengambil semua baris data
    conn.close()
    return rows  # Mengembalikan hasil

# Fungsi untuk menyimpan data baru ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))  # Menambahkan data baru ke tabel
    conn.commit()
    conn.close()

# Fungsi untuk memperbarui data dalam database
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))  # Memperbarui data berdasarkan ID
    conn.commit()
    conn.close()

# Fungsi untuk menghapus data dari database
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))  # Menghapus data berdasarkan ID
    conn.commit()
    conn.close()

# Fungsi untuk menghitung prediksi fakultas berdasarkan nilai
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Diketahui"

# Fungsi untuk menangani input saat menekan tombol "Add"
def submit():
    try:
        nama = nama_var.get()  # Mengambil input nama dari GUI
        biologi = int(biologi_var.get())  # Mengambil dan mengonversi input nilai biologi ke integer
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise Exception("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)  # Menghitung prediksi fakultas
        save_to_database(nama, biologi, fisika, inggris, prediksi)  # Menyimpan data ke database

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        clear_inputs()  # Mengosongkan input
        populate_table()  # Memperbarui tabel
    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")

# Fungsi untuk memperbarui data saat menekan tombol "Update"
def update():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk di-update!")

        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menghapus data saat menekan tombol "Delete"
def delete():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())
        delete_database(record_id)
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk mengosongkan input
def clear_inputs():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("")

# Fungsi untuk mengisi tabel dengan data dari database
def populate_table():
    for row in tree.get_children():
        tree.delete(row)  # Menghapus semua data di tabel sebelumnya
    for row in fetch_data():
        tree.insert('', 'end', values=row)  # Menambahkan data baru ke tabel

# Fungsi untuk mengisi input berdasarkan baris yang dipilih di tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]  # Mengambil ID baris yang dipilih
        selected_row = tree.item(selected_item)['values']  # Mengambil data dari baris tersebut

        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")

# Inisialisasi database
create_database()

# Membuat GUI dengan tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")

# Variabel tkinter
nama_var = StringVar()  # Untuk menyimpan input nama
biologi_var = StringVar()  # Untuk menyimpan input nilai biologi
fisika_var = StringVar()  # Untuk menyimpan input nilai fisika
inggris_var = StringVar()  # Untuk menyimpan input nilai Inggris
selected_record_id = StringVar()  # Untuk menyimpan ID record yang dipilih

# Menambahkan label dan input ke GUI
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)  # Tombol untuk menambahkan data
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)  # Tombol untuk memperbarui data
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)  # Tombol untuk menghapus data

# Tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')  # Membuat tabel

# Mengatur posisi isi tabel di tengah
for col in columns:
    tree.heading(col, text=col.capitalize())  # Menambahkan heading
    tree.column(col, anchor='center')  # Mengatur

tree.column(col, anchor='center')  # Mengatur posisi teks di tengah

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)  # Menempatkan tabel di GUI

tree.bind('<ButtonRelease-1>', fill_inputs_from_table)  # Menghubungkan event klik tabel ke fungsi pengisian input

populate_table()  # Mengisi tabel dengan data dari database

# Menjalankan aplikasi GUI
root.mainloop()  # Memulai loop utama aplikasi