import asyncio
import json
from pathlib import Path
import requests
from playwright.async_api import async_playwright
import pandas as pd
import time
import re

# Ścieżka do pliku z cookies
cookies_file = "cookies.json"
key_file = "key.txt"

################################### Dane logowania #######################################

login = 'LOGIN_DO_EDUVULCAN'
haselko = 'HASŁO_DO_EDUVULCAN'

dataOd='2024-09-01T22:00:00.000Z'
dataDo='2024-09-08T21:59:59.999Z'

################################### Dane logowania #######################################

# URL-e do logowania, tablicy i API planu lekcji
login_url = 'https://eduvulcan.pl/logowanie'

def gen_link(accklucz, linkname):
    if linkname == 'plan_lekcji_url':
        return f'https://uczen.eduvulcan.pl/powiatpoznanski/api/79ad9207-6132-427d-bbfa-62a7cff7735f?key={accklucz}&dataOd={dataOd}&dataDo={dataDo}&zakresDanych=2'
    elif linkname == 'dashboard_url':
        return f'https://uczen.eduvulcan.pl/powiatpoznanski/App/{accklucz}/tablica'

def load_cookies(path):
    if Path(path).exists():
        with open(path, "r") as file:
            return json.load(file)
    return None

def load_key(path):
    if Path(path).exists():
        with open(path, "r") as file:
            return file.read()
    return None

def save_cookies(cookies, path):
    with open(path, "w") as file:
        json.dump(cookies, file)

def save_key(key, path):
    with open(path, "w") as file:
        file.write(key)

def get_headers(cookies):
    cookies_str = '; '.join([f'{cookie["name"]}={cookie["value"]}' for cookie in cookies])
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0',
        'Referer': gen_link(load_key(key_file), 'dashboard_url'),
        'Cookie': cookies_str
    }
    return headers

def check_existing_cookies(cookies):
    headers = get_headers(cookies)
    response = requests.get(gen_link(load_key(key_file), 'plan_lekcji_url'), headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            pass
    return None

async def login_and_fetch_schedule(playwright):
    browser = await playwright.firefox.launch(headless=False)
    context = await browser.new_context()

    # Przeprowadź logowanie, jeśli cookies są nieważne
    page = await context.new_page()
    await page.goto(login_url)
    iframe = page.frame_locator('iframe#respect-privacy-frame.cookie-frame')
    await iframe.locator('button#save-default-button.base-button.button-primary.button-wide').click()
    await page.fill('input[name="Alias"]', login)
    await page.click('button#btNext')
    await page.fill('input[name="Password"]', haselko)
    await page.click('button#btLogOn')

    await page.wait_for_url("https://eduvulcan.pl/")
    await page.click("a.connected-account.access-row.flex-grow-1")
    
    await page.wait_for_url("**/tablica")

    try:
        cookies = await context.cookies()
        save_cookies(cookies, cookies_file)
        match = re.search(r'/([A-Za-z0-9]+)\/tablica', page.url)
        save_key(match.group(1), key_file)
        print("Klucz: " + match.group(1))
        print("Zalogowano pomyślnie!")
    except Exception as e:
        print("Logowanie nie powiodło się.")
        raise Exception(e)

    # Pobierz plan lekcji z API
    response = await page.request.get(gen_link(load_key(key_file), 'plan_lekcji_url'), headers=get_headers(cookies))
    data = await response.json()

    await browser.close()
    return data


def process_schedule(data):
    if isinstance(data, list):
        df = pd.DataFrame(data)
        df['data'] = pd.to_datetime(df['data'])
        df_sorted = df.sort_values(by='data')
        grouped = df_sorted.groupby(df_sorted['data'].dt.date)

        for date, group in grouped:
            print(f"\nPlan lekcji na {date}:")
            for _, row in group.iterrows():
                start_time = pd.to_datetime(row['godzinaOd']).strftime('%H:%M')
                end_time = pd.to_datetime(row['godzinaDo']).strftime('%H:%M')
                subject = row['przedmiot']
                print(f"  {start_time} - {end_time}: {subject}")

        df_sorted.to_csv('plan_lekcji.csv', index=False, columns=['data', 'godzinaOd', 'godzinaDo', 'przedmiot', 'sala'])
    else:
        print("Nieoczekiwany format odpowiedzi z API:", type(data))


async def main():
    cookies = load_cookies(cookies_file)

    if cookies:
        data = check_existing_cookies(cookies)
        if data:
            print("Użyto zapisanych ciasteczek.")
            process_schedule(data)
            return
        else:
            print("Ciasteczka wygasły lub są nieważne. Logowanie...")

    async with async_playwright() as playwright:
        data = await login_and_fetch_schedule(playwright)
        process_schedule(data)

asyncio.run(main())
