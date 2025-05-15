import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(
    page_title="JD Link Oil Gas Operations",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar
st.sidebar.image("JD.jpeg", width=200)
st.sidebar.title("JD Link Oil")
st.sidebar.markdown("**Operations Management Dashboard**")

# Navigation
pages = ["Calibration", "Daily Report", "Offloading", "Gas Calculations"]
page = st.sidebar.radio("Navigate to", pages)

# Main Interface Header with Logo
header_col1, header_col2 = st.columns([0.1, 0.9])
with header_col1:
    st.image("JD.jpeg", width=60)
with header_col2:
    st.title("JD Link Oil Gas Operations")

st.markdown("---")

# Calibration data storage (in-memory for now)
if 'calibration_data' not in st.session_state:
    st.session_state.calibration_data = []

if 'calibration_report' not in st.session_state:
    st.session_state.calibration_report = ""

if page == "Calibration":
    st.subheader("Calibration Module")
    st.markdown("Enter calibration data for each cylinder.")

    col1, col2 = st.columns([1, 2])

    with col1:
        with st.form("calibration_form"):
            cylinder_code = st.text_input("Cylinder Code (#)", key="code", max_chars=20)
            date = st.date_input("Date")
            weight_before = st.number_input("Weight Before (kg)", min_value=0.0, format="%.2f", key="before")
            weight_after = st.number_input("Weight After (kg)", min_value=0.0, format="%.2f", key="after")
            pump = st.selectbox("Pump", ["Pump 1", "Pump 2", "Pump 3"], key="pump")
            location = st.selectbox("Location", ["Ayikuma", "Kasoa", "Tema", "Kumasi"], key="location")
            start_time = st.time_input("Calibration Start Time")
            end_time = st.time_input("Calibration End Time")
            difference = weight_after - weight_before

            st.markdown(f"**Difference:** {difference:.2f} kg")

            submitted = st.form_submit_button("Submit Calibration Data")
            if submitted:
                st.success("Calibration data submitted successfully.")
                st.session_state.calibration_data.append({
                    "Cylinder Code": cylinder_code,
                    "Date": date.strftime('%Y-%m-%d'),
                    "Weight Before (kg)": weight_before,
                    "Weight After (kg)": weight_after,
                    "Difference (kg)": difference,
                    "Pump": pump,
                    "Location": location,
                    "Start Time": start_time.strftime("%I:%M %p"),
                    "End Time": end_time.strftime("%I:%M %p")
                })

        if st.button("Clear All Calibration Data", type="primary"):
            st.session_state.calibration_data.clear()
            st.session_state.calibration_report = ""
            st.warning("All calibration data cleared.")

        if st.button("Create Report") and st.session_state.calibration_data:
            now = datetime.now()
            period = "Morning" if now.hour < 12 else ("Afternoon" if now.hour < 17 else "Evening")
            report_date = now.strftime("%d/%m/%Y")

            report_lines = [
                "@⁨Boss. Evans Gatienu JDL⁩ @⁨Enoch JD Head Office⁩ @⁨Sir Isaac Operations JD Link⁩",
                f"\n{st.session_state.calibration_data[0]['Location']} calibration",
                f"\nLocation: {st.session_state.calibration_data[0]['Location']}",
                f"as at {report_date}",
                f"\n{period} -",
                f"Time: {st.session_state.calibration_data[0]['Start Time']} - {st.session_state.calibration_data[0]['End Time']}\n"
            ]
            for item in st.session_state.calibration_data:
                report_lines.append(f"Cylinder code: {item['Cylinder Code']}\nInitial weight: {item['Weight Before (kg)']}kg\nFinal weight: {item['Weight After (kg)']}kg\nDifference: {item['Difference (kg)']}kg\nPump: {item['Pump']}\n")

            st.session_state.calibration_report = "\n".join(report_lines)

    with col2:
        st.markdown("### Calibration Records")
        if st.session_state.calibration_data:
            df = pd.DataFrame(st.session_state.calibration_data)
            st.dataframe(df, use_container_width=True)
            st.markdown("### Calibration Report")
            st.text_area("Report Output", value=st.session_state.calibration_report, height=400, key="report_output")
            st.button("📋 Copy Report", on_click=st.code, args=(st.session_state.calibration_report,), key="copy_button")
        else:
            st.info("No calibration records submitted yet.")

elif page == "Daily Report":
    st.subheader("Daily Report")
    st.markdown("Log daily operations, incidents, and production data.")
    # Placeholder for future daily report content
    st.info("Daily report logging coming soon.")

elif page == "Offloading":
    st.subheader("Offloading")
    st.markdown("Monitor offloading processes and generate summaries.")
    # Placeholder for future offloading content
    st.info("Offloading tools coming soon.")

elif page == "Gas Calculations":
    st.subheader("Gas Calculations")
    st.markdown("Perform calculations for gas usage, conversions, and analytics.")
    # Placeholder for future gas calculations content
    st.info("Gas calculation modules coming soon.")

# Footer
st.markdown("---")
st.caption(f"Logged in as: JD Link Oil Operations Manager | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
