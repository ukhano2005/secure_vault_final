# login.py - LOGIN SCREEN WITH LIGHT BLUE LOCKc
import tkinter as tk

def create_login_screen(parent, on_login_callback):
    """
    Creates login screen with light blue lock
    Returns: (frame, update_attempts_func, username_entry, password_entry)
    """
    
    # ================= COLORS =================
    BG_MAIN        = "#F4F6F8"
    BG_CARD        = "#FFFFFF"
    TEXT_PRIMARY   = "#1F2937"
    TEXT_SECONDARY = "#6B7280"
    INPUT_BORDER   = "#CBD5E1"
    BTN_PRIMARY    = "#1A73E8"
    BTN_ACTIVE     = "#1558B0"
    ERROR_RED      = "#D93025"
    LOCK_BLUE      = "#4DABF7"  # LIGHT BLUE COLOR FOR LOCK
    
    # ================= MAIN FRAME =================
    frame = tk.Frame(parent, bg=BG_MAIN)
    frame.pack(fill='both', expand=True)
    
    # ================= CENTER CARD =================
    center = tk.Frame(frame, bg=BG_CARD, padx=40, pady=25)
    center.place(relx=0.5, rely=0.5, anchor='center')
    
    # ================= LOCK ICON =================
    lock_frame = tk.Frame(center, bg=BG_CARD)
    lock_frame.pack(pady=(0, 10))
    
    # LIGHT BLUE LOCK ICON
    lock_icon = tk.Label(
        lock_frame,
        text="🔒",
        font=('Segoe UI', 42),  # Slightly larger
        fg=LOCK_BLUE,  # LIGHT BLUE COLOR
        bg=BG_CARD
    )
    lock_icon.pack()
    
    # ================= TITLE =================
    tk.Label(
        center,
        text="Secure Vault",
        font=('Segoe UI', 28, 'bold'),
        fg=TEXT_PRIMARY,
        bg=BG_CARD
    ).pack(pady=(0, 5))
    
    tk.Label(
        center,
        text="Password Manager",
        font=('Segoe UI', 13),
        fg=TEXT_SECONDARY,
        bg=BG_CARD
    ).pack(pady=(0, 25))
    
    # ================= FORM =================
    form = tk.Frame(center, bg=BG_CARD)
    form.pack()
    
    # Username
    tk.Label(
        form,
        text="Username / Email",
        font=('Segoe UI', 11, 'bold'),
        fg=TEXT_PRIMARY,
        bg=BG_CARD
    ).grid(row=0, column=0, sticky='w', pady=(0, 5))
    
    username_entry = tk.Entry(
        form,
        font=('Segoe UI', 11),
        width=38,
        bg="white",
        fg=TEXT_PRIMARY,
        insertbackground=TEXT_PRIMARY,
        relief='solid',
        bd=1,
        highlightthickness=1,
        highlightbackground=INPUT_BORDER
    )
    username_entry.grid(row=1, column=0, pady=(0, 18))
    username_entry.insert(0, "Enter your username")
    
    # Password
    tk.Label(
        form,
        text="Master Password",
        font=('Segoe UI', 11, 'bold'),
        fg=TEXT_PRIMARY,
        bg=BG_CARD
    ).grid(row=2, column=0, sticky='w', pady=(0, 5))
    
    password_frame = tk.Frame(form, bg=BG_CARD)
    password_frame.grid(row=3, column=0, pady=(0, 10), sticky='ew')
    
    password_entry = tk.Entry(
        password_frame,
        font=('Segoe UI', 11),
        width=32,
        bg="white",
        fg=TEXT_PRIMARY,
        show="•",
        insertbackground=TEXT_PRIMARY,
        relief='solid',
        bd=1,
        highlightthickness=1,
        highlightbackground=INPUT_BORDER
    )
    password_entry.pack(side='left')
    
    # Show / Hide button
    def toggle_password_visibility():
        if password_entry.cget('show') == "•":
            password_entry.config(show="")
            eye_button.config(text="👁")
        else:
            password_entry.config(show="•")
            eye_button.config(text="👁🗨")
    
    eye_button = tk.Button(
        password_frame,
        text="👁🗨",
        font=('Segoe UI', 11),
        bg="#E5E7EB",
        fg=TEXT_PRIMARY,
        relief='flat',
        width=3,
        command=toggle_password_visibility
    )
    eye_button.pack(side='right', padx=(6, 0))
    
    # Failed attempts
    attempts_var = tk.StringVar(value="Failed attempts: 0/5")
    attempts_label = tk.Label(
        form,
        textvariable=attempts_var,
        font=('Segoe UI', 10),
        fg=ERROR_RED,
        bg=BG_CARD
    )
    attempts_label.grid(row=4, column=0, sticky='w', pady=(0, 20))
    
    # ================= LOGIN BUTTON =================
    def login_click():
        username = username_entry.get()
        password = password_entry.get()
        
        if username == "Enter your username":
            username = ""
        if password == "Enter master password":
            password = ""
        
        on_login_callback(username, password)
    
    login_btn = tk.Button(
        form,
        text="Login",
        font=('Segoe UI', 12, 'bold'),
        bg=BTN_PRIMARY,
        fg="white",
        activebackground=BTN_ACTIVE,
        relief='flat',
        width=16,
        command=login_click
    )
    login_btn.grid(row=5, column=0, pady=10)
    
    # Lock warning
    tk.Label(
        form,
        text="Account locked after 5 failed attempts",
        font=('Segoe UI', 9),
        fg=ERROR_RED,
        bg=BG_CARD
    ).grid(row=6, column=0, pady=(8, 0))
    
    # ================= PLACEHOLDERS =================
    def clear_placeholder(entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            if placeholder == "Enter master password":
                entry.config(show="•")
    
    def add_placeholder(entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            if placeholder == "Enter master password":
                entry.config(show="")
    
    username_entry.bind("<FocusIn>", lambda e: clear_placeholder(username_entry, "Enter your username"))
    username_entry.bind("<FocusOut>", lambda e: add_placeholder(username_entry, "Enter your username"))
    
    password_entry.bind("<FocusIn>", lambda e: clear_placeholder(password_entry, "Enter master password"))
    password_entry.bind("<FocusOut>", lambda e: add_placeholder(password_entry, "Enter master password"))
    
    # ================= UPDATE ATTEMPTS =================
    def update_attempts(count, max_attempts=5):
        attempts_var.set(f"Failed attempts: {count}/{max_attempts}")
        if count >= 3:
            attempts_label.config(font=('Segoe UI', 10, 'bold'))
    
    # Enter key login
    username_entry.bind("<Return>", lambda e: login_click())
    password_entry.bind("<Return>", lambda e: login_click())
    
    return frame, update_attempts, username_entry, password_entry
