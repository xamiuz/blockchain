from flask import Flask, jsonify, request, render_template
from web3 import Web3
from ecdsa import SigningKey, SECP256k1
import pandas as pd
import os
import json
from flask import send_file
import csv
import io

app = Flask(__name__)

# Inisialisasi Web3
ganache_url = 'http://127.0.0.1:7545'
web3 = Web3(Web3.HTTPProvider(ganache_url))
CSV_FILE_PATH = 'employee_data.csv'
UPDATED_CSV_FILE = 'updated_employee_data.csv'

if not web3.is_connected():
    print("Web3 is not connected to the Ganache network")
    exit(1)

# Alamat kontrak dan ABI
contract_address = '0xc4d78C04dF137BCf96cB3523633CEBEb2DDb290f'
abi_path = r"C:\kuliah\blockchain\build\contracts\EmployeeContract.json"
if not os.path.exists(abi_path):
    print(f"[ERROR] ABI file not found at: {abi_path}")
    exit(1)

with open(abi_path, 'r') as abi_file:
    contract_json = json.load(abi_file)
    contract_abi = contract_json['abi']


contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Admin private key dan address (deployer kontrak)
admin_private_key = '0xca7830d8c4fe833b4b737f86b6aa2fcb2e4b5595c8dcc394267a3cc5d3f5eaad'
admin_account = web3.eth.account.from_key(admin_private_key)
admin_address = admin_account.address

print(f"[INFO] Admin address: {admin_address}")

# Path ke file CSV utama dan file kunci
employee_data_file = 'employee_data.csv'
employee_keys_file = 'employee_keys.csv'

# Fungsi untuk generate pasangan private/public key
def generate_keys():
    try:
        # Periksa apakah file employee_data.csv ada
        if not os.path.exists(employee_data_file):
            raise FileNotFoundError(f"File {employee_data_file} tidak ditemukan.")

        # Baca file employee_data.csv
        df_data = pd.read_csv(employee_data_file)
        if df_data.empty:
            raise ValueError(f"File {employee_data_file} kosong atau tidak memiliki data yang valid.")

        # Baca atau buat file employee_keys.csv
        if os.path.exists(employee_keys_file):
            df_keys = pd.read_csv(employee_keys_file)
        else:
            df_keys = pd.DataFrame(columns=['FirstName', 'LastName', 'PrivateKey', 'PublicKey'])

        # Buat kunci untuk karyawan yang belum memiliki pasangan kunci
        for _, row in df_data.iterrows():
            first_name = row['FirstName']
            last_name = row['LastName']

            # Cek apakah pasangan kunci sudah ada
            if not ((df_keys['FirstName'] == first_name) & (df_keys['LastName'] == last_name)).any():
                print(f"[INFO] Generating keys for {first_name} {last_name}...")

                # Generate pasangan kunci
                sk = SigningKey.generate(curve=SECP256k1)
                private_key = sk.to_string().hex()
                public_key = sk.verifying_key.to_string().hex()

                # Tambahkan ke DataFrame employee_keys.csv
                df_keys = pd.concat([df_keys, pd.DataFrame([{
                    'FirstName': first_name,
                    'LastName': last_name,
                    'PrivateKey': private_key,
                    'PublicKey': public_key
                }])], ignore_index=True)

        # Simpan kembali ke file employee_keys.csv
        df_keys.to_csv(employee_keys_file, index=False)
        print(f"[INFO] Keys berhasil disimpan di {employee_keys_file}")

    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan saat generate keys: {e}")


@app.route('/')
def index():
    try:
        generate_keys()
    except Exception as e:
        return f"Error generating keys: {str(e)}"
    return render_template('index.html')

# Bagian kode lain tetap sama...

