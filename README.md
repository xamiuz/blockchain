# Employee Blockchain System

Sistem **Employee Blockchain** ini mengintegrasikan **teknologi blockchain** dengan aplikasi backend berbasis **Flask** untuk mengelola data karyawan secara aman dan terdesentralisasi. Aplikasi ini memungkinkan pengguna untuk:
- Menyimpan dan mengelola data karyawan di blockchain menggunakan kontrak pintar.
- Menyimpan dan mengelola data karyawan di file CSV.
- Menghubungkan antara **private key** dan data karyawan untuk proses pencarian dan pembaruan data.

## Fitur Utama

1. **Kontrak Blockchain**:
   - Data karyawan seperti `EmpID`, `FirstName`, `LastName`, `JobTitle`, dan `PerformanceScore` disimpan di **blockchain** menggunakan kontrak pintar yang ditulis dengan **Solidity**.
   - Interaksi dengan kontrak blockchain dilakukan menggunakan **Web3.py** di Python.

2. **Antarmuka Pengguna**:
   - Menggunakan **Flask** untuk membuat API dan frontend sederhana.
   - Halaman untuk input **Private Key** yang digunakan untuk mengambil atau memperbarui data karyawan.

3. **Pengelolaan CSV**:
   - Menyimpan data karyawan di file **CSV** dan menyediakan API untuk mengunduh dan memperbarui file CSV.

4. **Keamanan**:
   - Penggunaan **private key** untuk mengakses data karyawan dan memperbarui informasi di blockchain.

## Prasyarat

Sebelum menjalankan proyek ini, pastikan Anda sudah menginstal perangkat berikut:

1. **Python 3.x**: Pastikan Python terinstal di sistem Anda.
2. **Ganache**: Digunakan untuk mensimulasikan jaringan Ethereum di lokal (http://127.0.0.1:7545).
3. **Solidity**: Compiler untuk menulis kontrak pintar (gunakan **Truffle** untuk kompilasi dan deploy).
4. **Pustaka Python**:
   - Flask
   - Web3
   - Pandas
   - ECDSA
   - JSON

   Anda bisa menginstal pustaka yang dibutuhkan dengan perintah berikut:
   ```bash
   pip install flask web3 pandas ecdsa

**Struktur Proyek**
bash
Copy code
├── app.py                # Aplikasi Flask untuk backend
├── blockchain.py         # Fungsi interaksi blockchain menggunakan Web3.py
├── EmployeeContract.sol  # Kontrak pintar Solidity untuk menyimpan data karyawan
├── employee_data.csv     # File CSV untuk menyimpan data karyawan
├── employee_keys.csv     # File CSV untuk menyimpan pasangan kunci publik dan privat
└── templates/
    └── index.html        # UI sederhana untuk input private key

**Menjalankan Proyek**
1. Jalankan Ganache
Pastikan Ganache berjalan pada http://127.0.0.1:7545 untuk simulasi jaringan Ethereum lokal.

2. Deploy Kontrak Pintar
Gunakan Truffle atau Remix IDE untuk meng-compile dan meng-deploy kontrak pintar EmployeeContract.sol.
Pastikan Anda mendapatkan contract address dan ABI setelah kontrak dideploy.

3. Konfigurasi Aplikasi Flask
Pada file app.py, pastikan path untuk ABI file dan contract address sudah benar.
Jalankan aplikasi Flask:
bash
python app.py

5. Buka Aplikasi di Browser
Akses aplikasi di browser melalui http://127.0.0.1:5000.
Cara Penggunaan
Generate Keys:
Aplikasi akan secara otomatis menghasilkan private/public key untuk setiap karyawan yang ada di employee_data.csv jika belum ada pasangan kunci.

**Menambahkan Karyawan:**
Ketika data karyawan tidak ditemukan di blockchain, aplikasi akan menambahkan karyawan baru menggunakan data dari file CSV ke dalam kontrak pintar.

**Mengambil Data Karyawan:**
Pengguna dapat memasukkan private key mereka untuk melihat atau mengedit data karyawan mereka.

**Update CSV:**
API /update_csv digunakan untuk memperbarui informasi karyawan dalam file CSV jika ada perubahan di data.

**Unduh File CSV:**
Pengguna dapat mengunduh file CSV yang sudah diperbarui melalui API /download_updated_csv.

**Penjelasan File Utama**
1. app.py
Backend Flask untuk mengelola interaksi dengan kontrak pintar.
Menyediakan beberapa API seperti:
/get_employee_by_key: Mengambil data karyawan menggunakan private key.
/update_csv: Memperbarui informasi karyawan di CSV.
/see_updated_csv: Menampilkan file CSV yang sudah diperbarui.
/download_updated_csv: Menyediakan unduhan file CSV yang telah diperbarui.
2. blockchain.py
Fungsi-fungsi untuk berinteraksi dengan kontrak pintar menggunakan Web3.py:
get_employee(account_address): Mengambil data karyawan berdasarkan alamat akun.
update_employee(): Memperbarui data karyawan di blockchain dengan transaksi Ethereum.
3. EmployeeContract.sol
Kontrak pintar yang menyimpan data karyawan di blockchain.
Fungsi utama yang digunakan: getEmployee untuk mengambil data dan addEmployee untuk menambah karyawan baru.
4. index.html
Halaman antarmuka pengguna yang memungkinkan pengguna untuk memasukkan private key dan mendapatkan data karyawan yang terhubung dengan blockchain.
