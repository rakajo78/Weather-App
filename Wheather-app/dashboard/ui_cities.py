import streamlit as st
import pandas as pd

def render_cities(main_col, right_col, latest_data, icon_url, base_img, city_data, get_icon_func, active_city, format_temp):
    c_temp_main, t_sym = format_temp(latest_data['suhu'])
    c_desc_main = latest_data['deskripsi_cuaca'].title()
    c_icon_name_main = icon_url.split('/')[-1]

    with main_col:
        for city_name, data in city_data.items():
            active_class = "active" if city_name == active_city else ""
            nav_icon = '<span class="material-symbols-rounded" style="font-size: 20px;">near_me</span>' if city_name == active_city else ""
            c_icon = get_icon_func(data['deskripsi_cuaca'])
            c_temp, _ = format_temp(data['suhu'])

            try: time_str = pd.to_datetime(data['waktu_pencatatan']).strftime('%H:%M')
            except: time_str = "Real-time"

            st.markdown(f"""
                <div class="city-card {active_class}">
                    <img src="{c_icon}" width="70" style="filter: drop-shadow(0px 8px 10px rgba(0,0,0,0.3));">
                    <div class="city-info">
                        <div class="city-name">{city_name} {nav_icon}</div>
                        <div class="city-time">{time_str}</div>
                    </div>
                    <div class="city-temp">{c_temp}{t_sym}</div>
                </div>
            """, unsafe_allow_html=True)

    with right_col:
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <div>
                    <h1 style="margin: 0; font-size: 40px; font-weight: bold; white-space: nowrap;">{active_city}</h1>
                    <p style="color: #939cb0; margin: 5px 0 0 0; font-size: 14px; white-space: nowrap;">Chance of rain: 0%</p>
                    <h1 style="margin: 20px 0 0 0; font-size: 64px; font-weight: bold;">{c_temp_main}{t_sym}</h1>
                </div>
                <img src="{icon_url}" style="width: 125px; filter: drop-shadow(0px 10px 15px rgba(0,0,0,0.4));">
            </div>
            <hr style="border: none; border-top: 1px solid #323d4e; margin: 30px 0;">
            <div class="section-title">TODAY'S FORECAST</div>
            <div class="hourly-flex" style="margin-top: 20px;">
                <div class="hourly-item"><div class="hourly-time">6:00 AM</div><img src="{base_img}/cloud.png" width="50"><div class="hourly-temp">{format_temp(latest_data['suhu'] - 3)[0]}{t_sym}</div></div>
                <div class="hourly-item"><div class="hourly-time">9:00 AM</div><img src="{base_img}/partly-cloudy-day.png" width="50"><div class="hourly-temp">{format_temp(latest_data['suhu'] - 1)[0]}{t_sym}</div></div>
                <div class="hourly-item" style="border: none;"><div class="hourly-time">12:00 PM</div><img src="{icon_url}" width="50"><div class="hourly-temp">{c_temp_main}{t_sym}</div></div>
            </div>
            <hr style="border: none; border-top: 1px solid #323d4e; margin: 30px 0;">
            <div class="section-title">3-DAY FORECAST</div>
        """, unsafe_allow_html=True)

        base_c = latest_data['suhu']
        days = [("Today", c_icon_name_main, c_desc_main, base_c + 1, base_c - 3), ("Tue", "sun.png", "Cerah", base_c + 2, base_c - 2), ("Wed", "partly-cloudy-day.png", "Berawan", base_c + 1, base_c - 3)]
        rows_html = ""
        for day, icon, desc, t_max_c, t_min_c in days:
            t_max, _ = format_temp(t_max_c)
            t_min, _ = format_temp(t_min_c)
            rows_html += f'<div class="forecast-row" style="padding: 15px 0;"><div class="f-day">{day}</div><div class="f-cond"><img src="{base_img}/{icon}" width="30"><span>{desc}</span></div><div class="f-temp">{t_max}{t_sym} <span class="f-temp-min">/{t_min}{t_sym}</span></div></div>'
        st.markdown(f'<div>{rows_html}</div>', unsafe_allow_html=True)
