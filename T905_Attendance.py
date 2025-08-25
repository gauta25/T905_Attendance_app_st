import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col

# st.title("Website in maintainence. Will be back soon. \n-11:00am Aug 25 2025 /n - Gautam")
# st.stop()
# # --- LOGIN PAGE ---
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# if not st.session_state.logged_in:
#     st.title("Troop 905 Attendance Tracker")
#     password = st.text_input("Enter password", type="password")
#     if st.button("Login"):
#         if password == "905Member":
#             st.session_state.logged_in = True
#             st.success("Login successful! Reloading app...")
#         else:
#             st.error("Incorrect password")
#     st.stop()  # Prevents rest of app from running until login is successful
    
# Init
cnx = st.connection("snowflake")
session = cnx.session()

Tdata = session.table('T905.ATTENDANCE.T905_ATTENDANCE').to_pandas()

# st.title("Troop 905 Attendance")

queried_name = st.multiselect('Choose a name to get attendance', Tdata,
                             max_selections=1)

st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

time_to_q = st.button("Get attendance")

if time_to_q and queried_name:
    queried_name = str(queried_name[0])
    meetings_attended_query = (
        f"select meetings_count from T905.ATTENDANCE.T905_ATTENDANCE "
        f"where NAME = '{queried_name}'"
    )
    meetings_attended = session.sql(meetings_attended_query)
    meetings_attended = meetings_attended.select(col('MEETINGS_COUNT')).collect()
    meetings_attended = meetings_attended[0]['MEETINGS_COUNT']
    meetings_possible = 6  # update automatically later if needed
    meetings_ratio = round(meetings_attended/meetings_possible * 100, 2)
    st.write(f"""So far, {queried_name} has attended {meetings_ratio}% 
of meetings. \n\nThe minimum requirement for getting credit for
a leadership position is 51%. \n\nA good amount to aim for is 90%,
or an 'A' grade.""")

st.write("Email gautamkanwar9@gmail.com for any changes.")
