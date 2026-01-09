import pandas as pd
import os
from datetime import datetime

user_file = "users.csv"

variable_login = [
    "Nama Depan",
    "Nama Belakang",
    "Username",
    "Email",
    "Nomor Telepon",
    "Tanggal Lahir (DD/MM/YYYY)",
    "Password",
    "Konfirmasi Password"
]

max_var_len = max(len(l) for l in variable_login)


def titik_koma(varb):
    spasi = " " * (max_var_len - len(varb))
    return input(f"{varb}{spasi}: ").strip()


def init_user_file():
    if not os.path.exists(user_file):
        df = pd.DataFrame(columns=[
            "username",
            "password",
            "nama_depan",
            "nama_belakang",
            "email",
            "no_telp",
            "tanggal_lahir"
        ])
        df.to_csv(user_file, index=False)


def register():
    init_user_file()
    df = pd.read_csv(user_file, dtype=str)
    df["username"] = df["username"].str.strip()
    df["email"] = df["email"].str.strip()

    print("\n📝 REGISTRASI AKUN")

    while True:
        nama_depan = titik_koma("Nama Depan")
        if not nama_depan:
            print("❌ Nama depan tidak boleh kosong!")
            continue

        if any(char.isdigit() for char in nama_depan):
            print("❌ Nama depan tidak boleh mengandung angka!")
            continue
        
        break

    while True:
        nama_belakang = titik_koma("Nama Belakang")
        if not nama_belakang:
            print("❌ Nama belakang tidak boleh kosong!")
            continue

        if any(char.isdigit() for char in nama_belakang):
            print("❌ Nama belakang tidak boleh mengandung angka!")
            continue

        break

    while True:
        username = titik_koma("Username")

        if not username or " " in username:
            print("❌ Username tidak boleh kosong atau mengandung spasi!")
            continue

        if username in df["username"].values:
            print("❌ Username sudah digunakan!")
            continue

        break

    while True:
        email = titik_koma("Email")

        if "@" not in email or "." not in email:
            print("❌ Email tidak valid! Harus mengandung '@' dan '.'")
            continue

        if email in df["email"].values:
            print("❌ Email sudah terdaftar!")
            continue

        break

    while True:
        no_telp = titik_koma("Nomor Telepon")

        if not no_telp.isdigit() or len(no_telp) < 10:
            print("❌ Nomor telepon harus angka dan minimal 10 digit!")
            continue

        break

    while True:
        tanggal_lahir = titik_koma("Tanggal Lahir (DD/MM/YYYY)")
        try:
            import datetime
            datetime.datetime.strptime(tanggal_lahir, "%d/%m/%Y")
            break
        except ValueError:
            print("❌ Format tanggal salah! Gunakan DD/MM/YYYY")

    while True:
        password = titik_koma("Password")
        if len(password) < 6:
            print("❌ Password minimal 6 karakter!")
            continue
        break

    while True:
        konfirmasi = titik_koma("Konfirmasi Password")
        if konfirmasi != password:
            print("❌ Password tidak cocok!")
            continue
        break


    df.loc[len(df)] = [
        username,
        password,
        nama_depan,
        nama_belakang,
        email,
        no_telp,
        tanggal_lahir
    ]

    df.to_csv(user_file, index=False)

    print("✅ Registrasi berhasil! Silakan login.")
    return True

def login():
    init_user_file()
    df = pd.read_csv(user_file, dtype=str)

    print("\n🔐 LOGIN AKUN")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    df["username"] = df["username"].str.strip()
    df["password"] = df["password"].str.strip()

    user = df[
        (df["username"] == username) &
        (df["password"] == password)
    ]

    if not user.empty:
        print(f"\n✅ Selamat datang, {user.iloc[0]['nama_depan']}!")
        return user.iloc[0].to_dict()
    else:
        print("❌ Username atau password salah!")
        return None


def menu_auth():
    while True:
        print("\n=== RUANG TEDUH ===")
        print("1. Login")
        print("2. Register")
        print("3. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            data_user = login()
            if data_user:
                return data_user
        elif pilihan == "2":
            register()
        elif pilihan == "3":
            print("👋 Sampai jumpa!")
            return False
        else:
            print("❌ Pilihan tidak valid!")
