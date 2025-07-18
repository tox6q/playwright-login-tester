#!/usr/bin/env python3
"""
Site-specific scraper for localhost:3000 React portal
This script runs after successful authentication via login_tester.py
"""

import asyncio
import os
from datetime import datetime

async def run_scraper(page, browser):
    """
    Main scraper function - receives authenticated page and browser from login_tester.py
    Specific for localhost:3000 File Portal Dashboard structure
    """
    print("\n🎯 Starting localhost:3000 File Portal scraping...")
    
    try:
        # We should already be on the dashboard after successful 2FA
        current_url = page.url
        print(f"📍 Current location: {current_url}")
        
        # Wait for dashboard to fully load
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)
        
        # Create downloads directory if it doesn't exist
        downloads_dir = "downloads"
        if not os.path.exists(downloads_dir):
            os.makedirs(downloads_dir)
            print(f"📁 Created downloads directory: {downloads_dir}")
        
        # Step 1: Navigate to Files section
        print("\n🔍 Looking for 'Open Files' button on dashboard...")
        
        # Look for the "Open Files" button
        open_files_selectors = [
            'button:has-text("Open Files")',
            'a:has-text("Open Files")',
            '[class*="files"] button',
            'button:has-text("Files")',
        ]
        
        files_button_found = False
        for selector in open_files_selectors:
            try:
                files_button = page.locator(selector).first
                if await files_button.count() > 0:
                    print(f"✅ Found 'Open Files' button: {selector}")
                    await files_button.click()
                    print("🚀 Clicked 'Open Files' button")
                    files_button_found = True
                    break
            except Exception as e:
                continue
        
        if not files_button_found:
            print("❌ Could not find 'Open Files' button - trying alternative navigation...")
            # Try clicking on Files section directly
            files_section = page.locator(':has-text("Files")').first
            await files_section.click()
        
        # Wait for files page to load
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(3)
        
        print(f"📍 Navigated to: {page.url}")
        
        # Step 2: Scan the files table
        print("\n🔍 Scanning files table...")
        
        # Target files we want to download
        target_files = ["Project_Report_2024.pdf", "Meeting_Notes.docx"]
        downloads_found = 0
        
        # Look for table rows containing files
        print("🔍 Looking for file table rows...")
        
        # Try different table selectors
        table_selectors = [
            'table tr',           # Standard table rows
            '[role="table"] tr',  # ARIA table
            '.table tr',          # CSS class table
            'tbody tr',           # Table body rows
        ]
        
        for table_selector in table_selectors:
            try:
                rows = await page.locator(table_selector).all()
                if len(rows) > 1:  # More than header row
                    print(f"✅ Found table with {len(rows)} rows using: {table_selector}")
                    
                    for row in rows:
                        try:
                            row_text = await row.text_content()
                            row_text = row_text.strip() if row_text else ""
                            
                            # Check if this row contains one of our target files
                            for target_file in target_files:
                                if target_file in row_text:
                                    print(f"🎯 Found target file in row: {target_file}")
                                    
                                    # Look for download button in this row
                                    download_button = row.locator('button:has-text("Download"), a:has-text("Download"), [class*="download"]').first
                                    
                                    if await download_button.count() > 0:
                                        print(f"🔗 Clicking download for: {target_file}")
                                        
                                        # Set up download handling
                                        async with page.expect_download() as download_info:
                                            await download_button.click()
                                        
                                        # Handle the download
                                        download = await download_info.value
                                        filename = download.suggested_filename or target_file
                                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                        safe_filename = f"{timestamp}_{filename}"
                                        
                                        download_path = os.path.join(downloads_dir, safe_filename)
                                        await download.save_as(download_path)
                                        
                                        print(f"💾 Successfully downloaded: {safe_filename}")
                                        downloads_found += 1
                                        
                                        # Remove from target list so we don't download duplicates
                                        target_files.remove(target_file)
                                        
                                        # Small delay between downloads
                                        await asyncio.sleep(2)
                                        break
                                    else:
                                        print(f"⚠️  No download button found for: {target_file}")
                        
                        except Exception as e:
                            print(f"⚠️  Error processing row: {str(e)}")
                            continue
                    
                    break  # Found working table selector, no need to try others
                    
            except Exception as e:
                print(f"⚠️  Error with table selector '{table_selector}': {str(e)}")
                continue
        
        # If we didn't find the files in table, try alternative download methods
        if downloads_found == 0:
            print("\n🔍 Table method didn't work, trying alternative download detection...")
            
            # Look for any download buttons on the page
            download_buttons = await page.locator('button:has-text("Download"), a:has-text("Download")').all()
            
            if download_buttons:
                print(f"✅ Found {len(download_buttons)} download buttons")
                
                for i, button in enumerate(download_buttons):
                    try:
                        button_text = await button.text_content()
                        print(f"🔗 Clicking download button {i+1}: '{button_text}'")
                        
                        async with page.expect_download() as download_info:
                            await button.click()
                        
                        download = await download_info.value
                        filename = download.suggested_filename
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        safe_filename = f"{timestamp}_{filename}"
                        
                        download_path = os.path.join(downloads_dir, safe_filename)
                        await download.save_as(download_path)
                        
                        print(f"💾 Downloaded: {safe_filename}")
                        downloads_found += 1
                        
                        await asyncio.sleep(2)
                        
                    except Exception as e:
                        print(f"⚠️  Failed to download from button {i+1}: {str(e)}")
                        continue
        
        # Final summary
        print(f"\n📊 Scraping Summary:")
        print(f"   💾 Total downloads: {downloads_found}")
        print(f"   📁 Saved to: {downloads_dir}/")
        
        if downloads_found > 0:
            print("🎉 Scraping completed successfully!")
        else:
            print("⚠️  No downloads found - check if the site structure has changed")
        
        # Keep browser open for a few seconds to see results
        print("\n⏳ Keeping browser open for 10 seconds...")
        await asyncio.sleep(10)
        
    except Exception as e:
        print(f"❌ Error during scraping: {str(e)}")
        
    finally:
        print("🔚 Closing browser...")
        await browser.close()

async def scan_page_for_downloads(page, downloads_dir):
    """Helper function to scan current page for downloads"""
    print(f"🔍 Scanning current page: {page.url}")
    downloads_count = 0
    
    download_selectors = [
        'a[href*=".pdf"]', 'a[href*=".doc"]', 'a[href*=".xlsx"]',
        'button:has-text("Download")', 'a:has-text("Download")'
    ]
    
    for selector in download_selectors:
        try:
            elements = await page.locator(selector).all()
            for element in elements:
                try:
                    async with page.expect_download() as download_info:
                        await element.click()
                    
                    download = await download_info.value
                    filename = download.suggested_filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    safe_filename = f"{timestamp}_{filename}"
                    
                    download_path = os.path.join(downloads_dir, safe_filename)
                    await download.save_as(download_path)
                    
                    print(f"💾 Downloaded: {safe_filename}")
                    downloads_count += 1
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    continue
                    
        except Exception as e:
            continue
    
    return downloads_count 