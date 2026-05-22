import streamlit as st
import pandas as pd
import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine
import urllib.parse
from streamlit_autorefresh import st_autorefresh

# Import UI modular kita
from ui_home import render_home
from ui_detail import render_detail
from ui_cities import render_cities
from ui_map import render_map
from ui_settings import render_settings

st.set_page_config(page_title="Weather Analytics", page_icon="☁️", layout="wide", initial_sidebar_state="expanded")
st_autorefresh(interval=600000, limit=10000, key="data_refresh")
load_dotenv()

# --- INISIALISASI SESSION STATE PERMANEN ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'active_city' not in st.session_state: st.session_state.active_city = 'Surabaya'

# Variabel memori yang kebal dari "Widget Cleanup" Streamlit
if 'SAVED_temp' not in st.session_state: st.session_state.SAVED_temp = 'Celsius'
if 'SAVED_wind' not in st.session_state: st.session_state.SAVED_wind = 'km/h'
if 'SAVED_pressure' not in st.session_state: st.session_state.SAVED_pressure = 'mm'
if 'SAVED_precip' not in st.session_state: st.session_state.SAVED_precip = 'Milimeters'
if 'SAVED_dist' not in st.session_state: st.session_state.SAVED_dist = 'Kilometers'

# Session state untuk toggle settings
if 'SAVED_notifications' not in st.session_state: st.session_state.SAVED_notifications = True
if 'SAVED_12hour' not in st.session_state: st.session_state.SAVED_12hour = True
if 'SAVED_location' not in st.session_state: st.session_state.SAVED_location = True

def change_page(page_name): st.session_state.page = page_name
def go_to_detail(): st.session_state.page = 'detail'
def go_to_home(): st.session_state.page = 'home'

# --- FUNGSI KONVERSI MATEMATIKA (Merujuk ke Memori Permanen) ---
def format_temp(celsius_temp):
    if st.session_state.SAVED_temp == 'Fahrenheit':
        return int((celsius_temp * 9/5) + 32), "°F"
    return int(celsius_temp), "°"

def format_wind(kmh_wind):
    if st.session_state.SAVED_wind == 'm/s':
        return f"{round(kmh_wind / 3.6, 2)} m/s"
    elif st.session_state.SAVED_wind == 'Knots':
        return f"{round(kmh_wind / 1.852, 2)} Knots"
    return f"{kmh_wind} km/h"

