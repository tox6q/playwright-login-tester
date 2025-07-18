# 🚀 Universal Login Tester

A robust, intelligent login automation tool built with Playwright that can handle any website's login flow.

## ✨ Features

- **🔄 Single & Two-Step Login Support** - Automatically detects and handles both simple and complex login flows
- **🎯 Smart Element Detection** - Uses flexible selectors to find login fields on any website
- **✅ Intelligent Success/Failure Detection** - Tracks URL changes and error messages for accurate results
- **🌐 Universal Compatibility** - Works on everything from test sites to production platforms (X, Google, etc.)
- **👀 Visual Testing** - Runs in visible browser mode for easy debugging and verification

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install playwright

# Install browsers
playwright install
```

### Usage

```bash
# Basic usage (defaults to practice site)
python login_tester.py <username> <password>

# Specify custom website
python login_tester.py <username> <password> <url>
```

### Examples

```bash
# Test on practice site
python login_tester.py student Password123

# Test on custom site
python login_tester.py myuser mypass https://example.com/login

# Test two-step login (like X/Twitter)
python login_tester.py myuser mypass https://x.com/login
```

## 🧠 How It Works

1. **Smart Element Detection** - Uses multiple CSS selector patterns to find username, password fields, and submit buttons
2. **Two-Step Flow Detection** - If password field isn't found, automatically looks for "Next" buttons
3. **URL Change Tracking** - Monitors URL changes to detect successful navigation
4. **Content Analysis** - Scans page content for success/error indicators
5. **Comprehensive Reporting** - Provides detailed feedback on each step

## 🏆 Tested Websites

- ✅ Practice Test Automation
- ✅ Expand Testing Login
- ✅ The Internet (Heroku)
- ✅ X (Twitter) - Two-step flow
- ✅ And many more...

## 🔧 Customization

The tool automatically adapts to different websites, but you can modify the selector patterns in `login_tester.py` for specific sites if needed.

## 📝 License

MIT License - Feel free to use and modify for your projects!

---

**⚠️ Disclaimer**: This tool is for testing and educational purposes. Always respect website terms of service and rate limits. 