#!/usr/bin/env python3
"""
Simple login tester using Playwright
Usage: python login_tester.py <username> <password> [url]
"""

import sys
import asyncio
from playwright.async_api import async_playwright

async def test_login(username, password, url=None):
    """Test login functionality on a website"""
    
    # Default to the practice test site if no URL provided
    if url is None:
        url = "https://practicetestautomation.com/practice-test-login/"
    
    print(f"🚀 Starting login test for: {url}")
    print(f"👤 Username: {username}")
    print(f"🔒 Password: {'*' * len(password)}")
    
    async with async_playwright() as p:
        # Launch browser in visible mode (headless=False)
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        page = await browser.new_page()
        
        try:
            # Navigate to login page
            print(f"\n📖 Navigating to: {url}")
            await page.goto(url)
            await page.wait_for_load_state('networkidle')
            
            # Find and fill username field
            print("🔍 Looking for username field...")
            username_field = page.locator('input[name="username"], input[id="username"], input[type="text"]').first
            await username_field.fill(username)
            print(f"✅ Username entered: {username}")
            
            # Try to find password field first
            print("🔍 Looking for password field...")
            password_field = page.locator('input[name="password"], input[id="password"], input[type="password"]').first
            
            try:
                # Check if password field exists (with short timeout)
                await password_field.wait_for(timeout=3000)
                await password_field.fill(password)
                print("✅ Password entered")
                
                # Find and click submit button
                print("🔍 Looking for submit button...")
                submit_button = page.locator('button[type="submit"], input[type="submit"], button:has-text("Submit"), button:has-text("Log in"), button:has-text("Login"), button:has-text("Sign in")').first
                
                # Store URL before clicking submit
                initial_url = page.url
                await submit_button.click()
                print("✅ Login button clicked")
                
            except:
                # Password field not found - likely a two-step login
                print("⚠️  Password field not found - checking for two-step login...")
                
                # Look for Next/Continue/Proceed buttons
                print("🔍 Looking for Next/Continue button...")
                next_button = page.locator('button:has-text("Next"), button:has-text("Continue"), button:has-text("Proceed"), button:has-text("Continue to"), button[data-testid*="next"], button[data-testid*="continue"]').first
                await next_button.click()
                print("✅ Next button clicked")
                
                # Wait for next page to load
                await page.wait_for_load_state('networkidle')
                await asyncio.sleep(2)
                
                # Now try to find password field again
                print("🔍 Looking for password field on step 2...")
                password_field = page.locator('input[name="password"], input[id="password"], input[type="password"]').first
                await password_field.fill(password)
                print("✅ Password entered")
                
                # Find and click final submit button
                print("🔍 Looking for final submit button...")
                submit_button = page.locator('button[type="submit"], input[type="submit"], button:has-text("Submit"), button:has-text("Log in"), button:has-text("Login"), button:has-text("Sign in")').first
                
                # Store URL before clicking submit
                initial_url = page.url
                await submit_button.click()
                print("✅ Final login button clicked")
            
            # Wait for navigation/response
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(2)  # Give it a moment
            
            # Check current state
            current_url = page.url
            page_content = await page.content()
            
            print(f"\n📍 Initial URL: {initial_url}")
            print(f"📍 Current URL: {current_url}")
            
            login_successful = False
            
            # First check: Did the URL change? (Good sign)
            if current_url != initial_url:
                print("✅ URL changed - potential success!")
                
                # Check for success indicators
                success_indicators = [
                    'dashboard', 'welcome', 'logged-in-successfully', 'logout', 'profile',
                    'successfully logged in', 'congratulations', 'secure'
                ]
                
                for indicator in success_indicators:
                    if indicator.lower() in current_url.lower() or indicator.lower() in page_content.lower():
                        login_successful = True
                        print(f"✅ SUCCESS! Found success indicator: '{indicator}'")
                        break
                        
            else:
                # URL didn't change - RED FLAG! Check for errors
                print("🚩 URL didn't change - checking for error messages...")
                
                # Look for error messages
                error_indicators = [
                    'invalid', 'incorrect', 'wrong', 'error', 'failed', 'denied',
                    'bad credentials', 'authentication failed', 'login failed',
                    'username is invalid', 'password is invalid', 'try again'
                ]
                
                error_found = False
                for error in error_indicators:
                    if error.lower() in page_content.lower():
                        print(f"❌ LOGIN FAILED! Found error: '{error}'")
                        error_found = True
                        break
                
                if not error_found:
                    print("⚠️  URL didn't change but no clear error found - likely failed")
            
            # Final fallback check for obvious failures
            if not login_successful:
                obvious_failures = ['sign in', 'log in', 'login', 'enter password', 'authentication']
                for failure in obvious_failures:
                    if failure.lower() in page_content.lower():
                        print(f"❌ Still on login page - found: '{failure}'")
                        break
            
            # Keep browser open for a few seconds to see the result
            print("\n⏳ Keeping browser open for 5 seconds...")
            await asyncio.sleep(5)
            
        except Exception as e:
            print(f"❌ Error during login test: {str(e)}")
            
        finally:
            await browser.close()
            
    return login_successful

def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) < 3:
        print("Usage: python login_tester.py <username> <password> [url]")
        print("\nExample:")
        print("  python login_tester.py student Password123")
        print("  python login_tester.py myuser mypass https://example.com/login")
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]
    url = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Run the async login test
    success = asyncio.run(test_login(username, password, url))
    
    if success:
        print("\n🎉 LOGIN TEST COMPLETED SUCCESSFULLY!")
    else:
        print("\n💥 LOGIN TEST FAILED OR UNCLEAR")

if __name__ == "__main__":
    main() 