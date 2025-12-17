import pandas as pd
import os

user_file = "users.txt"


def init_user_file():
    if not os.path.exists(user_file):
        df = pd.DataFrame(columns=["username", "password"])
        df.to_csv(user_file, index=False)


def register():
    init_user_file()

    # Paksa string
    df = pd.read_csv(user_file, dtype=str)

    print("\n📝 REGISTRASI AKUN")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    # Bersihkan data lama
    df["username"] = df["username"].str.strip()

    if username in df["username"].values:
        print("❌ Username sudah terdaftar!")
        return False

    new_user = pd.DataFrame(
        [[username, password]],
        columns=["username", "password"]
    )

    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(user_file, index=False)

    print("✅ Registrasi berhasil! Silakan login.")
    return True


def login():
    init_user_file()

    # Paksa string
    df = pd.read_csv(user_file, dtype=str)

    print("\n🔐 LOGIN AKUN")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    # Bersihkan spasi di CSV
    df["username"] = df["username"].str.strip()
    df["password"] = df["password"].str.strip()

    user_valid = df[
        (df["username"] == username) &
        (df["password"] == password)
    ]

    if not user_valid.empty:
        print(f"\n✅ Login berhasil! Selamat datang, {username}")
        return True
    else:
        print("❌ Username atau password salah!")
        return False


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
