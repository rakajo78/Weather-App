"""
Pipeline ETL: Extract weather data from OpenWeatherMap API,
transform it, and load it into PostgreSQL.
"""
import os
import sys
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine
import urllib.parse

load_dotenv()

# Database & API Configuration
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS") or ""
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
API_KEY = os.getenv("OWM_API_KEY")

db_pass_encoded = urllib.parse.quote_plus(DB_PASS)
DB_URI = f"postgresql+psycopg2://{DB_USER}:{db_pass_encoded}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Target cities: API name -> Display name
TARGET_CITIES = {
    "Jakarta": "Jakarta",
    "Bandung": "Bandung",
    "Yogyakarta": "Yogyakarta",
    "Surabaya": "Surabaya",
    "Denpasar": "Bali",
}


def extract_and_load():
    """Extract weather data from OpenWeatherMap, transform, and load to DB."""
    engine = create_engine(DB_URI)
    all_data = []

    # 1. Extract
    for city_api, city_ui in TARGET_CITIES.items():
        url = (
            f"http://api.openweathermap.org/data/2.5/weather"
            f"?q={city_api},ID&appid={API_KEY}&units=metric&lang=id"
        )
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # 2. Transform
            weather_info = {
                "nama_kota": city_ui,
                "waktu_pencatatan": datetime.now(),
                "deskripsi_cuaca": data["weather"][0]["description"],
                "suhu": data["main"]["temp"],
                "terasa_seperti": data["main"]["feels_like"],
                "kelembapan": data["main"]["humidity"],
                "kecepatan_angin": round(data["wind"]["speed"] * 3.6, 2),
            }
            all_data.append(weather_info)
            print(f"  [OK] {city_ui}")

        except Exception as e:
            print(f"  [FAIL] {city_ui}: {e}")

    # 3. Load
    if all_data:
        df = pd.DataFrame(all_data)
        try:
            df.to_sql("data_cuaca", engine, if_exists="append", index=False)
            print(f"  -> {len(df)} rows inserted into 'data_cuaca'")
        except Exception as e:
            print(f"  [FAIL] DB insert: {e}")


if __name__ == "__main__":
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting weather pipeline...")
    extract_and_load()
    print("Pipeline complete.\n")
