import streamlit as st

def render_detail(main_col, right_col, latest_data, icon_url, base_img, active_city, format_temp, format_wind):
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

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div class="weather-card" style="margin-bottom: 0; padding: 20px;"><div class="detail-metric-title"><span class="material-symbols-rounded">light_mode</span> UV INDEX</div><div class="detail-metric-value">3</div></div>
                <div class="weather-card" style="margin-bottom: 0; padding: 20px;"><div class="detail-metric-title"><span class="material-symbols-rounded">air</span> WIND</div><div class="detail-metric-value">{wind_display}</div></div>
                <div class="weather-card" style="margin-bottom: 0; padding: 20px;"><div class="detail-metric-title"><span class="material-symbols-rounded">water_drop</span> HUMIDITY</div><div class="detail-metric-value">{latest_data['kelembapan']}%</div></div>
                <div class="weather-card" style="margin-bottom: 0; padding: 20px;"><div class="detail-metric-title"><span class="material-symbols-rounded">visibility</span> VISIBILITY</div><div class="detail-metric-value">12 km</div></div>
                <div class="weather-card" style="margin-bottom: 0; padding: 20px;"><div class="detail-metric-title"><span class="material-symbols-rounded">device_thermostat</span> FEELS LIKE</div><div class="detail-metric-value">{feels_like}{t_sym}</div></div>
                <div class="weather-card" style="margin-bottom: 0; padding: 20px;"><div class="detail-metric-title"><span class="material-symbols-rounded">rainy</span> CHANCE OF RAIN</div><div class="detail-metric-value">0%</div></div>
                <div class="weather-card" style="margin-bottom: 0; padding: 20px;"><div class="detail-metric-title"><span class="material-symbols-rounded">speed</span> PRESSURE</div><div class="detail-metric-value">1008 hPa</div></div>
                <div class="weather-card" style="margin-bottom: 0; padding: 20px;"><div class="detail-metric-title"><span class="material-symbols-rounded">wb_twilight</span> SUNSET</div><div class="detail-metric-value">17:30</div></div>
            </div>
        """, unsafe_allow_html=True)

    with right_col:
        st.markdown(f"""
            <div class="weather-card" style="padding: 25px;">
                <div class="section-title">TODAY'S FORECAST</div>
                <div class="hourly-flex">
                    <div class="hourly-item"><div class="hourly-time">6:00 AM</div><img src="{base_img}/cloud.png" width="50"><div class="hourly-temp">{format_temp(latest_data['suhu'] - 3)[0]}{t_sym}</div></div>
                    <div class="hourly-item"><div class="hourly-time">9:00 AM</div><img src="{base_img}/partly-cloudy-day.png" width="50"><div class="hourly-temp">{format_temp(latest_data['suhu'] - 1)[0]}{t_sym}</div></div>
                    <div class="hourly-item" style="border: none;"><div class="hourly-time">12:00 PM</div><img src="{icon_url}" width="50"><div class="hourly-temp">{c_temp}{t_sym}</div></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

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
            rows_html += f'<div class="forecast-row" style="padding: 10px 0;"><div class="f-day">{day}</div><div class="f-cond"><img src="{base_img}/{icon}" width="30"><span>{desc}</span></div><div class="f-temp">{t_max}{t_sym} <span class="f-temp-min">/{t_min}{t_sym}</span></div></div>'
        st.markdown(f'<div class="weather-card" style="padding: 25px;"><div class="section-title">7-DAY FORECAST</div>{rows_html}</div>', unsafe_allow_html=True)
