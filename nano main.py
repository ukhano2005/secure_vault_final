#!/usr/bin/env python3
"""
SECURE PASSWORD MANAGER - MAIN FILE
Run this file to start the application
"""

import tkinter as tk
import json
import os
import bcrypt
from login import create_login_screen
from dashboard import Dashboard
from encryption import EncryptionManager
from credential_management import CredentialManager


class SecureVaultApp:
    def __init__(self):
        # ---------------- Main Window ----------------
        self.root = tk.Tk()
        self.root.title("Secure Vault - Password Manager")
        self.root.geometry("1300x800")
        self.root.configure(bg='#f8f9fa')

        # ---------------- Encryption ----------------
        self.encryption = EncryptionManager()

        # ---------------- Session Data ----------------
        self.current_user = None
        self.user_data = None
        self.failed_attempts = 0

        # ---------------- File Paths ----------------
        self.users_file = "users.json"
        self.vault_file = "vault.json"

        # ---------------- Credential Manager ----------------
        self.credential_manager = CredentialManager(
            root=self.root,
            current_user=None,
            update_callback=self.update_vault_data,
            encryption=self.encryption,
            dashboard_callback=self.show_dashboard   # ✅ FIX ADDED
        )

        # ---------------- Create Sample Data ----------------
        self.initialize_sample_data()

        # ---------------- Start Login ----------------
        self.show_login()

        # ---------------- Run App ----------------
        self.root.mainloop()

    # ---------------- Sample Users & Vault ----------------
    def initialize_sample_data(self):
        if not os.path.exists(self.users_file):
            users = {
                "john.doe": {
                    "name": "John Doe",
                    "password": bcrypt.hashpw("Password123!".encode(), bcrypt.gensalt()).decode(),
                    "email": "john.doe@gmail.com",
                    "created": "2024-01-15"
                },
                "alice.smith": {
                    "name": "Alice Smith",
                    "password": bcrypt.hashpw("SecurePass456@".encode(), bcrypt.gensalt()).decode(),
                    "email": "alice.smith@protonmail.com",
                    "created": "2024-02-20"
                },
                "bob.johnson": {
                    "name": "Bob Johnson",
                    "password": bcrypt.hashpw("VaultPass789#".encode(), bcrypt.gensalt()).decode(),
                    "email": "bob.j@outlook.com",
                    "created": "2024-03-10"
                }
            }
            with open(self.users_file, "w") as f:
                json.dump(users, f, indent=4)

        if not os.path.exists(self.vault_file):
            with open(self.vault_file, "w") as f:
                json.dump({}, f, indent=4)

    # ---------------- Login Screen ----------------
    def show_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # ✅ Corrected function call to match login.py requirements
        login_frame, update_attempts, _, _ = create_login_screen(
            self.root,
            self.handle_login,
            lambda: None  # Dummy callback for registration
        )
        self.update_attempts_func = update_attempts
        login_frame.pack(expand=True, fill='both')

    def handle_login(self, username, password):
        from tkinter import messagebox

        with open(self.users_file, "r") as f:
            users = json.load(f)

        if username in users:
            user_data = users[username]
            if bcrypt.checkpw(password.encode(), user_data["password"].encode()):
                self.current_user = username
                self.user_data = user_data
                self.failed_attempts = 0

                self.credential_manager.current_user = self.current_user
                self.show_dashboard()
                return
            else:
                self.failed_attempts += 1
        else:
            self.failed_attempts += 1

        self.update_attempts_func(self.failed_attempts)

        if self.failed_attempts >= 5:
            messagebox.showerror("Account Locked", "Too many failed attempts! Exiting.")
            self.root.quit()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")

    # ---------------- Dashboard ----------------
    def show_dashboard(self):
        with open(self.vault_file, "r") as f:
            vault_data = json.load(f)

        credentials = []
        if self.current_user in vault_data:
            for cred in vault_data[self.current_user]:
                credentials.append({
                    'service': self.encryption.decrypt(cred['service']),
                    'username': self.encryption.decrypt(cred['username']),
                    'password': self.encryption.decrypt(cred['password']),
                    'category': cred.get('category', 'General'),
                    'strength': cred.get('strength', 'Medium')
                })

        self.dashboard = Dashboard(
            self.root,
            self.current_user,
            self.user_data,
            credentials,
            self.handle_logout,
            self.update_vault_data,
            self.open_credentials_manager
        )

    def update_vault_data(self, updated_credentials):
        encrypted_creds = []
        for cred in updated_credentials:
            encrypted_creds.append({
                'service': self.encryption.encrypt(cred['service']),
                'username': self.encryption.encrypt(cred['username']),
                'password': self.encryption.encrypt(cred['password']),
                'category': cred.get('category', 'General'),
                'strength': cred['strength']
            })

        vault = {}
        if os.path.exists(self.vault_file):
            with open(self.vault_file, "r") as f:
                vault = json.load(f)

        vault[self.current_user] = encrypted_creds

        with open(self.vault_file, "w") as f:
            json.dump(vault, f, indent=4)

    def handle_logout(self):
        self.current_user = None
        self.user_data = None
        self.failed_attempts = 0
        self.show_login()

    # ---------------- Open Credential Manager ----------------
    def open_credentials_manager(self):
        self.credential_manager.current_user = self.current_user

        self.credential_manager.data["users"][self.current_user] = {"credentials": []}
        with open(self.vault_file, "r") as f:
            for cred in json.load(f).get(self.current_user, []):
                self.credential_manager.data["users"][self.current_user]["credentials"].append({
                    "service": self.encryption.decrypt(cred['service']),
                    "username": self.encryption.decrypt(cred['username']),
                    "password": self.encryption.decrypt(cred['password']),
                    "strength": cred.get('strength', 'Medium')
                })

        self.credential_manager.show_credentials()


print(">>> MAIN.PY EXECUTED <<<")
print(">>> STARTING APPLICATION <<<")
app = SecureVaultApp()
