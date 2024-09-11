# Chrome-Saved-Passwords-Extractor

## Chrome Password Extractor

This tool extracts saved passwords from Google Chrome's local files and decrypts them. It grabs the username, password, URLs, and other metadata, then saves the data to a text file.

## How it works
  - Accesses Chrome's encrypted login database
  - Decrypts passwords using Windows DPAPI
  - Extracts detailed login information including URLs, usernames, and passwords
  - Saves extracted data to a text file
    
## Requirements
  - Python 3.x
  - Google Chrome browser installed
  - Windows operating system
    
## Installation
  1. Clone this repository
  2. Install the required packages      

## Usage
  1. Ensure Chrome is not running or move the Local State and Login Data to a different place since the database will be locked if Chrome is 
     running
  2. Update the `login_data_path` and `local_state_path` in the script to match your Chrome profile location
  3. Run the script: `python ChromeLogin.py`
  4. Find the extracted login data in the `login_data.txt` file.

Note: Always respect privacy and adhere to legal guidelines.
