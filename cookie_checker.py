import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import http.cookies
from datetime import datetime
import threading
import json
import requests
from urllib.parse import unquote
from PIL import Image, ImageDraw, ImageFilter
import io

class ModernCookieCheckerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Netflix Cookie Checker")
        self.root.geometry("1600x900")
        
        # Modern color scheme
        self.bg_dark = "#0a0e27"  # Deep dark blue
        self.bg_secondary = "#1a1f3a"  # Slightly lighter blue
        self.accent_red = "#e50914"  # Netflix red
        self.accent_blue = "#564d8f"  # Purple accent
        self.text_light = "#e0e0e0"
        self.text_muted = "#8892b0"
        self.success_green = "#10b981"
        self.error_red = "#ef4444"
        
        self.root.configure(bg=self.bg_dark)
        
        # Create custom styles
        self.setup_modern_styles()
        self.create_modern_ui()
        self.checking = False
    
    def setup_modern_styles(self):
        style = ttk.Style()
        
        # Define custom styles
        style.configure('Dark.TFrame', background=self.bg_dark)
        style.configure('Card.TFrame', background=self.bg_secondary, relief=tk.FLAT)
        
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 24, 'bold'), 
                       background=self.bg_dark, 
                       foreground=self.accent_red)
        
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 9),
                       background=self.bg_dark,
                       foreground=self.text_muted)
        
        style.configure('SectionHeader.TLabel',
                       font=('Segoe UI', 13, 'bold'),
                       background=self.bg_secondary,
                       foreground=self.text_light)
        
        style.configure('TLabel', 
                       font=('Segoe UI', 9), 
                       background=self.bg_secondary, 
                       foreground=self.text_light)
        
        # Button styles
        style.configure('Modern.TButton',
                       font=('Segoe UI', 9, 'bold'),
                       background=self.accent_red,
                       foreground='white',
                       borderwidth=0,
                       relief=tk.FLAT,
                       padding=8)
        
        style.configure('Secondary.TButton',
                       font=('Segoe UI', 9),
                       background=self.bg_secondary,
                       foreground=self.text_light,
                       borderwidth=1,
                       relief=tk.FLAT,
                       padding=6)
        
        # Treeview
        style.configure('Modern.Treeview',
                       font=('Segoe UI', 9),
                       background=self.bg_secondary,
                       foreground=self.text_light,
                       fieldbackground=self.bg_secondary,
                       borderwidth=0)
        
        style.configure('Modern.Treeview.Heading',
                       font=('Segoe UI', 9, 'bold'),
                       background=self.accent_blue,
                       foreground='white',
                       borderwidth=0)
        
        style.map('Modern.Treeview', background=[('selected', self.accent_red)])
        style.map('Modern.Treeview.Heading', background=[('active', self.accent_red)])
    
    def create_modern_ui(self):
        # Main container with gradient effect
        main = ttk.Frame(self.root, style='Dark.TFrame')
        main.pack(fill=tk.BOTH, expand=True)
        
        # === HEADER SECTION ===
        header = tk.Frame(main, bg=self.bg_dark, height=110)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        # Add a subtle line under header
        line = tk.Frame(header, bg=self.accent_red, height=2)
        line.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Header content
        header_content = tk.Frame(header, bg=self.bg_dark)
        header_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)
        
        title = tk.Label(header_content, text="🎬 Netflix Cookie Checker", 
                        font=('Segoe UI', 28, 'bold'), 
                        bg=self.bg_dark, fg=self.accent_red)
        title.pack(anchor=tk.W)
        
        subtitle = tk.Label(header_content, 
                           text="Check and validate Netflix authentication cookies • Test active status • Export results",
                           font=('Segoe UI', 9),
                           bg=self.bg_dark, fg=self.text_muted)
        subtitle.pack(anchor=tk.W, pady=(5, 0))
        
        # === CONTENT AREA ===
        content = ttk.Frame(main, style='Dark.TFrame')
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left Panel - Input
        left_panel = tk.Frame(content, bg=self.bg_secondary, highlightthickness=1, 
                             highlightbackground=self.accent_blue)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 20), 
                       ipady=20, ipadx=20)
        
        left_title = tk.Label(left_panel, text="📋 Cookie Input", 
                             font=('Segoe UI', 12, 'bold'),
                             bg=self.bg_secondary, fg=self.accent_red)
        left_title.pack(anchor=tk.W, pady=(0, 10))
        
        desc = tk.Label(left_panel, text="Paste Netflix cookies (one per line):",
                       font=('Segoe UI', 8),
                       bg=self.bg_secondary, fg=self.text_muted)
        desc.pack(anchor=tk.W, pady=(0, 10))
        
        # Input text area
        self.input_text = scrolledtext.ScrolledText(
            left_panel, height=24, width=50,
            font=('Courier New', 8),
            bg="#0f1428", fg=self.text_light,
            insertbackground=self.accent_red,
            relief=tk.FLAT, borderwidth=0,
            highlightthickness=1, highlightbackground=self.accent_blue
        )
        self.input_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Input buttons
        input_btn_frame = tk.Frame(left_panel, bg=self.bg_secondary)
        input_btn_frame.pack(fill=tk.X)
        
        tk.Button(input_btn_frame, text="📂 Load File", command=self.load_from_file,
                 bg=self.accent_blue, fg='white', font=('Segoe UI', 9, 'bold'),
                 relief=tk.FLAT, padx=15, pady=8, cursor="hand2").pack(side=tk.LEFT, padx=3)
        
        tk.Button(input_btn_frame, text="🧹 Clear", command=self.clear_input,
                 bg=self.error_red, fg='white', font=('Segoe UI', 9, 'bold'),
                 relief=tk.FLAT, padx=15, pady=8, cursor="hand2").pack(side=tk.LEFT, padx=3)
        
        # Right Panel - Results
        right_panel = tk.Frame(content, bg=self.bg_secondary, highlightthickness=1,
                              highlightbackground=self.accent_blue)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, 
                        ipady=20, ipadx=20)
        
        # Results header
        results_header = tk.Frame(right_panel, bg=self.bg_secondary)
        results_header.pack(fill=tk.X, pady=(0, 15))
        
        results_title = tk.Label(results_header, text="🔍 Results",
                                font=('Segoe UI', 12, 'bold'),
                                bg=self.bg_secondary, fg=self.accent_red)
        results_title.pack(anchor=tk.W, side=tk.LEFT)
        
        # Action buttons
        action_frame = tk.Frame(right_panel, bg=self.bg_secondary)
        action_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Button(action_frame, text="✓ Check Format", command=self.check_format_only,
                 bg=self.success_green, fg='white', font=('Segoe UI', 9, 'bold'),
                 relief=tk.FLAT, padx=12, pady=7, cursor="hand2").pack(side=tk.LEFT, padx=4)
        
        tk.Button(action_frame, text="⚡ Test Active", command=self.check_cookies_active,
                 bg=self.accent_red, fg='white', font=('Segoe UI', 9, 'bold'),
                 relief=tk.FLAT, padx=12, pady=7, cursor="hand2").pack(side=tk.LEFT, padx=4)
        
        tk.Button(action_frame, text="📊 Export JSON", command=self.export_json,
                 bg=self.accent_blue, fg='white', font=('Segoe UI', 9, 'bold'),
                 relief=tk.FLAT, padx=12, pady=7, cursor="hand2").pack(side=tk.LEFT, padx=4)
        
        tk.Button(action_frame, text="📄 Export CSV", command=self.export_csv,
                 bg=self.accent_blue, fg='white', font=('Segoe UI', 9, 'bold'),
                 relief=tk.FLAT, padx=12, pady=7, cursor="hand2").pack(side=tk.LEFT, padx=4)
        
        tk.Button(action_frame, text="🗑️ Clear", command=self.clear_results,
                 bg=self.error_red, fg='white', font=('Segoe UI', 9, 'bold'),
                 relief=tk.FLAT, padx=12, pady=7, cursor="hand2").pack(side=tk.LEFT, padx=4)
        
        # Results tree
        tree_frame = tk.Frame(right_panel, bg=self.bg_secondary)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('Status', 'Valid', 'Active', 'Name', 'Value', 'Domain', 'Path', 'Expires')
        self.tree = ttk.Treeview(tree_frame, columns=columns, height=25, 
                                show='tree headings', style='Modern.Treeview')
        
        # Column configuration
        self.tree.column('#0', width=0)
        self.tree.column('Status', anchor=tk.CENTER, width=50)
        self.tree.column('Valid', anchor=tk.CENTER, width=70)
        self.tree.column('Active', anchor=tk.CENTER, width=90)
        self.tree.column('Name', anchor=tk.W, width=85)
        self.tree.column('Value', anchor=tk.W, width=130)
        self.tree.column('Domain', anchor=tk.W, width=85)
        self.tree.column('Path', anchor=tk.CENTER, width=50)
        self.tree.column('Expires', anchor=tk.W, width=100)
        
        for col in columns:
            self.tree.heading(col, text=col)
        
        # Scrollbars
        scrollbar_v = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_h = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscroll=scrollbar_v.set, xscroll=scrollbar_h.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_h.pack(side=tk.BOTTOM, fill=tk.X)
        
        # === FOOTER ===
        footer = tk.Frame(main, bg=self.accent_blue, height=50)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)
        
        self.status_var = tk.StringVar(value="Ready • 0 cookies loaded")
        status_bar = tk.Label(footer, textvariable=self.status_var,
                             font=('Segoe UI', 9),
                             bg=self.accent_blue, fg='white')
        status_bar.pack(side=tk.LEFT, padx=30, pady=12)
    
    def load_from_file(self):
        """Load cookies from a file"""
        filepath = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(1.0, content)
                num_cookies = len([c for c in content.split('\n') if c.strip()])
                self.status_var.set(f"✓ Loaded {num_cookies} cookies from file")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def check_format_only(self):
        """Check only cookie format"""
        self.clear_results()
        self.status_var.set("Checking cookie format...")
        self.root.update()
        
        cookie_strings = self.input_text.get(1.0, tk.END).strip().split('\n')
        cookie_strings = [c.strip() for c in cookie_strings if c.strip()]
        
        if not cookie_strings:
            messagebox.showwarning("Warning", "Please enter at least one cookie")
            return
        
        valid_count = 0
        for cookie_str in cookie_strings:
            try:
                parsed = self.parse_cookie(cookie_str)
                self.tree.insert('', 'end', values=(
                    '✓', '✓ Valid', '⏸️ Pending',
                    parsed.get('name', ''),
                    parsed.get('value', '')[:30] + '...',
                    parsed.get('domain', ''),
                    parsed.get('path', ''),
                    parsed.get('expires', '')
                ))
                valid_count += 1
            except Exception as e:
                self.tree.insert('', 'end', values=(
                    '✗', '✗ Invalid', '❌ Error',
                    'ERROR', str(e)[:30], '', '', ''
                ))
        
        self.status_var.set(f"✓ Format check: {valid_count}/{len(cookie_strings)} valid cookies")
    
    def check_cookies_active(self):
        """Check if cookies are actually working"""
        thread = threading.Thread(target=self.test_cookies_active, daemon=True)
        thread.start()
    
    def test_cookies_active(self):
        """Test cookies against Netflix API"""
        self.clear_results()
        self.checking = True
        
        cookie_strings = self.input_text.get(1.0, tk.END).strip().split('\n')
        cookie_strings = [c.strip() for c in cookie_strings if c.strip()]
        
        if not cookie_strings:
            messagebox.showwarning("Warning", "Please enter at least one cookie")
            return
        
        self.status_var.set(f"Testing {len(cookie_strings)} cookies...")
        self.root.update()
        
        active_count = 0
        for idx, cookie_str in enumerate(cookie_strings):
            try:
                parsed = self.parse_cookie(cookie_str)
                is_active = self.test_netflix_cookie(parsed.get('value', ''))
                
                active_status = '✅ ACTIVE' if is_active else '❌ INACTIVE'
                
                self.tree.insert('', 'end', values=(
                    '✓' if is_active else '⚠',
                    '✓ Valid', active_status,
                    parsed.get('name', ''),
                    parsed.get('value', '')[:30] + '...',
                    parsed.get('domain', ''),
                    parsed.get('path', ''),
                    parsed.get('expires', '')
                ))
                
                if is_active:
                    active_count += 1
            except Exception as e:
                self.tree.insert('', 'end', values=(
                    '✗', '✗ Invalid', '❌ Error',
                    'ERROR', str(e)[:30], '', '', ''
                ))
            
            if (idx + 1) % 5 == 0 or idx + 1 == len(cookie_strings):
                self.status_var.set(f"Testing: {idx + 1}/{len(cookie_strings)} | Active: {active_count}")
                self.root.update()
        
        self.checking = False
        self.status_var.set(f"✓ Completed: {active_count}/{len(cookie_strings)} active cookies")
    
    def test_netflix_cookie(self, cookie_value, timeout=5):
        """Test if Netflix cookie is active"""
        try:
            decoded_value = unquote(cookie_value)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            cookies = {'NetflixId': decoded_value}
            
            response = requests.get(
                'https://www.netflix.com/api/v1/user',
                headers=headers, cookies=cookies, timeout=timeout, allow_redirects=False
            )
            
            return response.status_code == 200
        except:
            return False
    
    def parse_cookie(self, cookie_str):
        """Parse a cookie string"""
        c = http.cookies.SimpleCookie()
        c.load(cookie_str)
        
        if not c:
            raise ValueError("No valid cookie found")
        
        morsel = list(c.values())[0]
        return {
            'name': list(c.keys())[0],
            'value': morsel.value,
            'domain': morsel['domain'] or 'N/A',
            'path': morsel['path'] or '/',
            'expires': morsel['expires'] or 'Session',
        }
    
    def clear_input(self):
        """Clear input text"""
        self.input_text.delete(1.0, tk.END)
        self.status_var.set("Input cleared")
    
    def clear_results(self):
        """Clear results tree"""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def export_json(self):
        """Export results as JSON"""
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
                    values = self.tree.item(item)['values']
                    results.append({
                        'status': values[0], 'valid': values[1], 'active': values[2],
                        'name': values[3], 'value': values[4], 'domain': values[5],
                        'path': values[6], 'expires': values[7]
                    })
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2)
                
                messagebox.showinfo("Success", f"✓ Exported {len(results)} results")
                self.status_var.set(f"✓ Exported to {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def export_csv(self):
        """Export results as CSV"""
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
                with open(filepath, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Status', 'Valid', 'Active', 'Name', 'Value', 'Domain', 'Path', 'Expires'])
                    
                    for item in self.tree.get_children():
                        values = self.tree.item(item)['values']
                        writer.writerow(values)
                
                messagebox.showinfo("Success", f"✓ Exported {len(self.tree.get_children())} results")
                self.status_var.set(f"✓ Exported to {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernCookieCheckerGUI(root)
    root.mainloop()
