# dashboard.py - ENHANCED WITH PANELS AND BETTER DESIGN
import tkinter as tk
from tkinter import ttk

class Dashboard:
    def __init__(self, parent, username, user_data, credentials, on_logout_callback, on_update_stats=None, open_credentials_callback=None):
        self.parent = parent
        self.username = username
        self.user_data = user_data
        self.credentials = credentials
        self.filtered_credentials = credentials.copy()  # Store filtered credentials
        self.on_logout = on_logout_callback
        self.on_update_stats = on_update_stats
        self.open_credentials_callback = open_credentials_callback  # NEW: Callback for CredentialManager
        
        # Increase main window width to fit everything
        self.parent.geometry("1300x800")  # INCREASED FROM 1200 TO 1300
        
        self.create_dashboard()
    
    def create_dashboard(self):
        """Create complete dashboard with panels"""
        # Clear previous content
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Main frame with gradient-like background
        self.frame = tk.Frame(self.parent, bg='#f0f4f8')
        self.frame.pack(fill='both', expand=True)
        
        # ========== HEADER WITH LOGOUT ==========
        header = tk.Frame(self.frame, bg='#ffffff', height=70, relief='flat', highlightthickness=0)
        header.pack(fill='x', pady=(0, 2))
        
        # Left: Title with icon
        title_frame = tk.Frame(header, bg='#ffffff')
        title_frame.place(x=40, y=15)
        
        # Light Blue Lock Icon
        lock_icon = tk.Label(title_frame, text="🔒",
                           font=('Arial', 24),
                           fg='#4dabf7',
                           bg='#ffffff')
        lock_icon.pack(side='left', padx=(0, 10))
        
        # Title
        title_text = tk.Label(title_frame, text="Secure Vault",
                            font=('Arial', 22, 'bold'),
                            fg='#2c3e50',
                            bg='#ffffff')
        title_text.pack(side='left')
        
        subtitle = tk.Label(title_frame, text="Password Manager Dashboard",
                          font=('Arial', 10),
                          fg='#7f8c8d',
                          bg='#ffffff')
        subtitle.pack(side='left', padx=(10, 0))
        
        # Right: User info and logout
        user_frame = tk.Frame(header, bg='#ffffff')
        user_frame.place(relx=1.0, x=-40, y=15, anchor='ne')
        
        # User greeting
        user_greet = tk.Label(user_frame, text=f"Hi, {self.user_data['name'].split()[0]}",
                            font=('Arial', 11, 'bold'),
                            fg='#2c3e50',
                            bg='#ffffff')
        user_greet.pack(side='left', padx=(0, 15))
        
        # Logout button with modern style
        logout_btn = tk.Button(user_frame, text="🚪 Logout",
                             font=('Arial', 10, 'bold'),
                             bg='#e74c3c',
                             fg='white',
                             activebackground='#c0392b',
                             relief='flat',
                             padx=20,
                             pady=6,
                             cursor='hand2',
                             command=self.on_logout)
        logout_btn.pack(side='left')
        
        # ========== MAIN CONTENT AREA ==========
        main_content = tk.Frame(self.frame, bg='#f0f4f8')
        main_content.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Left Column (Stats + Management)
        left_column = tk.Frame(main_content, bg='#f0f4f8')
        left_column.pack(side='left', fill='both', expand=True)
        
        # Right Column (Credentials) - INCREASED WIDTH
        right_column = tk.Frame(main_content, bg='#f0f4f8')
        right_column.pack(side='right', fill='both', expand=True, padx=(40, 0))  # Increased padding
        
        # ========== WELCOME PANEL ==========
        welcome_panel = self.create_panel(left_column, "Welcome Panel", padding=20)
        welcome_panel.pack(fill='x', pady=(0, 20))
        
        # Welcome content
        welcome_content = tk.Frame(welcome_panel, bg='white')
        welcome_content.pack(fill='both', expand=True)
        
        # Welcome icon and text
        welcome_icon = tk.Label(welcome_content, text="👋",
                              font=('Arial', 28),
                              fg='#3498db',
                              bg='white')
        welcome_icon.pack(side='left', padx=(0, 15))
        
        welcome_text_frame = tk.Frame(welcome_content, bg='white')
        welcome_text_frame.pack(side='left', fill='both', expand=True)
        
        welcome_title = tk.Label(welcome_text_frame,
                               text=f"Welcome back, {self.user_data['name']}!",
                               font=('Arial', 16, 'bold'),
                               fg='#2c3e50',
                               bg='white',
                               anchor='w')
        welcome_title.pack(fill='x')
        
        welcome_subtitle = tk.Label(welcome_text_frame,
                                  text=f"Your vault is secure and protected. You have {len(self.credentials)} stored credentials.",
                                  font=('Arial', 12),
                                  fg='#7f8c8d',
                                  bg='white',
                                  anchor='w',
                                  wraplength=400)
        welcome_subtitle.pack(fill='x', pady=(5, 0))
        
        # ========== STATS PANEL ==========
        stats_panel = self.create_panel(left_column, "Security Overview", padding=20)
        stats_panel.pack(fill='x', pady=(0, 20))
        
        self.update_stats_display(stats_panel)
        
        # ========== MANAGEMENT PANEL ==========
        mgmt_panel = self.create_panel(left_column, "Vault Management", padding=20)
        mgmt_panel.pack(fill='both', expand=True)
        
        # Management buttons grid
        mgmt_grid = tk.Frame(mgmt_panel, bg='white')
        mgmt_grid.pack(fill='both', expand=True, pady=(10, 0))
        
        # Button 1: Credential Management - NOW WORKABLE
        cred_card = self.create_management_card(mgmt_grid, "🔐", "Credential Management",
                                              "Add, update, or delete credentials",
                                              self.show_credential_management)
        cred_card.grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky='nsew')
        
        # Button 2: Security Utilities - NOW WORKABLE
        sec_card = self.create_management_card(mgmt_grid, "🛡", "Security Utilities",
                                             "Password tools and auto-lock",
                                             self.show_security_utilities)
        sec_card.grid(row=0, column=1, padx=(0, 10), pady=(0, 10), sticky='nsew')
        
        # Button 3: Audit and Logs - NOW WORKABLE
        audit_card = self.create_management_card(mgmt_grid, "📊", "Audit and Logs",
                                               "View login activity and alerts",
                                               self.show_audit_logs)
        audit_card.grid(row=0, column=2, pady=(0, 10), sticky='nsew')
        
        mgmt_grid.grid_columnconfigure(0, weight=1)
        mgmt_grid.grid_columnconfigure(1, weight=1)
        mgmt_grid.grid_columnconfigure(2, weight=1)
        
        # ========== CREDENTIALS PANEL ==========
        # Create the panel using the same create_panel function
        cred_panel = tk.Frame(right_column, bg='white', relief='flat', highlightthickness=0)
        cred_panel.pack(fill='both', expand=True)
        
        # Add subtle shadow (like other panels)
        shadow = tk.Frame(cred_panel, bg='#e0e6ed', height=2)
        shadow.pack(fill='x', side='bottom')
        
        # Panel content with padding
        panel_content = tk.Frame(cred_panel, bg='white', padx=20, pady=20)
        panel_content.pack(fill='both', expand=True)
        
        # Panel title (FIXED: Added this line)
        title_label = tk.Label(panel_content,
                             text="Saved Credentials",
                             font=('Arial', 14, 'bold'),
                             fg='#2c3e50',
                             bg='white',
                             anchor='w')
        title_label.pack(fill='x', pady=(0, 15))
        
        # Panel header with stats
        cred_header = tk.Frame(panel_content, bg='white')
        cred_header.pack(fill='x', pady=(0, 15))
        
        # Stats in header
        total = len(self.filtered_credentials)
        strong = sum(1 for c in self.filtered_credentials if c.get('strength') == 'Strong')
        
        self.stats_label = tk.Label(cred_header,
                             text=f"📊 {total} items • ✅ {strong} strong • ⚠️ {total-strong} weak",
                             font=('Arial', 10),
                             fg='#7f8c8d',
                             bg='white')
        self.stats_label.pack(side='left')
        
        # Search bar (working)
        search_frame = tk.Frame(cred_header, bg='white')
        search_frame.pack(side='right')
        
        search_icon = tk.Label(search_frame, text="🔍",
                             font=('Arial', 10),
                             fg='#95a5a6',
                             bg='white')
        search_icon.pack(side='left', padx=(0, 5))
        
        self.search_entry = tk.Entry(search_frame,
                              font=('Arial', 10),
                              width=20,
                              bg='#f8f9fa',
                              fg='#2c3e50',
                              relief='flat',
                              highlightthickness=1,
                              highlightcolor='#3498db',
                              highlightbackground='#ecf0f1')
        self.search_entry.insert(0, "Search credentials...")
        self.search_entry.pack(side='left')
        
        # Add search functionality
        self.search_entry.bind('<KeyRelease>', self.perform_search)
        
        # Add clear button
        clear_btn = tk.Button(search_frame, text="✕",
                            font=('Arial', 9),
                            bg='#e2e8f0',
                            fg='#4a5568',
                            relief='flat',
                            width=2,
                            cursor='hand2',
                            command=self.clear_search)
        clear_btn.pack(side='left', padx=(5, 0))
        
        # Create table container
        self.table_container = tk.Frame(panel_content, bg='white')
        self.table_container.pack(fill='both', expand=True)
        
        # Display credentials in a nice table
        self.display_credentials_table()
    
    def create_panel(self, parent, title, padding=20):
        """Create a styled panel with shadow effect"""
        panel = tk.Frame(parent, bg='white', relief='flat', highlightthickness=0)
        
        # Add subtle shadow
        shadow = tk.Frame(panel, bg='#e0e6ed', height=2)
        shadow.pack(fill='x', side='bottom')
        
        # Panel content
        content = tk.Frame(panel, bg='white')
        content.pack(fill='both', expand=True, padx=padding, pady=padding)
        
        # Panel title
        if title:
            title_label = tk.Label(content,
                                 text=title,
                                 font=('Arial', 14, 'bold'),
                                 fg='#2c3e50',
                                 bg='white',
                                 anchor='w')
            title_label.pack(fill='x', pady=(0, 10))
        
        return panel
    
    def create_management_card(self, parent, icon, title, description, command):
        """Create a management card/button"""
        card = tk.Frame(parent, bg='#f8fafc', relief='flat',
                       highlightthickness=1, highlightbackground='#e2e8f0',
                       cursor='hand2')
        card.bind('<Enter>', lambda e: card.config(bg='#edf2f7'))
        card.bind('<Leave>', lambda e: card.config(bg='#f8fafc'))
        
        # Card content
        content = tk.Frame(card, bg='#f8fafc', padx=20, pady=25)
        content.pack(fill='both', expand=True)
        
        # Make entire content area clickable
        content.bind('<Button-1>', lambda e: command())
        for widget in content.winfo_children():
            widget.bind('<Button-1>', lambda e: command())
        
        # Icon
        icon_label = tk.Label(content, text=icon,
                            font=('Arial', 28),
                            fg='#4dabf7',
                            bg='#f8fafc',
                            cursor='hand2')
        icon_label.pack(pady=(0, 10))
        icon_label.bind('<Button-1>', lambda e: command())
        
        # Title
        title_label = tk.Label(content, text=title,
                             font=('Arial', 12, 'bold'),
                             fg='#2c3e50',
                             bg='#f8fafc',
                             cursor='hand2')
        title_label.pack()
        title_label.bind('<Button-1>', lambda e: command())
        
        # Description
        desc_label = tk.Label(content, text=description,
                            font=('Arial', 10),
                            fg='#718096',
                            bg='#f8fafc',
                            wraplength=150,
                            justify='center',
                            cursor='hand2')
        desc_label.pack(pady=(5, 0))
        desc_label.bind('<Button-1>', lambda e: command())
        
        # Hover indicator
        hover_indicator = tk.Frame(card, height=2, bg='#4dabf7')
        hover_indicator.pack(fill='x', side='bottom')
        
        # Add click handler to entire card
        card.bind('<Button-1>', lambda e: command())
        
        return card
    
    def update_stats_display(self, parent):
        """Update and display stats in panel"""
        # Calculate stats
        total = len(self.filtered_credentials)
        strong = sum(1 for c in self.filtered_credentials if c.get('strength') == 'Strong')
        weak = total - strong
        
        # Stats container
        stats_container = tk.Frame(parent, bg='white')
        stats_container.pack(fill='x')
        
        stats = [
            {"title": "Total Passwords", "value": str(total), "color": "#4dabf7", "icon": "🔢"},
            {"title": "Strong Passwords", "value": str(strong), "color": "#28a745", "icon": "✅"},
            {"title": "Weak Passwords", "value": str(weak), "color": "#dc3545", "icon": "⚠️"},
        ]
        
        for i, stat in enumerate(stats):
            # Stat card
            stat_card = tk.Frame(stats_container, bg='#f8fafc', relief='flat',
                               highlightthickness=1, highlightbackground='#e2e8f0')
            stat_card.pack(side='left', fill='both', expand=True, padx=(0, 10) if i < 2 else 0)
            
            # Stat content
            stat_content = tk.Frame(stat_card, bg='#f8fafc', padx=15, pady=20)
            stat_content.pack(fill='both', expand=True)
            
            # Icon and value
            top_frame = tk.Frame(stat_content, bg='#f8fafc')
            top_frame.pack()
            
            # Icon
            icon_label = tk.Label(top_frame, text=stat["icon"],
                                font=('Arial', 14),
                                fg=stat["color"],
                                bg='#f8fafc')
            icon_label.pack(side='left', padx=(0, 10))
            
            # Value - MADE BIGGER
            value_label = tk.Label(top_frame, text=stat["value"],
                                 font=('Arial', 28, 'bold'),  # Increased size
                                 fg=stat["color"],
                                 bg='#f8fafc')
            value_label.pack(side='left')
            
            # Title - MADE FULLY VISIBLE
            title_label = tk.Label(stat_content, text=stat["title"],
                                 font=('Arial', 12, 'bold'),  # Made bold
                                 fg='#2c3e50',  # Darker color
                                 bg='#f8fafc')
            title_label.pack(pady=(15, 0))
    
    def display_credentials_table(self):
        """Display credentials in a nice table format"""
        # Clear existing table
        for widget in self.table_container.winfo_children():
            widget.destroy()
        
        # Create scrollable frame
        container = tk.Frame(self.table_container, bg='white')
        container.pack(fill='both', expand=True)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(container, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient='vertical', command=canvas.yview)
        
        # Create scrollable frame
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_width())
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Update canvas width when container resizes
        def update_canvas_width(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.bind('<Configure>', update_canvas_width)
        
        # Table header - ADJUSTED WIDTHS WITH MORE SPACE
        header_frame = tk.Frame(scrollable_frame, bg='#f8fafc', height=40)
        header_frame.pack(fill='x', pady=(0, 10))
        
        headers = ["Service", "Username", "Password", "Strength"]
        # INCREASED STRENGTH WIDTH, REDUCED OTHER COLUMNS SLIGHTLY
        widths = [0.23, 0.23, 0.20, 0.34]  # STRENGTH IS NOW 34% WIDTH
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            header_label = tk.Label(header_frame, text=header,
                                  font=('Arial', 10, 'bold'),
                                  fg='#4a5568',
                                  bg='#f8fafc',
                                  anchor='w',
                                  padx=15)
            header_label.place(relx=sum(widths[:i]), y=10, relwidth=width, height=20)
        
        # Display each credential
        for i, cred in enumerate(self.filtered_credentials):
            # Row with alternating background
            row_bg = '#ffffff' if i % 2 == 0 else '#f8fafc'
            row_frame = tk.Frame(scrollable_frame, bg=row_bg, height=50)
            row_frame.pack(fill='x', pady=(0, 1))
            
            # Service column (reduced width slightly)
            service_label = tk.Label(row_frame, text=cred['service'],
                                   font=('Arial', 11, 'bold'),
                                   fg='#2c3e50',
                                   bg=row_bg,
                                   anchor='w',
                                   padx=15)
            service_label.place(relx=0, y=15, relwidth=0.23, height=20)
            
            # Username column (reduced width slightly)
            username_label = tk.Label(row_frame, text=cred['username'],
                                    font=('Arial', 11),
                                    fg='#4a5568',
                                    bg=row_bg,
                                    anchor='w',
                                    padx=15)
            username_label.place(relx=0.23, y=15, relwidth=0.23, height=20)
            
            # Password column with toggle (reduced width)
            password_frame = tk.Frame(row_frame, bg=row_bg)
            password_frame.place(relx=0.46, y=10, relwidth=0.20, height=30)
            
            password_var = tk.StringVar(value="••••••••")
            password_label = tk.Label(password_frame, textvariable=password_var,
                                    font=('Arial', 10, 'bold'),
                                    fg='#718096',
                                    bg=row_bg)
            password_label.pack(side='left')
            
            eye_button = tk.Button(password_frame, text="👁",
                                 font=('Arial', 9),
                                 bg='#e2e8f0',
                                 fg='#4a5568',
                                 relief='flat',
                                 width=3,
                                 cursor='hand2')
            eye_button.config(
                command=lambda var=password_var, passwd=cred['password'], btn=eye_button, row=row_bg: 
                self.toggle_password_table(var, passwd, btn, row)
            )
            eye_button.pack(side='left', padx=(5, 0))
            
            # Strength column - SHORTER BOX SIZE
            strength_color = "#28a745" if cred['strength'] == "Strong" else "#dc3545"
            strength_icon = "✅" if cred['strength'] == "Strong" else "⚠️"
            strength_text = cred['strength']
            
            strength_frame = tk.Frame(row_frame, bg=row_bg)
            # Position: relx=0.66 (was 0.70), width=0.34 (was 0.30) - MORE SPACE
            strength_frame.place(relx=0.66, y=10, relwidth=0.34, height=30)
            
            # Create a canvas for the strength badge - SHORTER
            strength_canvas = tk.Canvas(strength_frame, bg=strength_color, highlightthickness=0, height=26)
            strength_canvas.pack(fill='both', expand=True, padx=8, pady=2)  # REDUCED PADDING from 15 to 8
            
            # Draw rectangle background - SHORTER LENGTH
            strength_canvas.create_rectangle(2, 2, 130, 26, fill=strength_color, outline=strength_color)  # REDUCED from 198 to 130
            
            # Add strength text with SAME FONT
            strength_canvas.create_text(66, 14,  # ADJUSTED POSITION for shorter box
                                      text=f"{strength_icon} {strength_text}",
                                      fill='white',
                                      font=('Arial', 11, 'bold'),
                                      anchor='center')
            
            # Hover effect
            row_frame.bind('<Enter>', lambda e, f=row_frame: f.config(bg='#edf2f7'))
            row_frame.bind('<Leave>', lambda e, f=row_frame, bg=row_bg: f.config(bg=bg))
    
    def perform_search(self, event=None):
        """Filter credentials based on search query"""
        search_term = self.search_entry.get().lower()
        
        if search_term == "search credentials..." or search_term == "":
            self.filtered_credentials = self.credentials.copy()
        else:
            self.filtered_credentials = [
                cred for cred in self.credentials 
                if (search_term in cred['service'].lower() or 
                    search_term in cred['username'].lower())
            ]
        
        # Update stats
        total = len(self.filtered_credentials)
        strong = sum(1 for c in self.filtered_credentials if c.get('strength') == 'Strong')
        self.stats_label.config(
            text=f"📊 {total} items • ✅ {strong} strong • ⚠️ {total-strong} weak"
        )
        
        # Update table
        self.display_credentials_table()
    
    def clear_search(self):
        """Clear search and show all credentials"""
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, "Search credentials...")
        self.perform_search()
    
    def toggle_password(self, password_var, actual_password, eye_button):
        """Toggle password visibility"""
        if password_var.get() == "••••••••":
            password_var.set(actual_password)
            eye_button.config(text="👁", fg='#4dabf7')
        else:
            password_var.set("••••••••")
            eye_button.config(text="👁🗨", fg='#495057')
    
    def toggle_password_table(self, password_var, actual_password, eye_button, row_bg):
        """Toggle password visibility in table"""
        if password_var.get() == "••••••••":
            password_var.set(actual_password)
            eye_button.config(text="👁", fg='#4dabf7', bg='#cbd5e0')
        else:
            password_var.set("••••••••")
            eye_button.config(text="👁", fg='#4a5568', bg='#e2e8f0')
    
    def show_credential_management(self):
        """Show credential management via callback if available"""
        if self.open_credentials_callback:
            self.open_credentials_callback()
        else:
            # Fallback: just show default screen
            for widget in self.frame.winfo_children():
                widget.destroy()
            
            black_panel = tk.Frame(self.frame, bg='#1a1a1a')
            black_panel.pack(fill='both', expand=True)
            
            back_button = tk.Button(black_panel, text="← Back to Dashboard",
                                  font=('Arial', 12, 'bold'),
                                  bg='#4dabf7',
                                  fg='white',
                                  relief='flat',
                                  padx=20,
                                  pady=10,
                                  cursor='hand2',
                                  command=self.create_dashboard)
            back_button.pack(anchor='nw', padx=20, pady=20)
            
            title = tk.Label(black_panel, text="🔐 CREDENTIAL MANAGEMENT",
                           font=('Arial', 32, 'bold'),
                           fg='white',
                           bg='#1a1a1a')
            title.pack(pady=(100, 50))
            
            message = tk.Label(black_panel, 
                             text="This is the Credential Management Screen\n\nYou can:\n• Add new credentials\n• Edit existing ones\n• Delete credentials\n• Organize by categories",
                             font=('Arial', 16),
                             fg='#cccccc',
                             bg='#1a1a1a',
                             justify='center')
            message.pack()

    
    def show_security_utilities(self):
        """Show security utilities white screen"""
        # Clear the main frame
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # Create black background (as requested)
        black_panel = tk.Frame(self.frame, bg='#1a1a1a')
        black_panel.pack(fill='both', expand=True)
        
        # Back button
        back_button = tk.Button(black_panel, text="← Back to Dashboard",
                              font=('Arial', 12, 'bold'),
                              bg='#4dabf7',
                              fg='white',
                              relief='flat',
                              padx=20,
                              pady=10,
                              cursor='hand2',
                              command=self.create_dashboard)
        back_button.pack(anchor='nw', padx=20, pady=20)
        
        # Title
        title = tk.Label(black_panel, text="🛡 SECURITY UTILITIES",
                       font=('Arial', 32, 'bold'),
                       fg='white',
                       bg='#1a1a1a')
        title.pack(pady=(100, 50))
        
        # Message
        message = tk.Label(black_panel, 
                         text="This is the Security Utilities Screen\n\nFeatures:\n• Password strength checker\n• Auto-lock settings\n• Security alerts\n• Two-factor authentication",
                         font=('Arial', 16),
                         fg='#cccccc',
                         bg='#1a1a1a',
                         justify='center')
        message.pack()
    
    def show_audit_logs(self):
        """Show audit logs white screen"""
        # Clear the main frame
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # Create black background (as requested)
        black_panel = tk.Frame(self.frame, bg='#1a1a1a')
        black_panel.pack(fill='both', expand=True)
        
        # Back button
        back_button = tk.Button(black_panel, text="← Back to Dashboard",
                              font=('Arial', 12, 'bold'),
                              bg='#4dabf7',
                              fg='white',
                              relief='flat',
                              padx=20,
                              pady=10,
                              cursor='hand2',
                              command=self.create_dashboard)
        back_button.pack(anchor='nw', padx=20, pady=20)
        
        # Title
        title = tk.Label(black_panel, text="📊 AUDIT AND LOGS",
                       font=('Arial', 32, 'bold'),
                       fg='white',
                       bg='#1a1a1a')
        title.pack(pady=(100, 50))
        
        # Message
        message = tk.Label(black_panel, 
                         text="This is the Audit and Logs Screen\n\nView:\n• Login history\n• Security events\n• Access logs\n• Activity reports",
                         font=('Arial', 16),
                         fg='#cccccc',
                         bg='#1a1a1a',
                         justify='center')
        message.pack()
