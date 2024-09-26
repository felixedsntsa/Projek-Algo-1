import os
import csv
import sys
import pandas as pd
from pathlib import Path
import getpass
from datetime import datetime,date
from tabulate import tabulate

session = '' 

def addData(): 
    os.system('cls') 

    with open('buku.csv', 'a', newline='') as file: 
        csvTambah = csv.writer(file) 

        kategori = input("Masukkan kategori buku: ")
        judul = input("Masukkan judul buku: ")
        posisi = input("Masukkan posisi buku: ")
        stok = int(input("Masukkan stok buku: "))  

        csvTambah.writerow([kategori, judul, posisi, stok])  
        file.close() 
        os.system('cls') 

        print("Data berhasil ditambahkan!\n")
        input("\nEnter untuk lanjutkan")
        os.system('cls') 
        admin_menu() 

def getData():
    df = pd.read_csv('buku.csv') 
    df.index = range(1, len(df)+1,)
    print(tabulate(df, headers='keys', tablefmt='grid'))

def showData():
    os.system('cls')
    getData() 
    input("\n enter untuk lanjut")
    admin_menu()

def getPeminjam():
    df = pd.read_csv('request.csv') 
    df.index = range(1, len(df)+1,) 
    print(tabulate(df, headers='keys', tablefmt='grid'))

def showPeminjam():
    os.system('cls')
    getPeminjam() 
    input("\n enter untuk lanjut")
    admin_menu()

def editData():
    os.system('cls')
    getData() 
    df = pd.read_csv('buku.csv') 

    try:
        edit = int(input("Pilih nomor yang ingin diedit : ")) 
        kategoriBaru = input("Masukkan kategori buku baru : ") 
        judulBaru = input("Masukkan judul buku baru : ") 
        posisiBaru = input("Masukkan posisi buku baru : ") 
        stokBaru = int(input("Masukkan stok buku baru: ")) 

        df.at[edit-1, 'kategori'] = kategoriBaru
        df.at[edit-1, 'judul'] = judulBaru
        df.at[edit-1, 'posisi'] = posisiBaru
        df.at[edit-1, 'stok'] = stokBaru

        df.to_csv('buku.csv', index=False)
        print("Data berhasil diedit")
    except ValueError:
        print("Invalid input.") 
    
    input("\n enter untuk lanjut")
    admin_menu()

def delData():
    os.system('cls')
    getData()
    df = pd.read_csv('buku.csv')

    try:
        row_to_delete = int(input("Masukkan nomor yg ingin dihapus : ")) 
        if 1 <= row_to_delete <= len(df): 
            df = df.drop(row_to_delete - 1) 
            df.index = range(1, len(df) + 1) 
            df.to_csv('buku.csv', index=False) 
            print("Data berhasil dihapus.")
        else:
            print("Nomor tidak sesuai.")
    except ValueError:
        print("Invalid input.") 

    input("\n enter untuk lanjut.")
    admin_menu()

def searchCategory():
    os.system('cls')
    category_to_search = input("Masukkan kategori buku yang ingin dicari: ") 
    df = pd.read_csv('buku.csv') 
    filtered_df = df[df['kategori'] == category_to_search]  

    if not filtered_df.empty: 
        filtered_df.index = range(1, len(filtered_df) + 1)
        print(tabulate(filtered_df, headers='keys', tablefmt='grid')) 
        return filtered_df 
    else:
        print(f"Tidak ada buku dengan kategori '{category_to_search}'")  
        input("\nTekan enter untuk kembali ke menu visitor.") 
        visitor_menu()

def pinjamBuku(df, selected_index):
    if 1 <= selected_index <= len(df):
        selected_book = df.iloc[selected_index - 1] 
        global session 

        if selected_book['stok'] > 0: 
            with open('request.csv', 'a', newline='') as request_file: 
                request_writer = csv.writer(request_file) 
                request_writer.writerow([selected_book['kategori'], selected_book['judul'], selected_book['posisi'], session, '', '', ''])
            
            df_books = pd.read_csv('buku.csv') 
            book_index = (df_books['kategori'] == selected_book['kategori']) & (df_books['judul'] == selected_book['judul']) 

            if df_books.loc[book_index, 'stok'].values[0] > 0: 
                df_books.loc[book_index, 'stok'] -= 1 
                df_books.to_csv('buku.csv', index=False)
                print("Silahkan ke meja peminjaman untuk konfirmasi dengan admin.") 
            else:
                print("Maaf, stok buku sudah habis.")
        else:
            print("Maaf, stok buku sudah habis.")
    else:
        print("Nomor tidak sesuai.") 

    input("\nTekan enter untuk kembali ke menu visitor.") 
    visitor_menu()

