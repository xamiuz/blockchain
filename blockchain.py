# blockchain.py
from web3 import Web3
import json
import os
# Koneksi ke Ganache
ganache_url = "http://127.0.0.1:7545"  # Ganti dengan alamat Ganache Anda
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Cek koneksi ke Ganache
if web3.is_connected():
    print("Terhubung dengan Ganache")
else:
    print("Gagal terhubung dengan Ganache")

# ABI dan alamat kontrak yang telah dideploy
contract_address = '0xc4d78C04dF137BCf96cB3523633CEBEb2DDb290f'
abi_path = r"C:\kuliah\blockchain\build\contracts\EmployeeContract.json"
if not os.path.exists(abi_path):
    print(f"[ERROR] ABI file not found at: {abi_path}")
    exit(1)

with open(abi_path, 'r') as abi_file:
    contract_json = json.load(abi_file)
    contract_abi = contract_json['abi']


contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def get_employee(account_address):
    try:
        return contract.functions.getEmployee(account_address).call()
    except Exception as e:
        print(f'Error fetching employee: {e}')
        return None

def update_employee(account_address, private_key, first_name, last_name, job_title, performance_score):
    try:
        account = web3.eth.account.privateKeyToAccount(private_key)
        nonce = web3.eth.getTransactionCount(account.address)

        transaction = contract.functions.updateEmployee(
            first_name, last_name, job_title, performance_score
        ).buildTransaction({
            'from': account.address,
            'nonce': nonce,
            'gas': 20000000,
            'gasPrice': web3.toWei('10', 'gwei')
        })

        signed_txn = web3.eth.account.signTransaction(transaction, private_key)
        txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        receipt = web3.eth.waitForTransactionReceipt(txn_hash)

        return txn_hash.hex()
    except Exception as e:
        print(f'Error updating employee: {e}')
        return None
