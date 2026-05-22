import streamlit as st

def render_home(main_col, right_col, latest_data, icon_url, base_img, go_to_detail_callback, active_city, format_temp, format_wind):
    # TERAPKAN KONVERSI CELSIUS KE FAHRENHEIT
    c_temp, t_sym = format_temp(latest_data['suhu'])
    feels_like, _ = format_temp(latest_data['terasa_seperti'])
    wind_display = format_wind(latest_data['kecepatan_angin'])

    c_desc = latest_data['deskripsi_cuaca'].title()
    c_icon_name = icon_url.split('/')[-1]

    with main_col:
        st.markdown(f"""
            <div class="weather-card main-card-flex">
                <div>
                    <div class="card-title">{active_city}</div>
                    <div class="card-subtitle">Kondisi: {c_desc}</div>
                    <div class="big-temp">{c_temp}{t_sym}</div>
                </div>
                <img src="{icon_url}" style="width: 220px; filter: drop-shadow(0px 15px 15px rgba(0,0,0,0.4));">
            </div>

            <div class="weather-card">
                <div class="section-title">TODAY'S FORECAST</div>
                <div class="hourly-flex">
                    <div class="hourly-item"><div class="hourly-time">6:00 AM</div><img src="{base_img}/cloud.png" width="55"><div class="hourly-temp">{format_temp(latest_data['suhu'] - 3)[0]}{t_sym}</div></div>
                    <div class="hourly-item"><div class="hourly-time">9:00 AM</div><img src="{base_img}/partly-cloudy-day.png" width="55"><div class="hourly-temp">{format_temp(latest_data['suhu'] - 1)[0]}{t_sym}</div></div>
                    <div class="hourly-item"><div class="hourly-time">12:00 PM</div><img src="{icon_url}" width="55"><div class="hourly-temp">{c_temp}{t_sym}</div></div>
                    <div class="hourly-item"><div class="hourly-time">3:00 PM</div><img src="{icon_url}" width="55"><div class="hourly-temp">{format_temp(latest_data['suhu'] + 1)[0]}{t_sym}</div></div>
                    <div class="hourly-item"><div class="hourly-time">6:00 PM</div><img src="{base_img}/partly-cloudy-day.png" width="55"><div class="hourly-temp">{format_temp(latest_data['suhu'] - 1)[0]}{t_sym}</div></div>
                    <div class="hourly-item" style="border: none;"><div class="hourly-time">9:00 PM</div><img src="{base_img}/cloud.png" width="55"><div class="hourly-temp">{format_temp(latest_data['suhu'] - 2)[0]}{t_sym}</div></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="weather-card" style="padding-bottom: 5px;">', unsafe_allow_html=True)
        head_c1, head_c2 = st.columns([4, 1])
        with head_c1: st.markdown('<div class="section-title" style="margin-top: 5px;">AIR CONDITIONS</div>', unsafe_allow_html=True)
        with head_c2: st.button("See more", type="primary", on_click=go_to_detail_callback, use_container_width=True)

        st.markdown(f"""
                <div class="air-grid" style="margin-top: 10px; margin-bottom: 20px;">
                    <div class="air-item"><span class="material-symbols-rounded air-icon">device_thermostat</span><div><div class="air-label">Real Feel</div><div class="air-value">{feels_like}{t_sym}</div></div></div>
                    <div class="air-item"><span class="material-symbols-rounded air-icon">air</span><div><div class="air-label">Wind</div><div class="air-value">{wind_display}</div></div></div>
                    <div class="air-item"><span class="material-symbols-rounded air-icon">water_drop</span><div><div class="air-label">Humidity</div><div class="air-value">{latest_data['kelembapan']}%</div></div></div>
                    <div class="air-item"><span class="material-symbols-rounded air-icon">light_mode</span><div><div class="air-label">UV Index</div><div class="air-value">3</div></div></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with right_col:
        base_c = latest_data['suhu']
        days = [
            ("Today", c_icon_name, c_desc, base_c + 1, base_c - 3),
            ("Tue", "sun.png", "Cerah", base_c + 2, base_c - 2),
            ("Wed", "partly-cloudy-day.png", "Berawan", base_c + 1, base_c - 3),
            ("Thu", "cloud.png", "Mendung", base_c, base_c - 4),
            ("Fri", "cloud.png", "Mendung", base_c - 1, base_c - 4),
            ("Sat", "storm.png", "Hujan", base_c - 3, base_c - 5),
            ("Sun", "sun.png", "Cerah", base_c + 2, base_c - 2),
        ]
        rows_html = ""
        for day, icon, desc, t_max_c, t_min_c in days:
            t_max, _ = format_temp(t_max_c)
            t_min, _ = format_temp(t_min_c)
            rows_html += f'<div class="forecast-row"><div class="f-day">{day}</div><div class="f-cond"><img src="{base_img}/{icon}" width="35"><span>{desc}</span></div><div class="f-temp">{t_max}{t_sym} <span class="f-temp-min">/{t_min}{t_sym}</span></div></div>'
        st.markdown(f'<div class="weather-card" style="padding: 30px 25px;"><div class="section-title">7-DAY FORECAST</div>{rows_html}</div>', unsafe_allow_html=True)
