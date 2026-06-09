import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import http.cookies
from datetime import datetime
import threading
import json
import requests
from urllib.parse import unquote

class CookieCheckerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Netflix Cookie Checker")
        self.root.geometry("1400x850")
        
        # Configure colors
        self.bg_color = "#0f0f0f"
        self.primary_color = "#e50914"  # Netflix red
        self.secondary_color = "#221f1f"
        self.accent_color = "#f5f5f1"
        self.text_color = "#ffffff"
        self.success_color = "#31c754"
        self.error_color = "#ff453a"
        
        self.root.configure(bg=self.bg_color)
        
        # Configure style
        self.setup_styles()
        
        # Create main frames
        self.create_widgets()
        self.checking = False
    
    def setup_styles(self):
        style = ttk.Style()
        
        # Configure custom colors - no theme loading
        style.configure('Dark.TFrame', background=self.bg_color)
        style.configure('Secondary.TFrame', background=self.secondary_color)
        style.configure('Title.TLabel', font=('Segoe UI', 20, 'bold'), background=self.bg_color, foreground=self.primary_color)
        style.configure('Header.TLabel', font=('Segoe UI', 11, 'bold'), background=self.secondary_color, foreground=self.accent_color)
        style.configure('TLabel', font=('Segoe UI', 10), background=self.secondary_color, foreground=self.text_color)
        style.configure('Status.TLabel', font=('Segoe UI', 9), background=self.bg_color, foreground=self.accent_color)
        
        # Button styling
        style.configure('Primary.TButton', font=('Segoe UI', 10, 'bold'), foreground=self.accent_color)
        style.configure('Secondary.TButton', font=('Segoe UI', 9))
        
        # Treeview styling
        style.configure('Treeview', font=('Segoe UI', 9), background=self.secondary_color, 
                       foreground=self.text_color, fieldbackground=self.secondary_color, borderwidth=0)
        style.configure('Treeview.Heading', font=('Segoe UI', 9, 'bold'), background=self.primary_color, 
                       foreground=self.accent_color)
    
    def create_widgets(self):
        # Main container
        main_container = ttk.Frame(self.root, style='Dark.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Header section
        header = ttk.Frame(main_container, style='Secondary.TFrame', height=100)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        # Netflix logo text
        title_label = ttk.Label(header, text="🎬 Netflix Cookie Checker", style='Title.TLabel')
        title_label.pack(pady=15, padx=20, anchor=tk.W)
        
        subtitle = ttk.Label(header, text="Check and validate Netflix authentication cookies • Test active status", 
                            font=('Segoe UI', 9), background=self.secondary_color, foreground="#999999")
        subtitle.pack(padx=20, anchor=tk.W)
        
        # Content area
        content = ttk.Frame(main_container, style='Dark.TFrame')
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Left panel (Input)
        left_panel = ttk.Frame(content, style='Secondary.TFrame')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=0, pady=0, ipadx=15, ipady=15)
        
        input_label = ttk.Label(left_panel, text="📋 Cookie Input", style='Header.TLabel')
        input_label.pack(anchor=tk.W, pady=(0, 10))
        
        desc_label = ttk.Label(left_panel, text="Paste Netflix cookies (one per line):", 
                              font=('Segoe UI', 9), background=self.secondary_color, foreground="#CCCCCC")
        desc_label.pack(anchor=tk.W, pady=(0, 8))
        
        self.input_text = scrolledtext.ScrolledText(left_panel, height=20, width=45, 
                                                     font=('Courier New', 9), 
                                                     bg="#1a1a1a", fg=self.text_color,
                                                     insertbackground=self.primary_color,
                                                     relief=tk.FLAT, borderwidth=1)
        self.input_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Control buttons
        button_frame = ttk.Frame(left_panel, style='Secondary.TFrame')
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="📂 Load File", command=self.load_from_file, style='Primary.TButton').pack(side=tk.LEFT, padx=3)
        ttk.Button(button_frame, text="🧹 Clear", command=self.clear_input, style='Secondary.TButton').pack(side=tk.LEFT, padx=3)
        
        # Right panel (Results)
        right_panel = ttk.Frame(content, style='Secondary.TFrame')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(15, 0), pady=0, ipadx=15, ipady=15)
        
        result_header_frame = ttk.Frame(right_panel, style='Secondary.TFrame')
        result_header_frame.pack(fill=tk.X, pady=(0, 10))
        
        result_label = ttk.Label(result_header_frame, text="🔍 Results", style='Header.TLabel')
        result_label.pack(side=tk.LEFT, anchor=tk.W)
        
        # Action buttons
        action_frame = ttk.Frame(right_panel, style='Secondary.TFrame')
        action_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(action_frame, text="✓ Check Format", command=self.check_format_only, style='Primary.TButton').pack(side=tk.LEFT, padx=3)
        ttk.Button(action_frame, text="⚡ Test Active", command=self.check_cookies_active, style='Primary.TButton').pack(side=tk.LEFT, padx=3)
        ttk.Button(action_frame, text="📊 Export JSON", command=self.export_json, style='Secondary.TButton').pack(side=tk.LEFT, padx=3)
        ttk.Button(action_frame, text="📄 Export CSV", command=self.export_csv, style='Secondary.TButton').pack(side=tk.LEFT, padx=3)
        ttk.Button(action_frame, text="🗑️ Clear", command=self.clear_results, style='Secondary.TButton').pack(side=tk.LEFT, padx=3)
        
        # Results tree
        columns = ('Status', 'Valid', 'Active', 'Name', 'Value', 'Domain', 'Path', 'Expires')
        self.tree = ttk.Treeview(right_panel, columns=columns, height=25, show='tree headings')
        
        # Define column headings and widths
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Status', anchor=tk.CENTER, width=50)
        self.tree.column('Valid', anchor=tk.CENTER, width=60)
        self.tree.column('Active', anchor=tk.CENTER, width=80)
        self.tree.column('Name', anchor=tk.W, width=90)
        self.tree.column('Value', anchor=tk.W, width=140)
        self.tree.column('Domain', anchor=tk.W, width=90)
        self.tree.column('Path', anchor=tk.CENTER, width=50)
        self.tree.column('Expires', anchor=tk.W, width=100)
        
        for col in columns:
            self.tree.heading(col, text=col)
        
        # Scrollbars
        scrollbar_v = ttk.Scrollbar(right_panel, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_h = ttk.Scrollbar(right_panel, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscroll=scrollbar_v.set, xscroll=scrollbar_h.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_v.grid(row=0, column=1, sticky='ns')
        scrollbar_h.grid(row=1, column=0, sticky='ew')
        
        right_panel.grid_rowconfigure(0, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)
        
        # Footer
        footer_frame = ttk.Frame(main_container, style='Secondary.TFrame', height=40)
        footer_frame.pack(fill=tk.X, padx=0, pady=0)
        footer_frame.pack_propagate(False)
        
        self.status_var = tk.StringVar(value="Ready • 0 cookies loaded")
        status_bar = ttk.Label(footer_frame, textvariable=self.status_var, style='Status.TLabel')
        status_bar.pack(side=tk.LEFT, padx=20, pady=10)
    
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
                self.status_var.set(f"Loaded {num_cookies} cookies from file")
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
        
        for cookie_str in cookie_strings:
            try:
                parsed = self.parse_cookie(cookie_str)
                self.tree.insert('', 'end', values=(
                    '✓',
                    '✓ Valid',
                    '⏸️ Not Tested',
                    parsed.get('name', ''),
                    parsed.get('value', '')[:35] + '...',
                    parsed.get('domain', ''),
                    parsed.get('path', ''),
                    parsed.get('expires', '')
                ))
            except Exception as e:
                self.tree.insert('', 'end', values=(
                    '✗',
                    '✗ Invalid',
                    '❌ Error',
                    'ERROR',
                    str(e)[:35],
                    '',
                    '',
                    ''
                ))
        
        self.status_var.set(f"Format check completed • {len(cookie_strings)} cookies checked")
    
    def check_cookies_active(self):
        """Check if cookies are actually working by testing with Netflix"""
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
        
        for idx, cookie_str in enumerate(cookie_strings):
            try:
                # Parse cookie format
                parsed = self.parse_cookie(cookie_str)
                
                # Test if active
                is_active = self.test_netflix_cookie(parsed.get('value', ''))
                
                active_status = '✅ ACTIVE' if is_active else '❌ INACTIVE'
                
                self.tree.insert('', 'end', values=(
                    '✓' if is_active else '⚠',
                    '✓ Valid',
                    active_status,
                    parsed.get('name', ''),
                    parsed.get('value', '')[:35] + '...',
                    parsed.get('domain', ''),
                    parsed.get('path', ''),
                    parsed.get('expires', '')
                ))
            except Exception as e:
                self.tree.insert('', 'end', values=(
                    '✗',
                    '✗ Invalid',
                    '❌ Error',
                    'ERROR',
                    str(e)[:35],
                    '',
                    '',
                    ''
                ))
            
            # Update status
            if (idx + 1) % 5 == 0 or idx + 1 == len(cookie_strings):
                self.status_var.set(f"Tested {idx + 1}/{len(cookie_strings)} cookies")
                self.root.update()
        
        self.checking = False
        self.status_var.set(f"Completed • {len(cookie_strings)} cookies tested")
    
    def test_netflix_cookie(self, cookie_value, timeout=5):
        """Test if Netflix cookie is active"""
        try:
            # Decode the cookie value
            decoded_value = unquote(cookie_value)
            
            # Try to make a request to Netflix with the cookie
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            cookies = {'NetflixId': decoded_value}
            
            # Make request to Netflix API endpoint
            response = requests.get(
                'https://www.netflix.com/api/v1/user',
                headers=headers,
                cookies=cookies,
                timeout=timeout,
                allow_redirects=False
            )
            
            # Check response status
            if response.status_code == 200:
                return True
            else:
                return False
                
        except requests.exceptions.Timeout:
            return None
        except requests.exceptions.ConnectionError:
            return None
        except Exception as e:
            return False
    
    def parse_cookie(self, cookie_str):
        """Parse a cookie string and extract information"""
        c = http.cookies.SimpleCookie()
        c.load(cookie_str)
        
        if not c:
            raise ValueError("No valid cookie found")
        
        # Get the first (and usually only) cookie
        morsel = list(c.values())[0]
        
        return {
            'name': list(c.keys())[0],
            'value': morsel.value,
            'domain': morsel['domain'] or 'N/A',
            'path': morsel['path'] or '/',
            'expires': morsel['expires'] or 'Session',
            'raw': cookie_str
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
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filepath:
            try:
                results = []
                for item in self.tree.get_children():
                    values = self.tree.item(item)['values']
                    results.append({
                        'status': values[0],
                        'valid_format': values[1],
                        'active': values[2],
                        'cookie_name': values[3],
                        'value_preview': values[4],
                        'domain': values[5],
                        'path': values[6],
                        'expires': values[7]
                    })
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2)
                
                messagebox.showinfo("Success", f"✓ Exported {len(results)} results")
                self.status_var.set(f"Exported to {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def export_csv(self):
        """Export results as CSV"""
        if not self.tree.get_children():
            messagebox.showwarning("Warning", "No results to export")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
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
                self.status_var.set(f"Exported to {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CookieCheckerGUI(root)
    root.mainloop()
