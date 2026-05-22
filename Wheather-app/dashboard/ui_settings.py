import streamlit as st

def render_settings(main_col, right_col):
    # --- CALLBACK FUNCTIONS: Auto-save saat user mengubah pilihan ---
    def save_temp():
        st.session_state.SAVED_temp = st.session_state._widget_temp

    def save_wind():
        st.session_state.SAVED_wind = st.session_state._widget_wind

    def save_pressure():
        st.session_state.SAVED_pressure = st.session_state._widget_pressure

    def save_precip():
        st.session_state.SAVED_precip = st.session_state._widget_precip

    def save_dist():
        st.session_state.SAVED_dist = st.session_state._widget_dist

    def save_notifications():
        st.session_state.SAVED_notifications = st.session_state._widget_notifications

    def save_12hour():
        st.session_state.SAVED_12hour = st.session_state._widget_12hour

    def save_location():
        st.session_state.SAVED_location = st.session_state._widget_location

    with main_col:
        st.markdown('<h2 style="margin-top: 0; margin-bottom: 20px; font-size: 24px;">Units</h2>', unsafe_allow_html=True)

        # Mengambil index (posisi) dari memori permanen agar tombol selalu berada di posisi terakhir yang di-save
        idx_temp = ["Celsius", "Fahrenheit"].index(st.session_state.SAVED_temp)
        idx_wind = ["km/h", "m/s", "Knots"].index(st.session_state.SAVED_wind)
        idx_press = ["hPa", "Inches", "kPa", "mm"].index(st.session_state.SAVED_pressure)
        idx_precip = ["Milimeters", "Inches"].index(st.session_state.SAVED_precip)
        idx_dist = ["Kilometers", "Miles"].index(st.session_state.SAVED_dist)

        # Radio buttons dengan on_change callback — langsung auto-save
        st.radio("TEMPERATURE", ["Celsius", "Fahrenheit"], horizontal=True, index=idx_temp,
                 key="_widget_temp", on_change=save_temp)
        st.radio("WIND SPEED", ["km/h", "m/s", "Knots"], horizontal=True, index=idx_wind,
                 key="_widget_wind", on_change=save_wind)
        st.radio("PRESSURE", ["hPa", "Inches", "kPa", "mm"], horizontal=True, index=idx_press,
                 key="_widget_pressure", on_change=save_pressure)
        st.radio("PRECIPITATION", ["Milimeters", "Inches"], horizontal=True, index=idx_precip,
                 key="_widget_precip", on_change=save_precip)
        st.radio("DISTANCE", ["Kilometers", "Miles"], horizontal=True, index=idx_dist,
                 key="_widget_dist", on_change=save_dist)

        st.markdown('<h2 style="margin-top: 30px; margin-bottom: 20px; font-size: 20px;">Notifications</h2>', unsafe_allow_html=True)
        st.toggle("Notifications (Be aware of the weather)",
                  value=st.session_state.SAVED_notifications,
                  key="_widget_notifications", on_change=save_notifications)

        st.markdown('<h2 style="margin-top: 30px; margin-bottom: 20px; font-size: 20px;">General</h2>', unsafe_allow_html=True)
        st.toggle("12-Hour Time",
                  value=st.session_state.SAVED_12hour,
                  key="_widget_12hour", on_change=save_12hour)
        st.toggle("Location (Get weather of your location)",
                  value=st.session_state.SAVED_location,
                  key="_widget_location", on_change=save_location)

        st.write("")  # Spacing

        # Indikator status — menampilkan pengaturan yang sedang aktif
        st.markdown(f"""
        <div style="background-color: #202b3b; border-radius: 15px; padding: 20px 25px; margin-top: 10px;">
            <div style="color: #939cb0; font-size: 12px; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px;">
                ✅ Current Settings
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 14px;">
                <span style="color: #939cb0;">Temperature:</span><span style="color: white; font-weight: 600;">{st.session_state.SAVED_temp}</span>
                <span style="color: #939cb0;">Wind Speed:</span><span style="color: white; font-weight: 600;">{st.session_state.SAVED_wind}</span>
                <span style="color: #939cb0;">Pressure:</span><span style="color: white; font-weight: 600;">{st.session_state.SAVED_pressure}</span>
                <span style="color: #939cb0;">Precipitation:</span><span style="color: white; font-weight: 600;">{st.session_state.SAVED_precip}</span>
                <span style="color: #939cb0;">Distance:</span><span style="color: white; font-weight: 600;">{st.session_state.SAVED_dist}</span>
                <span style="color: #939cb0;">Notifications:</span><span style="color: white; font-weight: 600;">{'On' if st.session_state.SAVED_notifications else 'Off'}</span>
                <span style="color: #939cb0;">12-Hour Time:</span><span style="color: white; font-weight: 600;">{'On' if st.session_state.SAVED_12hour else 'Off'}</span>
                <span style="color: #939cb0;">Location:</span><span style="color: white; font-weight: 600;">{'On' if st.session_state.SAVED_location else 'Off'}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- KOLOM KANAN ---
    with right_col:
        st.markdown("""
        <div class="weather-card" style="padding: 30px;">
            <h1 style="margin-top: 0; font-size: 36px; margin-bottom: 30px;">Advanced</h1>
            <h3 style="margin-top: 0; margin-bottom: 15px; font-size: 20px;">Get new experience</h3>
            <ul style="color: #939cb0; font-size: 14px; line-height: 2; padding-left: 20px; margin-bottom: 30px; list-style-type: disc;">
                <li>Ad free</li><li>Health activities overview</li><li>Severe weather notifications</li>
            </ul>
            <div style="background-color: #32405b; border-radius: 15px; padding: 20px; text-align: center;">
                <span style="font-size: 32px; font-weight: bold; color: white;">$5.99</span><span style="color: #939cb0; font-size: 14px;"> /month</span>
            </div>
        </div>

        <div class="weather-card" style="padding: 30px;">
            <h3 style="margin-top: 0; margin-bottom: 15px; font-size: 20px;">Never forget your umbrella!</h3>
            <p style="color: #939cb0; font-size: 14px; line-height: 1.6; margin-bottom: 30px;">
                Sign up for our daily weather newsletter personalized just for you.
            </p>
            <button style="width: 100%; background-color: #0095ff; color: white; border: none; border-radius: 20px; padding: 12px; font-weight: bold; font-size: 14px; cursor: pointer; transition: 0.3s;">
                Sign up
            </button>
        </div>
        """, unsafe_allow_html=True)