def terimaRequest():
    os.system('cls')
    request_df = pd.read_csv('request.csv') 

    filtered_requests = request_df[(request_df['peminjam'].notnull()) & (request_df['tanggal peminjaman'].isnull())]

    if not filtered_requests.empty: 
        filtered_requests.index = range(1, len(filtered_requests) + 1) 
        print("Daftar Request Peminjaman Buku yang Menunggu Persetujuan:")
        print(filtered_requests)

        try:
            request_index = int(input("Pilih nomor request yang akan disetujui: ")) 
            if 1 <= request_index <= len(filtered_requests): 
                approved_request_index = filtered_requests.index[request_index - 1]
                request_df.loc[approved_request_index - 1, 'tanggal peminjaman'] = date.today().strftime("%Y-%m-%d") 
                request_df.to_csv('request.csv', index=False) 
                print("Request berhasil disetujui.")
            else:
                print("Nomor request tidak sesuai.")
        except ValueError:
            print("Invalid input.") 
    else:
        print("Tidak ada request yang dapat disetujui saat ini.")  

    input("\nTekan enter untuk kembali ke menu admin.")
    admin_menu()

def requestKembali():
    os.system('cls') 
    global session

    request_df = pd.read_csv('request.csv')
    user_requests = request_df[(request_df['peminjam'] == session) & (request_df['pengembali'].isnull()) & (request_df['tanggal peminjaman'].notnull())]
    
    if not user_requests.empty:
        user_requests_display = user_requests.reset_index(drop=True)
        user_requests_display.index += 1
        print("Data Peminjaman Buku:")
        print(user_requests_display)

        try:
            request_index = int(input("Pilih indeks buku yang ingin dikembalikan: "))
            if 1 <= request_index <= len(user_requests):
                approved_request_index = user_requests.index[request_index - 1]
                request_df.loc[approved_request_index, 'pengembali'] = session
                request_df.to_csv('request.csv', index=False)
                print("Silahkan konfirmasi pengembalian di admin.")
            else:
                print("Nomor indeks tidak sesuai.")
        except ValueError:
            print("Invalid input.")
    else:
        print("Anda tidak memiliki buku yang sedang dipinjam atau dalam proses pengembalian.")

    input("\nTekan enter untuk kembali ke menu visitor.")
    visitor_menu()


def terimaRequestKembali():
    os.system('cls')
    request_df = pd.read_csv('request.csv') 

    return_requests = request_df[(request_df['pengembali'].notnull()) & (request_df['tanggal pengembalian'].isnull())]

    if not return_requests.empty:
        return_requests_display = return_requests.reset_index(drop=True)
        return_requests_display.index += 1
        print("Daftar Request Pengembalian Buku:")
        print(return_requests_display)

        try:
            return_index = int(input("Pilih nomor request pengembalian yang akan disetujui: ")) 
            if 1 <= return_index <= len(return_requests): 
                approved_request_index = return_requests.index[return_index - 1]  

                due_date = pd.to_datetime(request_df.loc[approved_request_index, 'tanggal peminjaman']) + pd.Timedelta(days=7)
                today = date.today() + pd.Timedelta(days=15)
                today_datetime = datetime.combine(today, datetime.min.time()) 
                days_overdue = today_datetime - due_date
                late_days = days_overdue.days

                request_df.loc[approved_request_index, 'tanggal pengembalian'] = today_datetime.date()
                request_df.to_csv('request.csv', index=False) 
                
                if late_days > 0:
                    denda = late_days * 500
                    print(f"Peminjam terlambat mengembalikan selama {late_days} hari dan dikenakan denda sebesar Rp {denda}.")
                else :
                    print("Buku dikembalikan tepat waktu")

                buku_df = pd.read_csv('buku.csv') 
                book_index = (buku_df['kategori'] == request_df.loc[approved_request_index, 'kategori']) & (buku_df['judul'] == request_df.loc[approved_request_index, 'judul']) 
                if not buku_df[book_index].empty: 
                    buku_df.loc[book_index, 'stok'] += 1  
                    buku_df.to_csv('buku.csv', index=False) 

                print("Request pengembalian berhasil disetujui.")
            else:
                print("Nomor request pengembalian tidak sesuai.")
        except ValueError:
            print("Invalid input.") 
    else:
        print("Tidak ada request pengembalian yang dapat disetujui saat ini.") 

    input("\nTekan enter untuk kembali ke menu admin.") 
    admin_menu()

