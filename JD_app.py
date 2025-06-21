import pandas as pd
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="LPG Operations Calculator",
    layout="wide"
)

# Sidebar Navigation
st.sidebar.image("JD.jpeg", width=150)
st.sidebar.title("LPG Tools")
menu = st.sidebar.radio("Select a calculation", ["Vessel Volume", "Per Kg Price", "Litres Sold", "Litres Left"])

# Header
st.title("LPG Operations Calculator")
st.caption(f"Logged in | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.markdown("---")

# Vessel Volume Calculation
if menu == "Vessel Volume":
    st.subheader("🔢 Vessel Product Volume Calculation")

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

# Placeholder sections for future tools
elif menu == "Per Kg Price":
    st.subheader("💰 Per Kg Price Calculator")
    st.markdown("Calculate the LPG price per kilogram and cylinder sizes (3kg to 17kg).")

    with st.form("price_calc"):
        col1, col2 = st.columns(2)

        with col1:
            litre_price = st.number_input("LPG Price per Litre (₵)", min_value=0.0, step=0.01, format="%.2f")

        with col2:
            density = st.number_input("LPG Density (kg/L)", min_value=0.01, step=0.01, value=0.54, format="%.3f")

        submitted = st.form_submit_button("Calculate")

    if submitted and density > 0:
        price_per_kg = litre_price / density

        st.success(f"✅ Price per kg: ₵{price_per_kg:.2f}")

        # Create price table for 3kg to 17kg cylinders
        weights = list(range(3, 18))
        prices = [round(weight * price_per_kg, 2) for weight in weights]
        df_prices = pd.DataFrame({
            "Cylinder Size (kg)": weights,
            "Total Price (₵)": prices
        })

        st.markdown("### Cylinder Price Table")
        st.dataframe(df_prices, use_container_width=True)


elif menu == "Litres Sold":
    st.subheader("📊 Total Litres Sold Comparison")

    st.markdown("#### 💧 Dispenser Pump Readings")
    with st.form("litres_sold_form"):
        col1, col2 = st.columns(2)

        with col1:
            pump1_initial = st.number_input("Pump 1 - Initial Reading (L)", min_value=0.0, step=0.1, format="%.2f")
            pump2_initial = st.number_input("Pump 2 - Initial Reading (L)", min_value=0.0, step=0.1, format="%.2f")

        with col2:
            pump1_final = st.number_input("Pump 1 - Final Reading (L)", min_value=0.0, step=0.1, format="%.2f")
            pump2_final = st.number_input("Pump 2 - Final Reading (L)", min_value=0.0, step=0.1, format="%.2f")

        st.markdown("#### 📏 Rotorgauge-Based Litres Calculation")

        col3, col4 = st.columns(2)
        with col3:
            rotor_initial = st.number_input("Initial Rotor %", min_value=0.0, max_value=200.0, step=0.1, format="%.2f")
            tank_capacity = st.number_input("Tank Capacity (L)", min_value=0.0, step=1.0, format="%.2f")
        with col4:
            rotor_final = st.number_input("Final Rotor %", min_value=0.0, max_value=100.0, step=0.1, format="%.2f")
            density = st.number_input("LPG Density (kg/L)", min_value=0.01, value=0.54, step=0.01, format="%.3f")

        submitted = st.form_submit_button("Calculate")

    if submitted:
        # Dispenser readings
        pump1_sold = pump1_final - pump1_initial
        pump2_sold = pump2_final - pump2_initial
        total_dispensed = pump1_sold + pump2_sold

        # Rotor gauge calculation
        rotor_diff = rotor_initial - rotor_final
        theoretical_litres = (rotor_diff / 100.0) * tank_capacity
        theoretical_kg = theoretical_litres * density

        # Variance
        variance_litres = total_dispensed - theoretical_litres
        status = "Overage" if variance_litres > 0 else "Shortage" if variance_litres < 0 else "Balanced"

        # Display results
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
            st.markdown(":green[↑ LPG dispensed is more than expected.]")
        elif variance_litres < 0:
            st.error(f"**Shortage:** {abs(variance_litres):.2f} L 📉🔴")
            st.markdown(":red[↓ LPG dispensed is less than expected.]")
        else:
            st.info("**Status:** ✅ Balanced — No variance detected.")



elif menu == "Litres Left":
    st.subheader("🚛 Offloading Planner - Bulk Truck to Station Tank")

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
        # Compute current levels
        truck_litres_available = (truck_rotor / 100.0) * bulk_capacity
        station_litres_current = (station_rotor / 100.0) * station_capacity
        station_litres_safe_limit = (safe_level / 100.0) * station_capacity

        # Determine space available in station tank
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
        
