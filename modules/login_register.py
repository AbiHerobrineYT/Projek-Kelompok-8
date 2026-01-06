import pandas as pd
import os

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

    print("\n📝 REGISTRASI AKUN")

    nama_depan = titik_koma("Nama Depan")
    nama_belakang = titik_koma("Nama Belakang")
    username = titik_koma("Username")
    email = titik_koma("Email")
    no_telp = titik_koma("Nomor Telepon")
    tanggal_lahir = titik_koma("Tanggal Lahir (DD/MM/YYYY)")
    password = titik_koma("Password")
    konfirmasi = titik_koma("Konfirmasi Password")

    # Validasi dasar
    if password != konfirmasi:
        print("❌ Password dan konfirmasi tidak cocok!")
        return False

    df["username"] = df["username"].str.strip()
    df["email"] = df["email"].str.strip()

    if username in df["username"].values:
        print("❌ Username sudah digunakan!")
        return False

    if email in df["email"].values:
        print("❌ Email sudah terdaftar!")
        return False

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
            if login():
                return True
        elif pilihan == "2":
            register()
        elif pilihan == "3":
            print("👋 Sampai jumpa!")
            return False
        else:
            print("❌ Pilihan tidak valid!")