@app.route('/get_employee_by_key', methods=['POST'])
def get_employee_by_key():
    private_key_input = request.form['private_key']
    try:
        print("[DEBUG] Fetching employee by private key...")

        # Generate address from private key
        account = web3.eth.account.from_key(private_key_input)
        address = account.address
        print(f"[INFO] Address generated: {address}")

        # Fetch employee data from contract
        try:
            empID, firstName, lastName, jobTitle, performanceScore = contract.functions.getEmployee(address).call()
        except Exception as e:
            print(f"[ERROR] Fetch failed: {e}")
            empID, firstName, lastName, jobTitle, performanceScore = 0, "", "", "", 0

        # Jika data karyawan tidak ada, tambahkan dari CSV
        if empID == 0:
            print("[INFO] Employee not found. Adding new employee from CSV...")

            # Load CSV files
            df_keys = pd.read_csv(employee_keys_file)
            df_data = pd.read_csv(employee_data_file)

            # Cari private key di keys file
            matching_key = df_keys[df_keys['PrivateKey'] == private_key_input]
            if matching_key.empty:
                return render_template('index.html', error_message="Private key not found in keys file.")

            first_name = matching_key.iloc[0]['FirstName']
            last_name = matching_key.iloc[0]['LastName']
            print(f"[INFO] Found employee in keys CSV: {first_name} {last_name}")

            # Temukan data di data CSV
            matching_data = df_data[(df_data['FirstName'] == first_name) & (df_data['LastName'] == last_name)]
            if matching_data.empty:
                return render_template('index.html', error_message="Employee data not found in data CSV.")

            empID = int(matching_data.iloc[0]['EmpID'])
            jobTitle = matching_data.iloc[0]['Title']
            performance_score_raw = matching_data.iloc[0]['Performance Score']
            performanceScore = {'Fully Meets': 85, 'Exceeds': 95, 'Needs Improvement': 60}.get(performance_score_raw, 0)

            # Kirim transaksi untuk menambahkan data karyawan
            print("[INFO] Adding employee to contract...")
            tx = contract.functions.addEmployee(
                address, empID, first_name, last_name, jobTitle, performanceScore
            ).transact({'from': web3.eth.accounts[0], 'gas': 3000000})

            receipt = web3.eth.wait_for_transaction_receipt(tx)
            print(f"[INFO] Employee added. Transaction hash: {tx.hex()}")

            # Fetch updated data
            empID, firstName, lastName, jobTitle, performanceScore = contract.functions.getEmployee(address).call()

        # Return employee data
        employee = {
            'EmpID': empID,
            'FirstName': firstName,
            'LastName': lastName,
            'JobTitle': jobTitle,
            'PerformanceScore': performanceScore
        }
        # Kirim private key ke edit_employee.html
        return render_template(
            'edit_employee.html',
            employee=employee,
            employee_address=address  # Kirim alamat pegawai
)

    except Exception as e:
        print(f"[ERROR] Exception occurred: {str(e)}")
        return render_template('index.html', error_message="An error occurred during the process.")
    
@app.route('/update_csv', methods=['POST'])
def update_csv():
    data = request.get_json()
    
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    job_title = data.get("job_title")
    performance_score = data.get("performance_score")
    emp_id = data.get("emp_id")  # EmpID yang dikirimkan

    updated = False
    rows = []

    try:
        # Membaca file CSV dan menyimpan semua baris
        with open(CSV_FILE_PATH, mode='r', newline='') as file:
            reader = csv.reader(file)
            header = next(reader)  # Mengambil header
            rows = list(reader)

        # Menyunting baris yang sesuai dengan EmpID
        for row in rows:
            if row[0] == str(emp_id):  # Pastikan EmpID dicocokkan sebagai string
                row[1] = first_name  # FirstName
                row[2] = last_name  # LastName
                row[5] = job_title  # Title
                row[21] = performance_score  # Performance Score
                updated = True
                break

        # Jika EmpID tidak ditemukan, tambahkan data baru ke file CSV
        if not updated:
            rows.append([emp_id, first_name, last_name, '', '', job_title, '', '', '', '', '', '', '', '', '', '', '', '', performance_score, '', '', '', ''])

        # Menulis kembali data yang sudah diperbarui ke file CSV
        with open(CSV_FILE_PATH, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Menulis header
            writer.writerows(rows)  # Menulis semua data

        return jsonify({"success": True}), 200
    except Exception as e:
        print("Error updating CSV:", e)
        return jsonify({"success": False, "error": str(e)}), 500
    
# Route to download the entire CSV file
@app.route('/see_updated_csv', methods=['GET'])
def see_updated_csv():
    try:
        # Read the existing CSV data
        rows = []
        with open(CSV_FILE_PATH, mode='r', newline='') as file:
            reader = csv.reader(file)
            header = next(reader)
            rows = list(reader)

        # Write the updated data to a new CSV file
        with open(UPDATED_CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Write the header
            writer.writerows(rows)   # Write all the data

        return jsonify({"success": True, "message": "Updated CSV file created successfully!"}), 200
    except Exception as e:
        print("Error creating updated CSV:", e)
        return jsonify({"success": False, "error": str(e)}), 500
    
@app.route('/download_updated_csv', methods=['GET'])
def download_updated_csv():
    try:
        return send_file(UPDATED_CSV_FILE, as_attachment=True)
    except Exception as e:
        print("Error downloading updated CSV:", e)
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)