def admin_menu():
    os.system('cls')
    print("="*80)
    print("Menu Admin".center(80))
    print("="*80)

    while True:
        menu = input("[1. Tambah Data][2. Lihat Data][3. Edit Data][4. Hapus Data][5. Terima Request][6. Daftar Peminjam][7. Terima Kembali][8. Kembali ke menu utama]= ")

        if menu == "1":
            addData() # Memanggil fungsi addData() untuk menambahkan data buku baru
        elif menu == "2":
            showData() # Memanggil fungsi showData() untuk menampilkan data buku dalam buku.csv
        elif menu == "3":
            editData() # Memanggil fungsi editData() untuk mengedit data dalam buku.csv
        elif menu == "4":
            delData() # Memanggil fungsi delData() untuk menghapus indeks data dalam buku.csv
        elif menu == "5":
            terimaRequest() # Memanggil fungsi terimaRequest() untuk menerima request peminjaman buku dari visitor
        elif menu == "6":
            showPeminjam() # Memanggil fungsi showData1() untuk menampilkan data peminjam buku dalam request.csv
        elif menu == "7":
            terimaRequestKembali() # Memanggil fungsi terimaRequestKembali() untuk menangani request pengembalian
        elif menu == "8":
            admin() # Kembali ke menu admin
        else:
            input("\n Pilihan tidak sesuai, enter untuk kembali ke menu admin") 
        admin_menu()

def visitor_menu():
    os.system('cls')
    print("="*80)
    print("Menu Pengunjung".center(80))
    print("="*80)

    while True:
        menu = input("[1. Cari Buku][2. Kembalikan Buku][3. Kembali ke menu utama]= ")

        if menu == "1":
            df = searchCategory() # Memanggil fungsi searchCategory() untuk mencari buku berdasarkan kategori
            if df is not None:
                print("Apakah Anda ingin meminjam buku? : ") 
                response = input("[1. Ya][2. Tidak]= ")

                if response == "1":
                    selected_index = int(input("Pilih indeks buku yang ingin Anda pinjam: ")) 
                    pinjamBuku(df, selected_index) 
                elif response == "2":
                    visitor_menu() 
                else:
                    input("\n Pilihan tidak valid. enter untuk kembali ke menu pengunjung")
                visitor_menu()
        elif menu == "2":
            requestKembali() # Memanggil fungsi requestKembali() untuk memproses pengembalian buku
        elif menu == "3":
            pengunjung() # Kembali ke menu admin
        else:
            input("\n Pilihan tidak sesuai, enter untuk kembali ke menu") 
        visitor_menu() 

def create_csv_if_not_exists(file_path, header):
    if not Path(file_path).is_file(): 
        with open(file_path, 'w', newline='') as filecsv: 
            csv_writer = csv.DictWriter(filecsv, fieldnames=header, delimiter=',')
            csv_writer.writeheader()

def awal():
    os.system('cls')

    create_csv_if_not_exists('buku.csv', ['kategori', 'judul', 'posisi', 'stok'])
    create_csv_if_not_exists('admin.csv', ['username', 'password'])
    create_csv_if_not_exists('visitor.csv', ['username', 'password'])
    create_csv_if_not_exists('request.csv', ['kategori', 'judul', 'posisi', 'peminjam', 'tanggal peminjaman', 'pengembali', 'tanggal pengembalian'])

    print("="*80)
    print("Welcome To".center(80))
    print_pola()
    print("="*80)
    
    user_type = input("[1. Menu Admin][2. Menu Pengunjung][3. Keluar]= ")
    
    if user_type == "1":
        admin() 
    elif user_type == "2":
        pengunjung() 
    elif user_type == "3":
        keluar()
    else:
        input("Masukkan pilihan yang ada\nUntuk melanjutkan, tekan enter") 
        awal()

