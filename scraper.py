import time
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
import datetime
import glob
import pandas as pd
import re


def apply_main(driver):
    try:
        print("[*] Opening auction status filter...")
        click_buttons = WebDriverWait(driver, 30).until(
            ec.presence_of_all_elements_located((By.XPATH, "//button[@class='btn btn-filter dropdown-toggle']"))
        )
        if click_buttons and len(click_buttons) >= 5:
            driver.execute_script('arguments[0].click();', click_buttons[4])
        else:
            print("[!] Filter dropdown not found or insufficient buttons.")

        try:
            print("[*] Applying beds filter...")
            beds = WebDriverWait(driver, 20).until(
                ec.presence_of_element_located((By.XPATH, "//div[@class='count-container bedsFilter']"))
            )
            lb = beds.find_elements(By.TAG_NAME, "label")
            if len(lb) > 4:
                driver.execute_script('arguments[0].click();', lb[4])
            else:
                print("[!] Not enough bed filter options found.")
        except Exception as e:
            print(f"[✗] Beds filter error: {e}")

        try:
            print("[*] Applying baths filter...")
            baths = WebDriverWait(driver, 20).until(
                ec.presence_of_element_located((By.XPATH, "//div[@class='count-container bathsFilter']"))
            )
            lb = baths.find_elements(By.TAG_NAME, "label")
            if len(lb) > 3:
                driver.execute_script('arguments[0].click();', lb[3])
            else:
                print("[!] Not enough bath filter options found.")
        except Exception as e:
            print(f"[✗] Baths filter error: {e}")

        try:
            print("[*] Setting minimum square footage...")
            inp = WebDriverWait(driver, 20).until(
                ec.presence_of_element_located((By.XPATH, "//input[@name='MinSquareFootage']"))
            )
            driver.execute_script('arguments[0].scrollIntoView(true);', inp)
            inp.clear()
            inp.send_keys("1000")
            inp.send_keys(Keys.ENTER)
            time.sleep(1)
        except Exception as e:
            print(f"[✗] Square footage filter error: {e}")

        try:
            print("[*] Setting auction status filter...")
            click_buttons = WebDriverWait(driver, 30).until(
                ec.presence_of_all_elements_located((By.XPATH, "//button[@class='btn btn-filter dropdown-toggle']"))
            )
            if len(click_buttons) >= 3:
                driver.execute_script('arguments[0].click(true);', click_buttons[2])
            else:
                print("[!] Not enough dropdowns to open auction status filter.")

            checkboxes = driver.find_elements(By.CSS_SELECTOR,
                                              "div.filter-container.auctionStatusFilters label[class='custom-check']")
            if len(checkboxes) >= 2:
                driver.execute_script("arguments[0].click();", checkboxes[0])
                time.sleep(1)
                driver.execute_script("arguments[0].click();", checkboxes[-1])
                time.sleep(1)
            else:
                print("[!] Not enough auction status checkboxes found.")
        except Exception as e:
            print(f"[✗] Auction status filter error: {e}")

        try:
            print("[*] Selecting asset type filter...")
            click_buttons = WebDriverWait(driver, 30).until(
                ec.presence_of_all_elements_located((By.XPATH, "//button[@class='btn btn-filter dropdown-toggle']"))
            )
            if click_buttons:
                driver.execute_script('arguments[0].click();', click_buttons[0])

            elements = driver.find_elements(By.CSS_SELECTOR,
                                            "div.filter-container.assetTypeFilters ul.dropdown-menu label.custom-check")
            if elements and len(elements) >= 2:
                driver.execute_script('arguments[0].click();', elements[-2])
            else:
                print("[!] Not enough asset type filters found.")
        except Exception as e:
            print(f"[✗] Asset type filter error: {e}")

        print("[✓] All filters applied successfully.")

    except Exception as e:
        print(f"[✗] Error in apply_main: {e}")


def change_location(driver, l):
    loc = WebDriverWait(driver, 40).until(ec.presence_of_element_located((By.XPATH, "//input[@id='location']")))
    if loc:
        try:
            time.sleep(2)
            d = WebDriverWait(driver, 3).until(ec.presence_of_element_located((By.XPATH, "//span[@class='close-icon-wrapper']")))
            if d:
                driver.execute_script('arguments[0].click(true);', d)
        except:
            pass
        loc.clear()
        loc.send_keys(l)
        # loc.send_keys(Keys.ENTER)
        i_tag = WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.XPATH, "//i[@id='submit-search']")))
        if i_tag:
            driver.execute_script('arguments[0].click(true);', i_tag)
        time.sleep(10)


