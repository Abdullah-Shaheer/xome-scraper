# 🏡 Xome Property Data Scraper

A Python-based scraper that automates the process of applying filters on [Xome.com](https://www.xome.com), downloading filtered property data files for various locations, and merging them into a single cleaned CSV file.

---

## 📌 Overview

This script uses **Selenium WebDriver** to:

1. Open [xome.com](https://www.xome.com)
2. Apply multiple filters such as:
   - 🛏 Beds
   - 🛁 Baths
   - 📐 Minimum square footage
   - 🏷️ Asset type
   - 🔄 Auction status
3. Apply a search location
4. Automatically trigger a download of the filtered data
5. Repeat for multiple locations
6. Merge all downloaded `.csv` files into a single **consolidated CSV**
7. Clean up by **deleting all individual CSV files** after merging

---

## ⚙️ Features

- ✅ Automated UI interaction via Selenium
- ✅ Dynamic filter application
- ✅ Download property data from the "Download Results" button
- ✅ Works with multiple locations
- ✅ Merges downloaded files into one
- ✅ Automatically removes temporary files from `downloads/`

---

## 🧰 Tech Stack

- Python 3.7+
- Selenium WebDriver
- Pandas

---

## 📦 Installation

1. Clone the repo:
```bash
git clone https://github.com/yourusername/xome-scraper.git
cd xome-scraper
```
2. Install required packages:
```bash
pip install selenium pandas glob re
```
3. Make sure chromedriver is installed and matches your Chrome version. Place it in your system PATH or project directory.

## 🧠 How it works
1. Visit xome.com
2. Open dropdown filters using XPath/CSS selectors
3. Apply the following filters:
   - Beds ≥ 4
   - Baths ≥ 3
   - Minimum square footage = 1000
   - Asset type = Residential
   - Auction Status = All available
4. Enter search location
5. Click the "Download Results" button
6. Repeat for other locations
7. Read each downloaded CSV into pandas
8. Concatenate all into `merged_output.csv`
9. Delete original files from downloads/

## Thank you so much!




