import json
import os
import requests

def baca_referensi():
    try:
        with open('referensi.json', 'r') as file:
            data = json.load(file)
            return data['nomor_referensi']
    except FileNotFoundError:
        return []

def tampilkan_referensi():
    nomor_ref = baca_referensi()
    print("\nDaftar Nomor Referensi:")
    for i, nomor in enumerate(nomor_ref, 1):
        print(f"{i}. {nomor}")
    return nomor_ref

def baca_hasil_gabungan():
    try:
        with open('asset/hasil_gabungan.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def tampilkan_detail(nomor_referensi):
    data = baca_hasil_gabungan()
    found = False
    
    for item in data:
        if item['ACTACCU'] == nomor_referensi:
            found = True
            print("\nDetail Informasi:")
            print("----------------")
            for key, value in item.items():
                print(f"{key}: {value}")
            print("----------------")
    
    if not found:
        print(f"Nomor referensi {nomor_referensi} tidak ditemukan dalam data.")

def input_nomor_referensi():
    nomor_referensi = []
    
    orang = input("Berapa Orang Rencana Penanganan Hari Ini: ")
    
    # Meminta input nomor cif
    for i in range(int(orang)):
        nomor = input(f"Nomor referensi ke-{i+1}: ")
        nomor_referensi.append(nomor)
    
    # Opsional: meminta input tambahan hingga maksimal 6 nomor
    for i in range(int(orang), 6):
        tambah = input(f"Tambahkan nomor ke-{i+1}? (y/n): ").lower()
        if tambah == 'y':
            nomor = input(f"Nomor referensi ke-{i+1}: ")
            nomor_referensi.append(nomor)
        else:
            break
    
    return nomor_referensi

def simpan_ke_json(data):
    with open('referensi.json', 'w') as file:
        json.dump({"nomor_referensi": data}, file, indent=4)
    print("Data berhasil disimpan ke referensi.json")

def menu_penanganan():
    print("\nMenu Penanganan")
    print("---------------")
    nomor_ref = input_nomor_referensi()
    simpan_ke_json(nomor_ref)
    
    # Menampilkan data yang disimpan
    print("\nData yang disimpan:")
    for i, nomor in enumerate(nomor_ref, 1):
        print(f"{i}. {nomor}")

def sync_data():
    print("\nSync Data dari GitHub...")
    url = "https://raw.githubusercontent.com/andoteger/dt_nunggak/main/hasil_gabungan.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Memeriksa apakah request berhasil
        
        data = response.json()
        
        with open('hasil_gabungan.json', 'w') as file:
            json.dump(data, file, indent=4)
        
        print("Sync data berhasil! Data terbaru telah didownload.")
    except requests.exceptions.RequestException as e:
        print(f"Gagal sync data: {e}")
    except json.JSONDecodeError:
        print("Error: Data yang diterima bukan format JSON yang valid")

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== MENU UTAMA ===")
        nomor_ref = tampilkan_referensi()
        
        print("\nPilihan Menu:")
        for i, nomor in enumerate(nomor_ref, 1):
            print(f"{i}. Lihat detail {nomor}")
        print("99. Orang Penanganan")
        print("999. Sync Data (Download dari GitHub)")
        print("00. Keluar")
        
        pilihan = input("\nMasukkan pilihan: ")
        
        if pilihan == '00':
            print("Terima kasih, program selesai.")
            break
        elif pilihan == '99':
            menu_penanganan()
            input("\nTekan Enter untuk kembali ke menu utama...")
        elif pilihan == '999':
            sync_data()
            input("\nTekan Enter untuk kembali ke menu utama...")
        elif pilihan.isdigit() and 1 <= int(pilihan) <= len(nomor_ref):
            nomor_dipilih = nomor_ref[int(pilihan)-1]
            tampilkan_detail(nomor_dipilih)
            input("\nTekan Enter untuk kembali ke menu utama...")
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("\nTekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    main()