def check(driver):
    cc = WebDriverWait(driver, 40).until(ec.presence_of_all_elements_located((By.XPATH, "//div[@class='srp-property-card']")))
    if cc:
        print('Properties are now loaded, downloading the document')
    else:
        print('properties not loaded in the dedicated 40 seconds')


def click(driver):
    c = WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.XPATH, "//a[@class='export-link']")))
    if c:
        driver.execute_script('arguments[0].click(true);', c)
        print('Clicked the download button')
        try:
            g = WebDriverWait(driver, 3).until(ec.presence_of_element_located((By.XPATH, "//button[@class='download-prop-link btn btn-default']")))
            if g:
                driver.execute_script('arguments[0].click(true);', g)
        except:
            pass
    else:
        print('Download button not available')
    time.sleep(5)


def states():
    states = [
        "Alabama", "Arizona", "California", "Colorado", "Connecticut", "Delaware",
        "Florida", "Georgia", "Idaho", "Iowa", "Kansas", "Maine", "Maryland",
        "Massachusetts", "Minnesota", "Mississippi", "Montana", "New Hampshire",
        "New Jersey", "New York", "North Carolina", "Ohio", "Oregon",
        "Pennsylvania", "Rhode Island", "South Carolina", "Tennessee", "Texas",
        "Utah", "Vermont", "Virginia", "Washington", "Wisconsin", "Wyoming"
    ]
    return states


def download_with_timestamp(driver, state, download_dir):
    try:
        print(f"[*] Starting download for state: {state}")
        change_location(driver, state)
        check(driver)
        click(driver)
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        time.sleep(20)

        downloaded_files = glob.glob(os.path.join(download_dir, "*.xlsx"))
        if not downloaded_files:
            print(f"[!] No Excel file downloaded for {state}")
            return

        latest_file = max(downloaded_files, key=os.path.getctime)

        new_filename = os.path.join(download_dir, f"{state}_{timestamp}.xlsx")
        os.rename(latest_file, new_filename)

        print(f"[✓] Downloaded and renamed: {new_filename}")

    except Exception as e:
        print(f"[✗] Failed for {state}: {e}")


def merge_multiple_excels(input_folder, output_csv='merged_output.csv'):
    merged_data = []

    for filename in os.listdir(input_folder):
        if filename.endswith('.xlsx'):
            file_path = os.path.join(input_folder, filename)

            match = re.match(r"(.+?)_(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})", filename)
            if not match:
                print(f"Skipping file {filename} — incorrect format.")
                continue
            state, timestamp = match.groups()
            timestamp = timestamp.replace('_', '  ')

            df = pd.read_excel(file_path, skiprows=1)

            df.insert(0, 'STATE', state)
            df.insert(1, 'Timestamp', timestamp)

            merged_data.append(df)

    if not merged_data:
        print("No valid Excel files found.")
        return

    final_df = pd.concat(merged_data, ignore_index=True)
    final_df.drop_duplicates(subset="ID", keep="first")
    final_df.to_csv(output_csv, index=False)
    print(f"Merged CSV saved as '{output_csv}'")
    print('Now going to delete files.')
    excel_files = glob.glob('downloads/*.xlsx')
    for file in excel_files:
        try:
            os.remove(file)
            print(f"Deleted: {file}")
        except Exception as e:
            print(f"Error deleting {file}: {e}")


def main():
    st = states()
    download_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(download_dir, exist_ok=True)
    for s in st:
        chrome_options = webdriver.ChromeOptions()
        chrome_prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", chrome_prefs)
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        dri = webdriver.Chrome(options=chrome_options)
        dri.get('https://www.xome.com/auctions')
        download_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(download_dir, exist_ok=True)
        apply_main(dri)
        download_with_timestamp(dri, s, download_dir)
        dri.quit()

    merge_multiple_excels("downloads")


if __name__ == "__main__":
    main()
