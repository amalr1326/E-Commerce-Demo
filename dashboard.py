import streamlit as st
import random
import time
import plotly.express as px
import pandas as pd
from datetime import datetime

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Peak Commerce Intelligence Platform",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS (animation + severity colors)
# --------------------------------------------------
st.markdown("""
<style>
.event-box {
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 12px;
    animation: fadeIn 0.5s ease-in;
}

.info { background-color: #1f77b420; }
.alert { background-color: #f39c1220; }
.critical { background-color: #e74c3c30; }

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "inventory" not in st.session_state:
    st.session_state.inventory = {
        "North": 5, "South": 5, "East": 5, "West": 5
    }

if "waitlist" not in st.session_state:
    st.session_state.waitlist = {
        "North": 0, "South": 0, "East": 0, "West": 0
    }

if "events" not in st.session_state:
    st.session_state.events = []

if "paused" not in st.session_state:
    st.session_state.paused = False

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("🚀 Peak Commerce Intelligence Platform")
st.caption("Real-Time Operations Dashboard — Flash Sale Simulation")

if st.button("⏯ Pause / Resume Simulation"):
    st.session_state.paused = not st.session_state.paused

col1, col2, col3 = st.columns([1.1, 1.4, 1.1])

# --------------------------------------------------
# SIMULATION LOGIC
# --------------------------------------------------
if not st.session_state.paused:
    region = random.choice(list(st.session_state.inventory.keys()))
    action = random.choice(["view", "add_to_cart", "purchase"])
    user = random.randint(100, 999)
    timestamp = datetime.now().strftime("%H:%M:%S")

    severity = "INFO"
    message = ""

    if action == "purchase":
        if st.session_state.inventory[region] > 0:
            st.session_state.inventory[region] -= 1
            message = "Order Confirmed"
            if st.session_state.inventory[region] <= 1:
                message += " — Low Inventory"
                severity = "ALERT"
        else:
            st.session_state.waitlist[region] += 1
            message = "Out of Stock → Added to Waitlist"
            severity = "CRITICAL"

    elif action == "add_to_cart":
        message = "Personalized Offer Triggered"

    else:
        message = "Product Viewed"

    st.session_state.events.insert(0, {
        "time": timestamp,
        "region": region,
        "user": user,
        "action": action.replace("_", " ").title(),
        "message": message,
        "severity": severity
    })

    st.session_state.events = st.session_state.events[:7]

# --------------------------------------------------
# LEFT — INVENTORY
# --------------------------------------------------
with col1:
    st.subheader("📦 Inventory by Region")

    inv_df = pd.DataFrame({
        "Region": st.session_state.inventory.keys(),
        "Units Remaining": st.session_state.inventory.values()
    })

    fig_inv = px.bar(
        inv_df,
        x="Region",
        y="Units Remaining",
        color="Units Remaining",
        color_continuous_scale="Blues",
        range_y=[0, 6]
    )

    st.plotly_chart(fig_inv, use_container_width=True)

# --------------------------------------------------
# MIDDLE — EVENT STREAM (FIXED)
# --------------------------------------------------
with col2:
    st.subheader("🧾 Live Event Stream")

    for e in st.session_state.events:
        css_class = e["severity"].lower()

        st.markdown(f"""
<div class="event-box {css_class}">
<b>{e['severity']}</b> ⏱ {e['time']}<br><br>
📍 <b>Region:</b> {e['region']}<br>
👤 <b>User:</b> {e['user']}<br>
🛒 <b>Action:</b> {e['action']}<br>
💡 <b>Status:</b> {e['message']}
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# RIGHT — WAITLIST
# --------------------------------------------------
with col3:
    st.subheader("⏳ Waitlist Pressure")

    wait_df = pd.DataFrame({
        "Region": st.session_state.waitlist.keys(),
        "Waitlist Count": st.session_state.waitlist.values()
    })

    fig_wait = px.bar(
        wait_df,
        x="Region",
        y="Waitlist Count",
        color="Waitlist Count",
        color_continuous_scale="Reds"
    )

    st.plotly_chart(fig_wait, use_container_width=True)

# --------------------------------------------------
# REAL-TIME LOOP
# --------------------------------------------------
time.sleep(1)
st.rerun()