def keluar():
    os.system('cls')

    print("="*80)
    print("Terimakasih telah menggunakan BookTrack".center(80))
    print("="*80)

    sys.exit()

def admin():
    os.system('cls')

    print("="*80)
    print("Menu Admin".center(80))
    print("="*80)

    user_type = input("[1. Registrasi][2. Login][3. Kembali ke halaman awal]= ")

    if user_type == "1":
        daftar_admin()
    elif user_type == "2":
        masuk_admin()
    elif user_type == "3":
        awal()
    else:
        input("Masukkan pilihan yang ada\nUntuk melanjutkan, tekan enter") 
        admin()

def pengunjung():
    os.system('cls')

    print("="*80)
    print("Menu Pengunjung".center(80))
    print("="*80)
    
    user_type = input("[1. Registrasi][2. Login][3. Kembali ke halaman awal]= ")

    if user_type == "1":
        daftar_visitor()
    elif user_type == "2":
        masuk_visitor()
    elif user_type == "3":
        awal()
    else:
        input("Masukkan pilihan yang ada\nUntuk melanjutkan, tekan enter") 
        pengunjung()

def validasi_admin(username, password):
    with open("admin.csv", "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["username"] == username and row["password"] == password:
                return True
    return False 

def cek_user_admin(username):
    with open("admin.csv", "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["username"] == username:
                print("Akun Sudah Tersedia. Silahkan coba lagi") 
                input("Untuk melanjutkan, tekan enter")
                admin() 

def daftar_admin():
    os.system('cls')
    username = input("Masukkan nama: ") 

    if cek_user_admin(username):
        print("Username sudah ada, silahkan coba lagi")
    password = input("Masukkan Password: ")

    with open("admin.csv", "a") as file:
        file.write(f"{username},{password}\n")
    input("Data telah ditambahkan\nUntuk melanjutkan, tekan enter") 
    admin() 

def masuk_admin():
    while True:
        os.system('cls')

        global session

        username = input("Masukkan nama: ") 
        password = getpass.getpass("Masukkan password: ") 

        if validasi_admin(username, password):

            session = username
            os.system("cls")
            admin_menu()
            break
        else:
            input("Masukkan data yang benar!\nTekan enter untuk melanjutkan.") 
        admin() 

def validasi_visitor(username, password):
    with open("visitor.csv", "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["username"] == username and row["password"] == password:
                return True
    return False 

def cek_user_visitor(username):
    with open("visitor.csv", "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["username"] == username:
                print("Akun Sudah Tersedia. Silahkan coba lagi") 
                input("Untuk melanjutkan, tekan enter")
                pengunjung() 

def daftar_visitor():
    os.system('cls')
    username = input("Masukkan nama: ") 

    if cek_user_visitor(username):
        print("Username sudah ada, silahkan coba lagi")
    password = input("Masukkan Password: ")

    with open("visitor.csv", "a") as file:
        file.write(f"{username},{password}\n")
    input("Data telah ditambahkan\nUntuk melanjutkan, tekan enter") 
    pengunjung() 

def masuk_visitor():
    while True:
        os.system('cls')

        global session

        username = input("Masukkan nama: ") 
        password = getpass.getpass("Masukkan password: ") 

        if validasi_visitor(username, password):

            session = username
            os.system("cls")
            visitor_menu()
            break
        else:
            input("Masukkan data yang benar!\nTekan enter untuk melanjutkan.") 
        pengunjung() 

def print_pola():
    pattern = """
    
BBBBB     OOOO     OOOO    K   K   TTTTTTTT   RRRRR      AAAAA     CCCCC   K   K
B    B   O    O   O    O   K  K       TT      R    R    A     A   C        K  K
B    B   O    O   O    O   K K        TT      R    R    A     A   C        K K
BBBBB    O    O   O    O   KK         TT      RRRRR     AAAAAAA   C        KK
B    B   O    O   O    O   K K        TT      R   R     A     A   C        K K
B    B   O    O   O    O   K  K       TT      R    R    A     A   C        K  K
BBBBB     OOOO     OOOO    K   K      TT      R     R   A     A    CCCCC   K   K
    """
    print(pattern)

if __name__ == "__main__":
    awal() 