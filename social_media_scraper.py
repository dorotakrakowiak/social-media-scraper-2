import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# Ustawienia Selenium
options = Options()
options.add_argument('--headless')  # Uruchamianie w tle
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Inicjalizacja przeglądarki
browser = webdriver.Chrome(options=options)

# Funkcja do pobierania danych z Instagrama
def get_instagram_data(url):
    browser.get(url)
    time.sleep(5)
    try:
        followers = browser.find_element(By.XPATH, "//span[contains(text(), 'followers')]").text
        posts = browser.find_element(By.XPATH, "//span[contains(text(), 'posts')]").text
        return {'Platform': 'Instagram', 'URL': url, 'Followers': followers, 'Posts': posts}
    except Exception as e:
        st.error(f'Error fetching Instagram data: {e}')
        return None

# Funkcja do pobierania danych z Facebooka
def get_facebook_data(url):
    browser.get(url)
    time.sleep(5)
    try:
        likes = browser.find_element(By.XPATH, "//div[contains(text(), 'likes')]").text
        follows = browser.find_element(By.XPATH, "//div[contains(text(), 'follows')]").text
        return {'Platform': 'Facebook', 'URL': url, 'Likes': likes, 'Follows': follows}
    except Exception as e:
        st.error(f'Error fetching Facebook data: {e}')
        return None

# Funkcja do pobierania danych z TikToka
def get_tiktok_data(url):
    browser.get(url)
    time.sleep(5)
    try:
        followers = browser.find_element(By.XPATH, "//strong[contains(text(), 'Followers')]").text
        likes = browser.find_element(By.XPATH, "//strong[contains(text(), 'Likes')]").text
        return {'Platform': 'TikTok', 'URL': url, 'Followers': followers, 'Likes': likes}
    except Exception as e:
        st.error(f'Error fetching TikTok data: {e}')
        return None

# Interfejs Streamlit
st.title('Social Media Data Scraper')
urls = st.text_area('Wprowadź linki do profili (po jednym w linii)').split('\n')

if st.button('Generuj raport'):
    data = []
    for url in urls:
        url = url.strip()
        if 'instagram.com' in url:
            result = get_instagram_data(url)
        elif 'facebook.com' in url:
            result = get_facebook_data(url)
        elif 'tiktok.com' in url:
            result = get_tiktok_data(url)
        if result:
            data.append(result)

    browser.quit()

    if data:
        df = pd.DataFrame(data)
        st.write(df)
        df.to_csv('social_media_report.csv', index=False)
        st.success('Raport zapisany jako social_media_report.csv')
    else:
        st.warning('Brak danych do zapisania.')
