# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
import pandas as pd

# Title and Subtitle
st.title(f"Troop 905 Attendance Tracker📚 Version 0.0")
st.write(
  """This is a prototype for a proposed website for Troop 905 
  attendance for a more accesible interface as compared 
  to a google sheet. Attendance was updated August 8 11:00am.
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


time_to_q = st.button("Get attendance")

if time_to_q:
    #try:
    queried_name = str(queried_name[0])
    meetings_attended_query = "select meetings_count from T905.ATTENDANCE.T905_ATTENDANCE where NAME = '" + queried_name + "'"
    meetings_attended = session.sql(meetings_attended_query)
    meetings_attended = meetings_attended.select(col('MEETINGS_COUNT')).collect()
    meetings_attended = meetings_attended[0]['MEETINGS_COUNT']
    # NEEDS TO BE UPDATED TO BE AUTOMATIC!!!!!!!!!
    meetings_possible = 4
    meetings_ratio = meetings_attended/meetings_possible * 100
    st.write(f"""So far, {queried_name} has attended {meetings_ratio}% 
of meetings. \n\nThe minimum requirement for getting credit for
a leadership position is 51%. \n\nA good amount to aim for is 90%,
or an 'A' grade.""")
    # except:
    #     st.write('Something bad happened.')
