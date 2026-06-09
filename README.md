# Bulk Cookie Checker GUI

A desktop application for validating and analyzing multiple HTTP cookies at once. Built with Python and Tkinter.

## Features

✅ **Bulk Cookie Input** - Paste multiple cookies at once  
✅ **File Loading** - Load cookies from a .txt file  
✅ **Cookie Parsing** - Extracts name, value, domain, path, expires, secure, and HttpOnly flags  
✅ **Status Tracking** - Real-time processing updates  
✅ **Results Display** - Table view with all cookie attributes  
✅ **Export Options** - Save results as JSON or CSV  
✅ **Multi-threaded** - Processing doesn't freeze the UI  
✅ **Error Handling** - Shows validation status for each cookie  

## Installation

No external dependencies required! Only uses Python standard library.

```bash
git clone https://github.com/turqey395/bulk-cookie-checker.git
cd bulk-cookie-checker
python cookie_checker.py
```

## Usage

1. **Paste Cookies** - Paste your cookies in the input area (one per line)
2. **Load from File** - Or load cookies from a text file
3. **Check Cookies** - Click "Check Cookies" to validate and parse
4. **View Results** - See parsed cookie details in the results table
5. **Export** - Export results as JSON or CSV

## Cookie Format

Cookies should be in standard HTTP cookie format:
```
name=value; Domain=example.com; Path=/; Expires=Wed, 09 Jun 2026 10:18:14 GMT; Secure; HttpOnly
```

## Results Table Columns

| Column | Description |
|--------|-------------|
| Status | Valid or Invalid |
| Name | Cookie name |
| Value | Cookie value (truncated to 50 chars) |
| Domain | Cookie domain |
| Path | Cookie path |
| Expires | Expiration date or "Session" |
| Secure | ✓ if secure flag is set |
| HttpOnly | ✓ if HttpOnly flag is set |

## Export Formats

### JSON Export
```json
[
  {
    "status": "Valid",
    "name": "session_id",
    "value": "abc123...",
    "domain": "example.com",
    "path": "/",
    "expires": "Wed, 09 Jun 2026 10:18:14 GMT",
    "secure": "✓",
    "httponly": "✓"
  }
]
```

### CSV Export
Standard CSV format with headers matching the results table columns.

## License

MIT
