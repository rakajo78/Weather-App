import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

def render_map(main_col, right_col, latest_data, icon_url, base_img, city_data, get_icon_func, active_city, format_temp):
    # Koordinat kota-kota di Pulau Jawa + Bali
    CITY_COORDS = {
        "Jakarta": (-6.2088, 106.8456),
        "Bandung": (-6.9175, 107.6191),
        "Yogyakarta": (-7.7956, 110.3695),
        "Surabaya": (-7.2575, 112.7521),
        "Bali": (-8.6500, 115.2167),
    }

    with main_col:
        # Buat peta Folium berpusat di Pulau Jawa
        m = folium.Map(
            location=[-7.5, 110.5],
            zoom_start=7,
            tiles="CartoDB dark_matter",
            control_scale=True,
            zoom_control=True,
            max_bounds=True,
        )

        # Batas peta agar fokus di Jawa-Bali
        m.fit_bounds([[-9.0, 105.0], [-5.5, 116.0]])

        for city_name, data in city_data.items():
            coords = CITY_COORDS.get(city_name)
            if not coords:
                continue

            c_temp, t_sym = format_temp(data['suhu'])
            c_desc = data['deskripsi_cuaca'].title()
            c_icon = get_icon_func(data['deskripsi_cuaca'])

            try:
                time_str = pd.to_datetime(data['waktu_pencatatan']).strftime('%H:%M')
            except:
                time_str = "Real-time"

            is_active = city_name == active_city

            # Popup HTML premium
            popup_html = f"""
            <div style="
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #1a2230 0%, #202b3b 100%);
                color: white;
                padding: 18px 22px;
                border-radius: 16px;
                min-width: 200px;
                text-align: center;
                box-shadow: 0 8px 32px rgba(0,0,0,0.4);
                border: {('2px solid #0095ff' if is_active else '1px solid #323d4e')};
            ">
                <div style="font-size: 18px; font-weight: bold; margin-bottom: 6px;">{city_name}</div>
                <img src="{c_icon}" width="65" style="filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3)); margin: 8px 0;">
                <div style="font-size: 32px; font-weight: bold; margin: 4px 0;">{c_temp}{t_sym}</div>
                <div style="color: #939cb0; font-size: 13px; margin-top: 4px;">{c_desc}</div>
                <div style="color: #6b7a90; font-size: 11px; margin-top: 6px;">🕐 {time_str}</div>
            </div>
            """



            # Custom DivIcon untuk tampilan lebih premium
            custom_icon = folium.DivIcon(
                icon_size=(120, 80),
                icon_anchor=(60, 80),
                html=f"""
                <div style="
                    background: {'linear-gradient(135deg, #0a3d6b 0%, #0095ff 100%)' if is_active else 'linear-gradient(135deg, #1a2230 0%, #202b3b 100%)'};
                    color: white;
                    padding: 8px 14px;
                    border-radius: 14px;
                    text-align: center;
                    font-family: 'Segoe UI', sans-serif;
                    box-shadow: 0 6px 20px rgba(0,0,0,0.5);
                    border: {('2px solid #0095ff' if is_active else '1px solid #323d4e')};
                    white-space: nowrap;
                    transition: transform 0.2s;
                    cursor: pointer;
                ">
                    <div style="font-weight: bold; font-size: 13px;">{city_name}</div>
                    <div style="font-size: 20px; font-weight: bold;">{c_temp}{t_sym}</div>
                </div>
                """
            )

            folium.Marker(
                location=coords,
                popup=folium.Popup(popup_html, max_width=250),
                icon=custom_icon,
                tooltip=f"{city_name}: {c_temp}{t_sym} — {c_desc}",
            ).add_to(m)

        # Custom CSS untuk Folium map agar sesuai dark theme
        st.markdown("""
        <style>
            iframe[title="streamlit_folium.st_folium"] {
                border-radius: 20px !important;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
                border: 1px solid #323d4e !important;
            }
            .leaflet-popup-content-wrapper {
                background: transparent !important;
                box-shadow: none !important;
                padding: 0 !important;
            }
            .leaflet-popup-tip {
                background: #202b3b !important;
            }
            .leaflet-popup-close-button {
                color: white !important;
                font-size: 18px !important;
                top: 8px !important;
                right: 10px !important;
            }
        </style>
        """, unsafe_allow_html=True)

        st_folium(m, width=None, height=550, use_container_width=True, returned_objects=[])

    with right_col:
        html_list = ""
        for city_name, data in city_data.items():
            c_icon = get_icon_func(data['deskripsi_cuaca'])
            c_temp, t_sym = format_temp(data['suhu'])
            try: time_str = pd.to_datetime(data['waktu_pencatatan']).strftime('%H:%M')
            except: time_str = "Real-time"

            bg_active = "background-color: #32405b; border-left-color: #0095ff;" if city_name == active_city else ""


            html_list += f"""<div class="mini-city-card" style="{bg_active}">
<img src="{c_icon}" width="45">
<div class="mini-city-info">
<div class="mini-city-name">{city_name}</div>
<div class="mini-city-time">{time_str}</div>
</div>
<div class="mini-city-temp">{c_temp}{t_sym}</div>
</div>"""

        st.markdown(html_list, unsafe_allow_html=True)
