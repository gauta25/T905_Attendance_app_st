import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime

# ---- CONFIG ----
PATROLS = ["LL", "IS", "MPP", "RED", "GB", "TT", "SS"]
USERS = {
    "LL": {"patrol": "LL", "password": "pass1"},
    "IS": {"patrol": "IS", "password": "pass2"},
    "MPP": {"patrol": "MPP", "password": "pass3"},
    "RED": {"patrol": "RED", "password": "pass4"},
    "GB": {"patrol": "GB", "password": "pass5"},
    "TT": {"patrol": "TT", "password": "pass6"},
    "SS": {"patrol": "SS", "password": "pass7"},
    "GOD": {"patrol": "ALL", "password": "superpass"}
}
SPREADSHEET_ID = "YOUR_SPREADSHEET_ID"

# ---- GOOGLE SHEETS AUTH ----
creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID)

# ---- FUNCTIONS ----
def get_attendance_df(patrol):
    ws = sheet.worksheet(patrol)
    data = ws.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    return df

def update_attendance(patrol, name, present):
    ws = sheet.worksheet(patrol)
    header = ws.row_values(1)
    today_str = datetime.now().strftime("%-m/%-d/%Y")
    if today_str not in header:
        ws.update_cell(1, len(header)+1, today_str)
        header.append(today_str)
    col_index = header.index(today_str) + 1
    col_a = ws.col_values(1)
    row_index = col_a.index(name) + 1
    ws.update_cell(row_index, col_index, "TRUE" if present else "FALSE")

def calculate_percentage(df):
    total_cols = len(df.columns) - 1
    percentages = {}
    for _, row in df.iterrows():
        vals = row[1:].str.upper()
        present_count = vals[vals == "TRUE"].count()
        percentages[row[0]] = round((present_count / total_cols) * 100, 1) if total_cols > 0 else 0
    return percentages

def patrol_average(patrol):
    df = get_attendance_df(patrol)
    pcts = calculate_percentage(df)
    return round(sum(pcts.values()) / len(pcts), 1) if pcts else 0

# ---- UI ----
st.set_page_config(page_title="Scout Attendance", layout="centered")
st.title("🏕 Scout Attendance Tracker")

menu = ["Home", "Login"]
if "user" in st.session_state:
    menu.append("Take Attendance")
    if st.session_state.user["patrol"] == "ALL":
        menu.append("Stats")
choice = st.sidebar.radio("Menu", menu)

# ---- HOME PAGE ----
if choice == "Home":
    st.subheader("Attendance Percentages")
    for patrol in PATROLS:
        df = get_attendance_df(patrol)
        avg = patrol_average(patrol)
        st.metric(label=f"Patrol {patrol}", value=f"{avg}% Avg Attendance")

# ---- LOGIN ----
elif choice == "Login":
    st.subheader("Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        if u in USERS and USERS[u]["password"] == p:
            st.session_state.user = USERS[u]
            st.success(f"Welcome {u}!")
        else:
            st.error("Invalid credentials")

# ---- TAKE ATTENDANCE ----
elif choice == "Take Attendance":
    user = st.session_state.user
    patrol = user["patrol"]
    if patrol == "ALL":
        patrol = st.selectbox("Select Patrol", PATROLS)
    df = get_attendance_df(patrol)
    names = df.iloc[:, 0].tolist()

    st.write(f"Taking attendance for **{patrol}** on {datetime.now().strftime('%-m/%-d/%Y')}")
    for name in names:
        present = st.radio(f"{name} present?", ["Yes", "No"], index=0, key=name)
        if st.button(f"Save {name}", key=f"btn_{name}"):
            update_attendance(patrol, name, present == "Yes")
            st.success(f"Saved {name}'s attendance")

# ---- STATS PAGE ----
elif choice == "Stats":
    st.subheader("Patrol Averages")
    for patrol in PATROLS:
        st.metric(label=f"Patrol {patrol}", value=f"{patrol_average(patrol)}%")
