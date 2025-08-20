# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
import pandas as pd

# Title and Subtitle
st.title(f"Troop 905 Attendance Tracker")
st.write(
  """This is an early version of a proposed attendance tracker for Troop 905.\n 

  Attendance was updated August 19, 9:20pm
  """
)

# Init
cnx = st.connection("snowflake")
session = cnx.session()

# Col function
from snowflake.snowpark.functions import col

Tdata = session.table('T905.ATTENDANCE.T905_ATTENDANCE').to_pandas()
# st.dataframe(data = Tdata, use_container_width = True)

queried_name = st.multiselect('Choose a name to get attendance', Tdata,
                             max_selections = 1)


st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

time_to_q = st.button("Get attendance")

if time_to_q:
    #try:
    queried_name = str(queried_name[0])
    meetings_attended_query = "select meetings_count from T905.ATTENDANCE.T905_ATTENDANCE where NAME = '" + queried_name + "'"
    meetings_attended = session.sql(meetings_attended_query)
    meetings_attended = meetings_attended.select(col('MEETINGS_COUNT')).collect()
    meetings_attended = meetings_attended[0]['MEETINGS_COUNT']
    # NEEDS TO BE UPDATED TO BE AUTOMATIC!!!!!!!!!
    meetings_possible = 5
    meetings_ratio = meetings_attended/meetings_possible * 100
    st.write(f"""So far, {queried_name} has attended {meetings_ratio}% 
of meetings. \n\nThe minimum requirement for getting credit for
a leadership position is 51%. \n\nA good amount to aim for is 90%,
or an 'A' grade.""")

st.write("Email gautamkanwar9@gmail.com for any changes.")
    # except:
    #     st.write('Something bad happened.')