# --- CUSTOM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,1,0');
    html, body, [class*="css"]  { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stApp { background-color: #0b131e; color: white; }
    header[data-testid="stHeader"] { background-color: transparent; }
    .block-container { padding-top: 2rem; padding-bottom: 1rem; max-width: 95%; }
    [data-testid="stSidebar"] { background-color: #1a2230 !important; }
    div[data-baseweb="select"] > div { background-color: #202b3b; border-radius: 10px; border: none; color: white; cursor: pointer; }
    div.stButton > button { border-radius: 20px; border: none; transition: 0.3s; white-space: nowrap; }
    div.stButton > button[kind="primary"] { background-color: #0095ff; color: white; padding: 0px 20px; font-weight: bold; font-size: 14px; height: 35px; }
    div.stButton > button[kind="secondary"] { background-color: #202b3b; color: #939cb0; height: 40px; width: 100%; }
    div.stButton > button[kind="secondary"]:hover { background-color: #323d4e; color: white; }

    /* Settings widget styling */
    div.stRadio, div.stToggle { background-color: #202b3b; padding: 15px 25px; border-radius: 15px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
    div.stRadio > label, div.stToggle > label { color: #939cb0; font-size: 12px !important; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px; }
    div[role="radiogroup"] { background: #0b131e; border-radius: 10px; overflow: hidden; display: flex; padding: 5px; }

    /* Weather cards */
    .weather-card { background-color: #202b3b; border-radius: 20px; padding: 25px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
    .card-title { font-size: 38px; font-weight: bold; margin: 0; }
    .card-subtitle { color: #939cb0; font-size: 14px; margin-top: 5px; }
    .big-temp { font-size: 72px; font-weight: bold; line-height: 1.2; margin-top: 30px; }
    .section-title { font-size: 12px; color: #939cb0; text-transform: uppercase; font-weight: bold; margin-bottom: 15px; letter-spacing: 1px; }
    .main-card-flex { display: flex; justify-content: space-between; align-items: center; }

    /* Hourly forecast */
    .hourly-flex { display: flex; justify-content: space-between; text-align: center; }
    .hourly-item { flex: 1; border-right: 1px solid #323d4e; padding: 10px 0; }
    .hourly-item:last-child { border-right: none; }
    .hourly-time { color: #939cb0; font-size: 13px; font-weight: 600; margin-bottom: 10px; }
    .hourly-temp { font-size: 18px; font-weight: bold; margin-top: 10px; }

    /* Air conditions */
    .air-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 25px; }
    .air-item { display: flex; align-items: flex-start; gap: 15px; }
    .air-icon { font-size: 24px !important; color: #939cb0; margin-top: 2px; }
    .air-label { color: #939cb0; font-size: 14px; }
    .air-value { font-size: 26px; font-weight: bold; margin-top: 2px; }

    /* 7-day forecast */
    .forecast-row { display: flex; justify-content: space-between; align-items: center; padding: 15px 0; border-bottom: 1px solid #323d4e; }
    .forecast-row:last-child { border-bottom: none; }
    .f-day { color: #939cb0; width: 50px; font-size: 14px; }
    .f-cond { display: flex; align-items: center; gap: 10px; flex-grow: 1; font-size: 14px; font-weight: bold; }
    .f-temp { text-align: right; font-size: 14px; }
    .f-temp-min { color: #939cb0; }

    /* Detail metrics */
    .detail-metric-title { color: #939cb0; font-size: 13px; text-transform: uppercase; font-weight: bold; display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
    .detail-metric-value { font-size: 32px; font-weight: bold; }

    /* City cards */
    .city-card { background-color: #202b3b; border-radius: 25px; padding: 25px 35px; margin-bottom: 25px; display: flex; align-items: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border: 2px solid transparent; transition: 0.3s; }
    .city-card.active { border: 2px solid #0095ff; }
    .city-info { flex-grow: 1; margin-left: 30px; }
    .city-name { font-size: 32px; font-weight: bold; margin: 0; display: flex; align-items: center; gap: 10px; }
    .city-time { color: #939cb0; font-size: 16px; margin-top: 5px; }
    .city-temp { font-size: 48px; font-weight: bold; }

    /* Mini city cards (map sidebar) */
    .mini-city-card { background-color: #202b3b; border-radius: 15px; padding: 15px 20px; margin-bottom: 15px; display: flex; align-items: center; border-left: 4px solid transparent; transition: 0.3s; }
    .mini-city-info { flex-grow: 1; margin-left: 15px; }
    .mini-city-name { font-size: 18px; font-weight: bold; }
    .mini-city-time { color: #939cb0; font-size: 12px; }
    .mini-city-temp { font-size: 28px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- FUNGSI DATA DENGAN CACHE ---
@st.cache_data(ttl=300)
def get_data():
    db_user = os.getenv("DB_USER")
    db_pass_raw = os.getenv("DB_PASS") or ""
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_pass_encoded = urllib.parse.quote_plus(db_pass_raw)
    db_uri = f"postgresql+psycopg2://{db_user}:{db_pass_encoded}@{db_host}:{db_port}/{db_name}"
    try:
        engine = create_engine(db_uri)
        query = "SELECT DISTINCT ON (nama_kota) * FROM data_cuaca ORDER BY nama_kota, waktu_pencatatan DESC"
        df = pd.read_sql(query, engine)
        if not df.empty: return df.set_index('nama_kota').to_dict('index')
        return {}
    except Exception as e: return {}

def refresh_weather_data():
    """Panggil pipeline extract langsung via subprocess, lalu clear cache"""
    import subprocess
    try:
        extract_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline', 'extract.py')
        subprocess.run([sys.executable, extract_script], check=True, timeout=60)
    except Exception as e:
        st.toast(f"⚠️ Gagal refresh dari API: {e}", icon="⚠️")

    # Clear cache agar data terbaru ter-load
    get_data.clear()

def get_3d_weather_icon(desc):
    desc = desc.lower()
    base_url = "https://img.icons8.com/3d-fluency/250"
    if any(k in desc for k in ["hujan", "gerimis", "rintik", "petir", "badai", "storm", "rain"]): return f"{base_url}/storm.png"
    elif any(k in desc for k in ["cerah", "langit cerah", "clear", "sunny"]): return f"{base_url}/sun.png"
    elif any(k in desc for k in ["sedikit berawan", "awan tersebar", "partly"]): return f"{base_url}/partly-cloudy-day.png"
    elif any(k in desc for k in ["mendung", "awan tebal", "awan pecah", "berawan", "kabut", "overcast"]): return f"{base_url}/cloud.png"
    return f"{base_url}/partly-cloudy-day.png"

with st.sidebar:
    st.markdown("<div style='text-align: center; margin-bottom: 30px; color: #0095ff;'><span class='material-symbols-rounded' style='font-size: 50px;'>routine</span><br><b style='color: white;'>Weather Dashboard</b></div>", unsafe_allow_html=True)
    st.button("Weather", icon=":material/partly_cloudy_day:", use_container_width=True, on_click=change_page, args=('home',))
    st.button("Cities", icon=":material/format_list_bulleted:", use_container_width=True, on_click=change_page, args=('cities',))
    st.button("Map", icon=":material/map:", use_container_width=True, on_click=change_page, args=('map',))
    st.button("Settings", icon=":material/tune:", use_container_width=True, on_click=change_page, args=('settings',))

city_data = get_data()
if not city_data: city_data = {'Surabaya': {'deskripsi_cuaca': 'sedikit berawan', 'suhu': 28, 'terasa_seperti': 34, 'kecepatan_angin': 2.06, 'kelembapan': 70}}

city_names = list(city_data.keys())
if st.session_state.active_city not in city_names: st.session_state.active_city = city_names[0] if city_names else 'Surabaya'
active_city = str(st.session_state.active_city)
latest_data = city_data[active_city]
base_img = "https://img.icons8.com/3d-fluency/250"
icon_url = get_3d_weather_icon(latest_data['deskripsi_cuaca'])

# --- TOP BAR: City Selector + Refresh Button + Close Button ---
top_c1, top_c2, top_c3 = st.columns([9, 1, 1], gap="small")
with top_c1:
    selected_city = st.selectbox("Search", options=city_names, index=city_names.index(active_city) if active_city in city_names else 0, label_visibility="collapsed")
    if selected_city != active_city:
        st.session_state.active_city = selected_city
        st.rerun()

with top_c2:
    if st.button("⟳", key="refresh_btn", help="Refresh data cuaca dari API", use_container_width=True):
        with st.spinner("🔄 Fetching data terbaru..."):
            refresh_weather_data()
        st.toast("✅ Data berhasil diperbarui!", icon="✅")
        st.rerun()

with top_c3:
    if st.session_state.page == 'detail': st.button("Close", icon=":material/close:", on_click=go_to_home, use_container_width=True, help="Kembali ke Dashboard")
st.write("")

if st.session_state.page in ['cities', 'map', 'settings']: main_col, right_col = st.columns([1.7, 1.2], gap="large")
else: main_col, right_col = st.columns([2.2, 1], gap="medium")

# --- ROUTING UI ---
if st.session_state.page == 'home': render_home(main_col, right_col, latest_data, icon_url, base_img, go_to_detail, active_city, format_temp, format_wind)
elif st.session_state.page == 'detail': render_detail(main_col, right_col, latest_data, icon_url, base_img, active_city, format_temp, format_wind)
elif st.session_state.page == 'cities': render_cities(main_col, right_col, latest_data, icon_url, base_img, city_data, get_3d_weather_icon, active_city, format_temp)
elif st.session_state.page == 'map': render_map(main_col, right_col, latest_data, icon_url, base_img, city_data, get_3d_weather_icon, active_city, format_temp)
elif st.session_state.page == 'settings': render_settings(main_col, right_col)

if not city_data: st.warning("Menampilkan data visualisasi sementara. Pastikan scheduler berjalan.")
