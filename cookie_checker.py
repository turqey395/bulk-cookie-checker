import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import http.cookies
from datetime import datetime
import threading
import json
import requests
from urllib.parse import unquote

class PremiumCookieCheckerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Netflix Cookie Checker")
        self.root.geometry("1700x950")
        self.root.minsize(1200, 700)
        
        # Premium color palette
        self.BG_MAIN = "#0f1419"  # Main background
        self.BG_CARD = "#1a1f2e"  # Card background
        self.BG_INPUT = "#141820"  # Input background
        self.ACCENT_RED = "#e50914"  # Netflix red
        self.ACCENT_BLUE = "#0080ff"  # Blue accent
        self.ACCENT_GREEN = "#10b981"  # Green for success
        self.TEXT_PRIMARY = "#ffffff"  # Primary text
        self.TEXT_SECONDARY = "#a0aec0"  # Secondary text
        self.BORDER_COLOR = "#2d3748"  # Border color
        
        self.root.configure(bg=self.BG_MAIN)
        
        self.setup_styles()
        self.create_ui()
        self.checking = False
    
    def setup_styles(self):
        style = ttk.Style()
        
        # Configure all frame styles
        style.configure('Main.TFrame', background=self.BG_MAIN)
        style.configure('Card.TFrame', background=self.BG_CARD)
        
        # Label styles
        style.configure('Title.TLabel',
                       font=('Segoe UI', 26, 'bold'),
                       background=self.BG_MAIN,
                       foreground=self.ACCENT_RED)
        
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 10),
                       background=self.BG_MAIN,
                       foreground=self.TEXT_SECONDARY)
        
        style.configure('SectionTitle.TLabel',
                       font=('Segoe UI', 13, 'bold'),
                       background=self.BG_CARD,
                       foreground=self.ACCENT_RED)
        
        style.configure('TLabel',
                       font=('Segoe UI', 9),
                       background=self.BG_CARD,
                       foreground=self.TEXT_PRIMARY)
        
        # Treeview style - DARK THEMED
        style.configure('Premium.Treeview',
                       font=('Segoe UI', 9),
                       background=self.BG_INPUT,
                       foreground=self.TEXT_PRIMARY,
                       fieldbackground=self.BG_INPUT,
                       borderwidth=0,
                       relief='flat')
        
        style.configure('Premium.Treeview.Heading',
                       font=('Segoe UI', 9, 'bold'),
                       background=self.ACCENT_BLUE,
                       foreground=self.TEXT_PRIMARY,
                       borderwidth=0,
                       relief='flat')
        
        style.map('Premium.Treeview',
                 background=[('selected', self.ACCENT_RED)],
                 foreground=[('selected', self.TEXT_PRIMARY)])
        
        style.map('Premium.Treeview.Heading',
                 background=[('active', self.ACCENT_RED)])
    
    def create_ui(self):
        # Main container
        main = ttk.Frame(self.root, style='Main.TFrame')
        main.pack(fill=tk.BOTH, expand=True)
        
        # ===== HEADER =====
        self.create_header(main)
        
        # ===== CONTENT AREA =====
        content_container = ttk.Frame(main, style='Main.TFrame')
        content_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)
        
        # Left panel - Input
        self.create_left_panel(content_container)
        
        # Right panel - Results
        self.create_right_panel(content_container)
        
        # ===== FOOTER =====
        self.create_footer(main)
    
    def create_header(self, parent):
        """Create header section"""
        header = tk.Frame(parent, bg=self.BG_MAIN, height=120)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        # Accent line
        accent_line = tk.Frame(header, bg=self.ACCENT_RED, height=3)
        accent_line.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Header content
        header_content = tk.Frame(header, bg=self.BG_MAIN)
        header_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        title = tk.Label(header_content,
                        text="🎬 Netflix Cookie Checker",
                        font=('Segoe UI', 28, 'bold'),
                        bg=self.BG_MAIN,
                        fg=self.ACCENT_RED)
        title.pack(anchor=tk.W)
        
        subtitle = tk.Label(header_content,
                           text="Validate • Test • Export | Check Netflix authentication cookies in bulk",
                           font=('Segoe UI', 10),
                           bg=self.BG_MAIN,
                           fg=self.TEXT_SECONDARY)
        subtitle.pack(anchor=tk.W, pady=(8, 0))
    
    def create_left_panel(self, parent):
        """Create left input panel"""
        left = tk.Frame(parent, bg=self.BG_CARD, relief=tk.FLAT, bd=0)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 20))
        
        # Border effect
        border = tk.Frame(left, bg=self.BORDER_COLOR, width=1)
        border.pack(side=tk.RIGHT, fill=tk.Y)
        
        content = tk.Frame(left, bg=self.BG_CARD)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title = tk.Label(content,
                        text="📋 Cookie Input",
                        font=('Segoe UI', 12, 'bold'),
                        bg=self.BG_CARD,
                        fg=self.ACCENT_RED)
        title.pack(anchor=tk.W, pady=(0, 12))
        
        # Description
        desc = tk.Label(content,
                       text="Paste Netflix cookies below\n(one per line)",
                       font=('Segoe UI', 8),
                       bg=self.BG_CARD,
                       fg=self.TEXT_SECONDARY,
                       justify=tk.LEFT)
        desc.pack(anchor=tk.W, pady=(0, 12))
        
        # Input text area
        self.input_text = scrolledtext.ScrolledText(
            content,
            height=26,
            width=48,
            font=('Courier New', 8),
            bg=self.BG_INPUT,
            fg=self.TEXT_PRIMARY,
            insertbackground=self.ACCENT_RED,
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=self.BORDER_COLOR,
            wrap=tk.WORD
        )
        self.input_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Buttons
        button_frame = tk.Frame(content, bg=self.BG_CARD)
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        load_btn = tk.Button(
            button_frame,
            text="📂 Load File",
            command=self.load_from_file,
            bg=self.ACCENT_BLUE,
            fg=self.TEXT_PRIMARY,
            font=('Segoe UI', 9, 'bold'),
            relief=tk.FLAT,
            padx=16,
            pady=10,
            cursor="hand2",
            activebackground=self.ACCENT_RED,
            activeforeground=self.TEXT_PRIMARY
        )
        load_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(
            button_frame,
            text="🧹 Clear Input",
            command=self.clear_input,
            bg=self.ACCENT_RED,
            fg=self.TEXT_PRIMARY,
            font=('Segoe UI', 9, 'bold'),
            relief=tk.FLAT,
            padx=16,
            pady=10,
            cursor="hand2",
            activebackground=self.ACCENT_BLUE,
            activeforeground=self.TEXT_PRIMARY
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
    
    def create_right_panel(self, parent):
        """Create right results panel"""
        right = tk.Frame(parent, bg=self.BG_CARD, relief=tk.FLAT, bd=0)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Border effect
        border = tk.Frame(right, bg=self.BORDER_COLOR, width=1)
        border.pack(side=tk.LEFT, fill=tk.Y)
        
        content = tk.Frame(right, bg=self.BG_CARD)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(content, bg=self.BG_CARD)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        title = tk.Label(header_frame,
                        text="🔍 Results",
                        font=('Segoe UI', 12, 'bold'),
                        bg=self.BG_CARD,
                        fg=self.ACCENT_RED)
        title.pack(anchor=tk.W, side=tk.LEFT)
        
        # Action buttons
        button_frame = tk.Frame(content, bg=self.BG_CARD)
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        buttons = [
            ("✓ Check Format", self.check_format_only, self.ACCENT_GREEN),
            ("⚡ Test Active", self.check_cookies_active, self.ACCENT_RED),
            ("📊 JSON", self.export_json, self.ACCENT_BLUE),
            ("📄 CSV", self.export_csv, self.ACCENT_BLUE),
            ("🗑️ Clear", self.clear_results, "#e74c3c"),
        ]
        
        for text, cmd, color in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                command=cmd,
                bg=color,
                fg=self.TEXT_PRIMARY,
                font=('Segoe UI', 8, 'bold'),
                relief=tk.FLAT,
                padx=12,
                pady=8,
                cursor="hand2",
                activebackground=self.ACCENT_RED,
                activeforeground=self.TEXT_PRIMARY,
                bd=0
            )
            btn.pack(side=tk.LEFT, padx=4)
        
        # Results table
        table_frame = tk.Frame(content, bg=self.BG_INPUT, highlightthickness=1,
                              highlightbackground=self.BORDER_COLOR)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 0))
        
        columns = ('Status', 'Valid', 'Active', 'Name', 'Value', 'Domain', 'Path', 'Expires')
        self.tree = ttk.Treeview(table_frame, columns=columns, height=24,
                                show='tree headings', style='Premium.Treeview')
        
        # Column setup
        widths = [50, 65, 85, 80, 140, 85, 45, 100]
        for col, width in zip(columns, widths):
            self.tree.column(col, anchor=tk.W, width=width)
            self.tree.heading(col, text=col)
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
    
    def create_footer(self, parent):
        """Create footer section"""
        footer = tk.Frame(parent, bg=self.ACCENT_BLUE, height=50)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)
        
        self.status_var = tk.StringVar(value="Ready • 0 cookies loaded")
        status = tk.Label(footer,
                         textvariable=self.status_var,
                         font=('Segoe UI', 9),
                         bg=self.ACCENT_BLUE,
                         fg=self.TEXT_PRIMARY)
        status.pack(side=tk.LEFT, padx=30, pady=12)
    
    def load_from_file(self):
        """Load cookies from file"""
        filepath = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(1.0, content)
                num = len([c for c in content.split('\n') if c.strip()])
                self.status_var.set(f"✓ Loaded {num} cookies")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load: {str(e)}")
    
    def check_format_only(self):
        """Check cookie format"""
        self.clear_results()
        self.status_var.set("Checking cookie format...")
        self.root.update()
        
        cookies = self.input_text.get(1.0, tk.END).strip().split('\n')
        cookies = [c.strip() for c in cookies if c.strip()]
        
        if not cookies:
            messagebox.showwarning("Warning", "Enter at least one cookie")
            return
        
        valid = 0
        for cookie_str in cookies:
            try:
                parsed = self.parse_cookie(cookie_str)
                self.tree.insert('', 'end', values=(
                    '✓', '✓ Valid', '⏸️ Pending',
                    parsed['name'], parsed['value'][:28] + '...',
                    parsed['domain'], parsed['path'], parsed['expires']
                ))
                valid += 1
            except:
                self.tree.insert('', 'end', values=(
                    '✗', '✗ Invalid', '❌', 'ERROR', 'Invalid format', '', '', ''
                ))
        
        self.status_var.set(f"✓ Format check: {valid}/{len(cookies)} valid")
    
    def check_cookies_active(self):
        """Test cookies"""
        thread = threading.Thread(target=self._test_active, daemon=True)
        thread.start()
    
    def _test_active(self):
        """Background test"""
        self.clear_results()
        
        cookies = self.input_text.get(1.0, tk.END).strip().split('\n')
        cookies = [c.strip() for c in cookies if c.strip()]
        
        if not cookies:
            messagebox.showwarning("Warning", "Enter at least one cookie")
            return
        
        self.status_var.set(f"Testing {len(cookies)} cookies...")
        self.root.update()
        
        active = 0
        for idx, cookie_str in enumerate(cookies):
            try:
                parsed = self.parse_cookie(cookie_str)
                is_active = self.test_netflix_cookie(parsed['value'])
                status = '✅ ACTIVE' if is_active else '❌ INACTIVE'
                
                self.tree.insert('', 'end', values=(
                    '✓' if is_active else '⚠',
                    '✓ Valid', status,
                    parsed['name'], parsed['value'][:28] + '...',
                    parsed['domain'], parsed['path'], parsed['expires']
                ))
                if is_active:
                    active += 1
            except:
                self.tree.insert('', 'end', values=(
                    '✗', '✗ Invalid', '❌', 'ERROR', 'Invalid', '', '', ''
                ))
            
            if (idx + 1) % 5 == 0:
                self.status_var.set(f"Testing: {idx + 1}/{len(cookies)} | Active: {active}")
                self.root.update()
        
        self.status_var.set(f"✓ Complete: {active}/{len(cookies)} active")
    
    def test_netflix_cookie(self, cookie_value, timeout=5):
        """Test if cookie works"""
        try:
            decoded = unquote(cookie_value)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            cookies = {'NetflixId': decoded}
            
            r = requests.get('https://www.netflix.com/api/v1/user',
                           headers=headers, cookies=cookies, timeout=timeout)
            return r.status_code == 200
        except:
            return False
    
    def parse_cookie(self, cookie_str):
        """Parse cookie"""
        c = http.cookies.SimpleCookie()
        c.load(cookie_str)
        if not c:
            raise ValueError("Invalid cookie")
        
        m = list(c.values())[0]
        return {
            'name': list(c.keys())[0],
            'value': m.value,
            'domain': m['domain'] or 'N/A',
            'path': m['path'] or '/',
            'expires': m['expires'] or 'Session',
        }
    
    def clear_input(self):
        """Clear input"""
        self.input_text.delete(1.0, tk.END)
        self.status_var.set("Input cleared")
    
    def clear_results(self):
        """Clear results"""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def export_json(self):
        """Export JSON"""
        if not self.tree.get_children():
            messagebox.showwarning("Warning", "No results to export")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        
        if filepath:
            try:
                results = []
                for item in self.tree.get_children():
                    vals = self.tree.item(item)['values']
                    results.append({
                        'status': vals[0], 'valid': vals[1], 'active': vals[2],
                        'name': vals[3], 'value': vals[4], 'domain': vals[5],
                        'path': vals[6], 'expires': vals[7]
                    })
                
                with open(filepath, 'w') as f:
                    json.dump(results, f, indent=2)
                
                messagebox.showinfo("Success", f"✓ Exported {len(results)} results")
                self.status_var.set(f"✓ Exported JSON")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def export_csv(self):
        """Export CSV"""
        if not self.tree.get_children():
            messagebox.showwarning("Warning", "No results to export")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        
        if filepath:
            try:
                import csv
                with open(filepath, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Status', 'Valid', 'Active', 'Name', 'Value', 'Domain', 'Path', 'Expires'])
                    
                    for item in self.tree.get_children():
                        writer.writerow(self.tree.item(item)['values'])
                
                messagebox.showinfo("Success", f"✓ Exported CSV")
                self.status_var.set(f"✓ Exported CSV")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PremiumCookieCheckerGUI(root)
    root.mainloop()
