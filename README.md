# Bulk Cookie Checker - Netflix Edition

A modern, beautiful desktop application for validating and analyzing Netflix authentication cookies in bulk.

## 🎬 Features

✅ **Modern Dark UI** - Netflix-inspired theme with sleek design  
✅ **Bulk Cookie Input** - Paste multiple cookies at once  
✅ **File Loading** - Load cookies from .txt or .csv files  
✅ **Format Validation** - Check if cookies are properly formatted  
✅ **Active Testing** - Test if cookies actually work with Netflix  
✅ **Real-time Results** - Beautiful table with all cookie details  
✅ **Export Options** - Save results as JSON or CSV  
✅ **Multi-threaded** - Processing doesn't freeze the UI  
✅ **Professional Design** - Dark mode, emojis, color-coded results  

## 📦 Requirements

- Python 3.7+
- requests
- ttkbootstrap

## 🚀 Installation & Setup

### Step 1: Install Python
1. Download from https://www.python.org/downloads/
2. **Check "Add Python to PATH"** ✓
3. Install

### Step 2: Extract Files
1. Right-click the ZIP file
2. Click "Extract All"
3. Open the folder

### Step 3: Install Dependencies
Open Command Prompt in the folder and run:
```bash
pip install requests ttkbootstrap
```

### Step 4: Run the App
```bash
python cookie_checker.py
```

**OR** double-click `run.bat` if it exists.

## 📖 Usage Guide

### 1. Load Cookies
- **Paste Directly**: Copy and paste Netflix cookies into the left panel (one per line)
- **Load from File**: Click "📂 Load File" to import from a .txt or .csv file

### 2. Check Format
Click **"✓ Check Format"** to validate cookie structure without testing:
- Shows if format is valid
- Displays cookie details
- Fast validation

### 3. Test Active Status
Click **"⚡ Test Active"** to verify cookies work with Netflix:
- ✅ ACTIVE = Cookie works
- ❌ INACTIVE = Cookie expired/dead
- Takes a few seconds per cookie

### 4. Export Results
- **📊 Export JSON** - Programmatic format
- **📄 Export CSV** - Excel/Spreadsheet format
- **🗑️ Clear** - Remove results

## 🍪 Cookie Format

Netflix cookies should look like:
```
NetflixId=v%3D3%26ct%3DBgjHlOvcAxKiAyvJPJjHwV2Tzzberg0ezpOd6GiRCw1TymQujXjrHEYP15V1klnJb_dIBBDqr00bpX_34d3JHh5LMjf1UkR32pJRQGfVvoec-bYsTQxbO8HyvHijfRhBE4LvIt5rMu-xHoLnMCcBPMUnAwmFOjo-nmU0Itn2r5KfXpuNeqS9ASSIwz4XuuCw5Mdks4Ou4jqQlu8LhdyVCRfD0qxP-SBphiUCvt-0Bn3pYVlZXXKjHvQnJKrWMN1lk06L3f47C4el1PDxe60gdE6M63xoWZ4ZgZ-ahdXi5YhaaoZ6zHwduYobBaUAbsdL_66Pe_A9h1YR9ZaH016R7iBzmpp9r5c_ATCg7t6k57qa8LMJwWxekQlF2Wcfy_-ls3AqgqO95ezLSt6gXLK0t90i60Cy5GKyHiNKbXgO6hpzW33Ah7xIzWGAGF7Q63bQMlESNQjwSCPAw5AvHkAV44VR62Y-XFBg7MEaFAegTzqvtiL81kLBNZ7tVAIiunPI2ciZ0R7PEZCu-OpvZaOqyJwKSzIOJDXiS67CqVeWgb_0RYJeBkvQVf4f4aYYBiIOCgx3DHfSnckQH9nykho.%26pg%3DSIWIAJ6DYBHIFBOVSNBNYDZRM4%26ch%3DAQEAEAABABRyRmkw129twHtdlVI6DRLHoHQv4jXV5qI.
```

## 🎨 UI Features

- **Dark Theme** - Netflix-inspired black and red
- **Split Layout** - Input on left, results on right
- **Emoji Icons** - Quick visual recognition
- **Status Bar** - Real-time progress updates
- **Professional Table** - Clean, organized results
- **Color-Coded** - Green for valid, red for invalid

## 📊 Results Columns

| Column | Description |
|--------|-------------|
| Status | ✓ Valid / ✗ Invalid |
| Valid | ✓ Valid Format / ✗ Invalid Format |
| Active | ✅ ACTIVE / ❌ INACTIVE |
| Name | Cookie name (NetflixId) |
| Value | Cookie value preview (first 35 chars) |
| Domain | Cookie domain |
| Path | Cookie path |
| Expires | Expiration date or "Session" |

## 💾 Export Formats

### JSON Export
```json
[
  {
    "status": "✓",
    "valid_format": "✓ Valid",
    "active": "✅ ACTIVE",
    "cookie_name": "NetflixId",
    "value_preview": "v%3D3%26ct%3DBgjHlOvcAxKiAyvJPJj...",
    "domain": "netflix.com",
    "path": "/",
    "expires": "Session"
  }
]
```

### CSV Export
Standard CSV format compatible with Excel and Google Sheets

## ⚙️ Troubleshooting

### App won't open
1. Check Python is installed: `python --version`
2. Install dependencies: `pip install requests ttkbootstrap`
3. Run from command prompt: `python cookie_checker.py`

### Dependencies not installing
Try with admin Command Prompt:
```bash
pip install --upgrade requests ttkbootstrap
```

### Cookies not testing
- Check internet connection
- Verify cookie format is correct
- Netflix API might be rate-limiting (wait a minute)

## 🔒 Security Note

- Never share your Netflix cookies publicly
- Cookies contain authentication tokens
- Keep them private and secure
- Don't paste them in public forums

## 📝 License

MIT License - Feel free to use and modify!

## 🎯 Version

**v2.0** - Modern UI Redesign
- Beautiful Netflix-inspired dark theme
- Split-panel layout
- Improved emoji indicators
- Better organization

---

**Made with ❤️ for cookie checking**
