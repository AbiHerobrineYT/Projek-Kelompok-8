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

        if not nama_depan.replace(" ", "").isalpha():
            print("❌ Nama depan hanya boleh huruf alfabet (tanpa angka & simbol)!")
            continue
        
        break

    while True:
        nama_belakang = titik_koma("Nama Belakang")
        if not nama_belakang:
            print("❌ Nama belakang tidak boleh kosong!")
            continue

        if not nama_belakang.replace(" ", "").isalpha():
            print("❌ Nama belakang hanya boleh huruf alfabet (tanpa angka & simbol)!")
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

        if " " in email:
            print("❌ Email tidak boleh mengandung spasi!")
            continue

        if "@" not in email or "." not in email:
            print("❌ Email tidak valid! Harus mengandung '@' dan '.'")
            continue

        if email in df["email"].values:
            print("❌ Email sudah terdaftar!")
            continue

        if email.startswith("@") or email.endswith("@"):
            print("❌ Email tidak boleh diawali atau diakhiri '@'!")
            continue

        if email.startswith(".") or email.endswith("."):
            print("❌ Email tidak boleh diawali atau diakhiri '.'!")
            continue

        break

    while True:
        no_telp = titik_koma("Nomor Telepon")

        if not no_telp.isdigit():
            print("❌ Nomor telepon hanya boleh angka!")
            continue

        if not no_telp.startswith("0"):
            print("❌ Nomor telepon harus diawali dengan 0 (format Indonesia)!")
            continue

        if len(no_telp) < 10 or len(no_telp) > 13:
            print("❌ Nomor telepon harus 10–13 digit!")
            continue

        break

    while True:
        tanggal_lahir = titik_koma("Tanggal Lahir (DD/MM/YYYY)")
        try:
            tgl_lahir = datetime.strptime(tanggal_lahir, "%d/%m/%Y")
            hari_ini = datetime.today()
            umur = hari_ini.year - tgl_lahir.year

            if tgl_lahir > hari_ini:
                print("❌ Tanggal lahir tidak boleh di masa depan!")
                continue

            if (hari_ini.month, hari_ini.day) < (tgl_lahir.month, tgl_lahir.day):
                umur -= 1

            if umur < 13:
                print("❌ Pendaftaran gagal! Umur minimal 13 tahun.")
                continue

            if umur > 100:
                print("❌ Umur tidak valid! Periksa kembali tanggal lahir.")
                continue

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
