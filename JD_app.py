import pandas as pd
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="LPG Operations Calculator",
    layout="wide"
)

# Welcome Message (shown once per session)
if "first_visit" not in st.session_state:
    st.session_state.first_visit = True

if st.session_state.first_visit:
    st.toast("👋 Welcome to the LPG Operations Calculator!", icon="ℹ️")
    st.session_state.first_visit = False

# Sidebar Navigation
st.sidebar.image("JD.jpeg", width=150)
st.sidebar.title("LPG Tools")
menu = st.sidebar.radio("Select a calculation", ["Vessel Volume", "Per Kg Price", "Litres Sold", "Offload", "Calibration"])

# Header
st.title("LPG Operations Calculator")
st.caption(f"Logged in | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.markdown("---")

# Vessel Volume Calculation
if menu == "Vessel Volume":
    st.subheader("🔢 Vessel Product Volume Calculation")

    with st.expander("💡 How to Use This Tool"):
        st.markdown("""
        - Input **Rotor % Left** and **Right** from the gauge.
        - Enter **Bulk Capacity** in litres.
        - Adjust LPG **Density (kg/L)** if needed (default: 0.54).
        - Click **Calculate** to get litres, kg, and tons.
        """)

    with st.form("vessel_calc"):
        col1, col2 = st.columns(2)

        with col1:
            rotor_left = st.number_input("Rotor % Left", min_value=0.0, max_value=100.0, step=0.1, format="%.2f")
            bulk_capacity = st.number_input("Bulk Capacity (litres)", min_value=0.0, step=1.0, format="%.2f")

        with col2:
            rotor_right = st.number_input("Rotor % Right", min_value=0.0, max_value=100.0, step=0.1, format="%.2f")
            density = st.number_input("LPG Density (kg/L)", min_value=0.0, step=0.01, value=0.54, format="%.3f")

        submitted = st.form_submit_button("Calculate")

        if submitted:
            avg_rotor = (rotor_left + rotor_right) / 2
            litres = (avg_rotor / 100.0) * bulk_capacity
            mass_kg = litres * density
            mass_tons = mass_kg / 1000

            st.success("✅ Calculation Complete")
            st.write(f"**Average Rotor %**: {avg_rotor:.2f}%")
            st.write(f"**Volume in Litres**: {litres:,.2f} L")
            st.write(f"**Mass in Kilograms**: {mass_kg:,.2f} kg")
            st.write(f"**Mass in Tons**: {mass_tons:,.2f} tons")

# Per Kg Price Calculator
elif menu == "Per Kg Price":
    st.subheader("💰 Per Kg Price Calculator")

    with st.expander("💡 How to Use This Tool"):
        st.markdown("""
        - Enter **LPG Price per Litre (₵)**.
        - Adjust **LPG Density** if necessary (default: 0.54).
        - Click **Calculate** to view **₵/kg** and cylinder prices from **3kg to 17kg**.
        """)

    with st.form("price_calc"):
        col1, col2 = st.columns(2)

        with col1:
            litre_price = st.number_input("LPG Price per Litre (₵)", min_value=0.0, step=0.01, format="%.2f")

        with col2:
            density = st.number_input("LPG Density (kg/L)", min_value=0.01, step=0.01, value=0.54, format="%.3f")

        submitted = st.form_submit_button("Calculate")

    if submitted:
        price_per_kg = litre_price / density
        st.success(f"✅ Price per kg: ₵{price_per_kg:.2f}")

        # Cylinder prices
        weights = list(range(3, 18))
        prices = [round(weight * price_per_kg, 2) for weight in weights]
        df_prices = pd.DataFrame({
            "Cylinder Size (kg)": weights,
            "Total Price (₵)": prices
        })

        st.markdown("### Cylinder Price Table")
        st.dataframe(df_prices, use_container_width=True)

# Litres Sold
elif menu == "Litres Sold":
    st.subheader("📊 Total Litres Sold Comparison")

    with st.expander("💡 How to Use This Tool"):
        st.markdown("""
        - Fill in **initial and final readings** for both pumps.
        - Enter **rotor % before and after** sale, tank capacity, and LPG density.
        - See litres sold, theoretical litres, and any overage/shortage.
        """)

    with st.form("litres_sold_form"):
        col1, col2 = st.columns(2)

        with col1:
            pump1_initial = st.number_input("Pump 1 - Initial Reading (L)", min_value=0.0, step=0.1, format="%.2f")
            pump2_initial = st.number_input("Pump 2 - Initial Reading (L)", min_value=0.0, step=0.1, format="%.2f")

        with col2:
            pump1_final = st.number_input("Pump 1 - Final Reading (L)", min_value=0.0, step=0.1, format="%.2f")
            pump2_final = st.number_input("Pump 2 - Final Reading (L)", min_value=0.0, step=0.1, format="%.2f")

        col3, col4 = st.columns(2)
        with col3:
            rotor_initial = st.number_input("Initial Rotor %", min_value=0.0, max_value=200.0, step=0.1, format="%.2f")
            tank_capacity = st.number_input("Tank Capacity (L)", min_value=0.0, step=1.0, format="%.2f")
        with col4:
            rotor_final = st.number_input("Final Rotor %", min_value=0.0, max_value=100.0, step=0.1, format="%.2f")
            density = st.number_input("LPG Density (kg/L)", min_value=0.01, value=0.54, step=0.01, format="%.3f")

        submitted = st.form_submit_button("Calculate")

    if submitted:
        pump1_sold = pump1_final - pump1_initial
        pump2_sold = pump2_final - pump2_initial
        total_dispensed = pump1_sold + pump2_sold

        rotor_diff = rotor_initial - rotor_final
        theoretical_litres = (rotor_diff / 100.0) * tank_capacity
        theoretical_kg = theoretical_litres * density
        variance_litres = total_dispensed - theoretical_litres

        st.success("✅ Calculations Complete")
        st.markdown("### 🔍 Dispenser Summary")
        st.write(f"**Pump 1 Sold:** {pump1_sold:.2f} L")
        st.write(f"**Pump 2 Sold:** {pump2_sold:.2f} L")
        st.write(f"**Total Dispensed:** {total_dispensed:.2f} L")

        st.markdown("### 📊 Rotor Gauge Summary")
        st.write(f"**Rotor Difference:** {rotor_diff:.2f}%")
        st.write(f"**Theoretical Litres Sold:** {theoretical_litres:.2f} L")
        st.write(f"**Mass Sold (kg):** {theoretical_kg:.2f} kg")

        st.markdown("### ⚠️ Variance Check")
        if variance_litres > 0:
            st.success(f"**Overage:** {variance_litres:.2f} L 📈🟢")
        elif variance_litres < 0:
            st.error(f"**Shortage:** {abs(variance_litres):.2f} L 📉🔴")
        else:
            st.info("**Status:** ✅ Balanced — No variance detected.")

# Offload
elif menu == "Offload":
    st.subheader("🚛 Offloading Planner - Bulk Truck to Station Tank")

    with st.expander("💡 How to Use This Tool"):
        st.markdown("""
        - Enter **Truck Rotor %**, **Truck Capacity**, and **Station Capacity**.
        - Add **Station Rotor %** and **Safe Fill Level** (default 85%).
        - Result shows how much to offload and how much remains.
        """)

    with st.form("offload_calc"):
        col1, col2 = st.columns(2)

        with col1:
            truck_rotor = st.number_input("Truck Rotor Gauge (%)", min_value=0.0, max_value=100.0, step=0.1, format="%.2f")
            bulk_capacity = st.number_input("Bulk Truck Capacity (L)", min_value=0.0, step=1.0, format="%.2f")
            station_capacity = st.number_input("Station Tank Capacity (L)", min_value=0.0, step=1.0, format="%.2f")

        with col2:
            safe_level = st.number_input("Station Safe Level (%)", min_value=0.0, max_value=100.0, value=85.0, step=0.1, format="%.1f")
            station_rotor = st.number_input("Station Rotor Gauge (%)", min_value=0.0, max_value=100.0, step=0.1, format="%.2f")

        submitted = st.form_submit_button("Calculate")

    if submitted:
        truck_litres_available = (truck_rotor / 100.0) * bulk_capacity
        station_litres_current = (station_rotor / 100.0) * station_capacity
        station_litres_safe_limit = (safe_level / 100.0) * station_capacity

        litres_to_fill = station_litres_safe_limit - station_litres_current
        litres_to_offload = min(truck_litres_available, litres_to_fill)
        final_truck_litres = truck_litres_available - litres_to_offload
        final_truck_percent = (final_truck_litres / bulk_capacity) * 100 if bulk_capacity > 0 else 0
        percent_of_truck_used = (litres_to_offload / bulk_capacity) * 100 if bulk_capacity > 0 else 0

        st.success("✅ Offloading Calculation Complete")
        st.markdown("### 🧾 Offloading Summary")
        st.write(f"**Litres in Truck (Before Offload):** {truck_litres_available:,.2f} L")
        st.write(f"**Current Station Volume:** {station_litres_current:,.2f} L")
        st.write(f"**Max Safe Fill Level:** {station_litres_safe_limit:,.2f} L")

        st.markdown("---")
        st.write(f"**🔽 Litres to Offload:** {litres_to_offload:,.2f} L")
        st.write(f"**📥 % of Bulk Truck Used to Fill Station Tank:** {percent_of_truck_used:.2f}%")
        st.write(f"**🚚 Litres Left in Truck After Offload:** {final_truck_litres:,.2f} L")
        st.write(f"**Truck Rotor % After Offload:** {final_truck_percent:.2f}%")

elif menu == "Calibration":
    st.subheader("🧪 Cylinder Calibration Tracker")

    with st.expander("💡 How to Use This Tool"):
        st.markdown("""
        - Enter calibration data for each cylinder.
        - Click **Add Entry** to update the table.
        - Use **Create New Table** to reset data.
        """)

    # Initialize calibration data in session state
    if "calibration_data" not in st.session_state:
        st.session_state.calibration_data = []

    # Calibration form
    with st.form("calibration_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            cylinder_no = st.text_input("Cylinder #")
            pump = st.selectbox("Pump", [1, 2])
        with col2:
            initial_kg = st.number_input("Initial Weight (kg)", min_value=0.0, step=0.1)
            final_kg = st.number_input("Final Weight (kg)", min_value=0.0, step=0.1)
        with col3:
            date = st.date_input("Date")
            time = st.time_input("Time")

        add_entry = st.form_submit_button("➕ Add Entry")

    if add_entry:
        diff = round(final_kg - initial_kg, 2)
        new_entry = {
            "Cylinder #": cylinder_no,
            "Initial (kg)": initial_kg,
            "Final (kg)": final_kg,
            "Difference (kg)": diff,
            "Pump": pump,
            "Date": date.strftime("%Y-%m-%d"),
            "Time": time.strftime("%H:%M:%S")
        }
        st.session_state.calibration_data.append(new_entry)
        st.success("✅ Entry added!")

    # Button to reset
    if st.button("🧹 Create New Table"):
        st.session_state.calibration_data = []
        st.success("🆕 Calibration table reset!")

    # Display table
    if st.session_state.calibration_data:
        df_cal = pd.DataFrame(st.session_state.calibration_data)
        st.markdown("### 📋 Calibration Log")
        st.dataframe(df_cal, use_container_width=True)
    else:
        st.info("No calibration data yet.")
