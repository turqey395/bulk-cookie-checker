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
        self.root.title("Bulk Cookie Checker")
        self.root.geometry("1200x750")
        self.root.configure(bg="#f0f0f0")
        
        # Configure style
        self.setup_styles()
        
        # Create main frames
        self.create_widgets()
        self.checking = False
    
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'), background='#f0f0f0')
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TLabel', background='#f0f0f0')
    
    def create_widgets(self):
        # Title
        title_label = ttk.Label(self.root, text="Bulk Cookie Checker - Netflix Edition", style='Header.TLabel')
        title_label.pack(pady=10)
        
        # Input Section
        input_frame = ttk.LabelFrame(self.root, text="Cookie Input", padding=10)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Paste cookies below (one per line):").pack(anchor=tk.W, pady=5)
        
        self.input_text = scrolledtext.ScrolledText(input_frame, height=6, width=80, font=('Courier', 9))
        self.input_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Buttons frame
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Load from File", command=self.load_from_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Check Cookies (Format Only)", command=self.check_format_only).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Test Cookies (Active Check)", command=self.check_cookies_active).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Input", command=self.clear_input).pack(side=tk.LEFT, padx=5)
        
        # Results Section
        results_frame = ttk.LabelFrame(self.root, text="Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Results tree
        columns = ('Status', 'Valid Format', 'Active', 'Cookie Name', 'Value Preview', 'Domain', 'Path', 'Expires')
        self.tree = ttk.Treeview(results_frame, columns=columns, height=12, show='tree headings')
        
        # Define column headings and widths
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Status', anchor=tk.W, width=60)
        self.tree.column('Valid Format', anchor=tk.W, width=80)
        self.tree.column('Active', anchor=tk.W, width=80)
        self.tree.column('Cookie Name', anchor=tk.W, width=100)
        self.tree.column('Value Preview', anchor=tk.W, width=120)
        self.tree.column('Domain', anchor=tk.W, width=80)
        self.tree.column('Path', anchor=tk.W, width=60)
        self.tree.column('Expires', anchor=tk.W, width=100)
        
        for col in columns:
            self.tree.heading(col, text=col)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Export frame
        export_frame = ttk.Frame(self.root)
        export_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(export_frame, text="Export Results (JSON)", command=self.export_json).pack(side=tk.LEFT, padx=5)
        ttk.Button(export_frame, text="Export Results (CSV)", command=self.export_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(export_frame, text="Clear Results", command=self.clear_results).pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
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
                self.status_var.set(f"Loaded cookies from file")
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
                    'Valid',
                    'Not Tested',
                    parsed.get('name', ''),
                    parsed.get('value', '')[:40] + '...',
                    parsed.get('domain', ''),
                    parsed.get('path', ''),
                    parsed.get('expires', '')
                ))
            except Exception as e:
                self.tree.insert('', 'end', values=(
                    '✗',
                    'Invalid',
                    'N/A',
                    'ERROR',
                    str(e)[:40],
                    '',
                    '',
                    ''
                ))
        
        self.status_var.set(f"Format check completed: {len(cookie_strings)} cookies")
    
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
        
        self.status_var.set(f"Testing {len(cookie_strings)} cookies against Netflix...")
        self.root.update()
        
        for idx, cookie_str in enumerate(cookie_strings):
            try:
                # Parse cookie format
                parsed = self.parse_cookie(cookie_str)
                
                # Test if active
                is_active = self.test_netflix_cookie(parsed.get('value', ''))
                
                self.tree.insert('', 'end', values=(
                    '✓' if is_active else '⚠',
                    'Valid',
                    '✓ ACTIVE' if is_active else '✗ INACTIVE/EXPIRED',
                    parsed.get('name', ''),
                    parsed.get('value', '')[:40] + '...',
                    parsed.get('domain', ''),
                    parsed.get('path', ''),
                    parsed.get('expires', '')
                ))
            except Exception as e:
                self.tree.insert('', 'end', values=(
                    '✗',
                    'Invalid',
                    'ERROR',
                    'ERROR',
                    str(e)[:40],
                    '',
                    '',
                    ''
                ))
            
            # Update status
            if (idx + 1) % 5 == 0 or idx + 1 == len(cookie_strings):
                self.status_var.set(f"Tested {idx + 1}/{len(cookie_strings)} cookies")
                self.root.update()
        
        self.checking = False
        self.status_var.set(f"Completed: {len(cookie_strings)} cookies tested")
    
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
            # 200 = Valid/Active cookie
            # 401 = Unauthorized/Invalid cookie
            # 403 = Forbidden/Expired
            if response.status_code == 200:
                return True
            else:
                return False
                
        except requests.exceptions.Timeout:
            return None  # Could not determine
        except requests.exceptions.ConnectionError:
            return None  # No internet
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
                
                messagebox.showinfo("Success", f"Results exported to {filepath}")
                self.status_var.set(f"Exported {len(results)} results to JSON")
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
                    writer.writerow(['Status', 'Valid Format', 'Active', 'Cookie Name', 'Value Preview', 'Domain', 'Path', 'Expires'])
                    
                    for item in self.tree.get_children():
                        values = self.tree.item(item)['values']
                        writer.writerow(values)
                
                messagebox.showinfo("Success", f"Results exported to {filepath}")
                self.status_var.set(f"Exported {len(self.tree.get_children())} results to CSV")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CookieCheckerGUI(root)
    root.mainloop()
