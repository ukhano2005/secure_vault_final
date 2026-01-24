
from tkinter import messagebox
from datetime import datetime
import string

class CredentialManager:
    def __init__(self, root, current_user, update_callback, encryption, dashboard_callback):
        self.root = root
        self.current_user = current_user
        self.update_callback = update_callback
        self.encryption = encryption
        self.dashboard_callback = dashboard_callback

        self.data = {"users": {}}

    # ---------------- Show Credentials ----------------
    def show_credentials(self):
        self.clear_window()

        # Back button (NO CONFIRM POPUP)
        tk.Button(
            self.root,
            text="← Back to Dashboard",
            font=("Arial", 12, "bold"),
            bg="#2563eb",
            fg="white",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.go_back
        ).pack(anchor="nw", padx=20, pady=10)

        header = tk.Frame(self.root, bg="#f0f2f5", pady=20, padx=30)
        header.pack(fill="x")

        tk.Label(
            header,
            text="Credential Management",
            font=("Arial", 24, "bold"),
            bg="#f0f2f5",
            fg="#1e293b"
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Add, update, or delete your stored credentials",
            font=("Arial", 12),
            bg="#f0f2f5",
            fg="#64748b"
        ).pack(anchor="w", pady=(5, 20))

        tk.Button(
            header,
            text="Add Credential",
            bg="#2563eb",
            fg="white",
            font=("Arial", 11),
            cursor="hand2",
            bd=0,
            padx=20,
            pady=8,
            command=self.add_credential_dialog
        ).pack(side="right")

        container = tk.Frame(self.root, bg="#f0f2f5")
        container.pack(fill="both", expand=True, padx=30, pady=10)

        canvas = tk.Canvas(container, bg="#f0f2f5", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        self.scrollable_frame = tk.Frame(canvas, bg="#f0f2f5")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for cred in self.data["users"].get(self.current_user, {}).get("credentials", []):
            self.create_credential_card(cred)

    # ---------------- Credential Card ----------------
    def create_credential_card(self, credential):
        card = tk.Frame(self.scrollable_frame, bg="white", padx=20, pady=15)
        card.pack(fill="x", pady=8)

        tk.Label(card, text="🔑", font=("Arial", 24), bg="#a855f7").pack(side="left", padx=15)

        info = tk.Frame(card, bg="white")
        info.pack(side="left", expand=True, fill="x")

        tk.Label(info, text=credential["service"], font=("Arial", 14, "bold"),
                 bg="white").pack(anchor="w")
        tk.Label(info, text=credential["username"], font=("Arial", 11),
                 bg="white", fg="#64748b").pack(anchor="w")

        tk.Label(card, text=credential["strength"], fg="white",
                 bg=self.strength_color(credential["strength"]),
                 padx=12, pady=4).pack(side="right", padx=10)

        tk.Button(card, text="👁", bd=0, font=("Arial", 14),
                  command=lambda c=credential: self.view_credential(c)).pack(side="right")

        tk.Button(card, text="Edit", bg="#dbeafe", fg="#2563eb", bd=0,
                  command=lambda c=credential: self.edit_credential(c)).pack(side="right", padx=5)

        tk.Button(card, text="Delete", bg="#fee2e2", fg="#dc2626", bd=0,
                  command=lambda c=credential: self.delete_credential(c)).pack(side="right", padx=5)

    # ---------------- Add ----------------
    def add_credential_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Credential")
        dialog.geometry("450x350")
        dialog.grab_set()

        entries = {}
        for label in ["Service", "Username", "Password"]:
            tk.Label(dialog, text=label).pack(pady=5)
            e = tk.Entry(dialog, show="●" if label == "Password" else "")
            e.pack(fill="x", padx=30)
            entries[label] = e

        def save():
            pwd = entries["Password"].get()
            cred = {
                "service": entries["Service"].get(),
                "username": entries["Username"].get(),
                "password": pwd,
                "strength": self.calculate_password_strength(pwd),
                "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            self.data["users"].setdefault(self.current_user, {"credentials": []})
            self.data["users"][self.current_user]["credentials"].append(cred)

            self.update_callback(self.data["users"][self.current_user]["credentials"])
            dialog.destroy()
            self.show_credentials()

        tk.Button(dialog, text="Save", bg="#2563eb", fg="white", command=save).pack(pady=20)

    # ---------------- View ----------------
    def view_credential(self, credential):
        messagebox.showinfo(
            "Credential",
            f"Service: {credential['service']}\n"
            f"Username: {credential['username']}\n"
            f"Password: {credential['password']}\n"
            f"Strength: {credential['strength']}"
        )

    # ---------------- Edit ----------------
    def edit_credential(self, credential):
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Credential")
        dialog.geometry("450x350")
        dialog.grab_set()

        fields = {}
        for key in ["service", "username", "password"]:
            tk.Label(dialog, text=key.capitalize()).pack()
            e = tk.Entry(dialog)
            e.insert(0, credential[key])
            e.pack(fill="x", padx=30)
            fields[key] = e

        def save():
            for k in fields:
                credential[k] = fields[k].get()
            credential["strength"] = self.calculate_password_strength(credential["password"])

            self.update_callback(self.data["users"][self.current_user]["credentials"])
            dialog.destroy()
            self.show_credentials()

        tk.Button(dialog, text="Save Changes", bg="#2563eb", fg="white",
                  command=save).pack(pady=20)

    # ---------------- Delete ----------------
    def delete_credential(self, credential):
        self.data["users"][self.current_user]["credentials"].remove(credential)
        self.update_callback(self.data["users"][self.current_user]["credentials"])
        self.show_credentials()

    # ---------------- Utils ----------------
    def calculate_password_strength(self, password):
        score = sum([
            len(password) >= 12,
            any(c.isupper() for c in password),
            any(c.islower() for c in password),
            any(c.isdigit() for c in password),
            any(c in string.punctuation for c in password)
        ])
        return "Strong" if score >= 4 else "Medium" if score == 3 else "Weak"

    def strength_color(self, strength):
        return {"Strong": "#4ade80", "Medium": "#fbbf24", "Weak": "#f87171"}[strength]

    def clear_window(self):
        for w in self.root.winfo_children():
            w.destroy()

    def go_back(self):
        self.update_callback(self.data["users"][self.current_user]["credentials"])
        self.dashboard_callback()
