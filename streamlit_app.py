# Import python packages
import streamlit as st
import requests
import pandas as pd
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f" 🥤 Customize your Smoothie! :cup_with_straw:")
st.write(
  """Replace this example with your own code!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)
#cnx = st.connection("snowflake")
cnx = st.connection("snowflake", type="snowflake")


name_on_order = st.text_input("Name on Smoothie")
st.write('The name on your Smoothie will be:', name_on_order)

#session = get_active_session()
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

# Convert the Snowpark Dataframe to Pandas Dataframe so we can use the LOC function
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()


ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
      my_dataframe,
    max_selections = 5
)

if ingredients_list:
 
  ingredients_string = ''

  for fruit_chosen in ingredients_list:
      ingredients_string += fruit_chosen + ' '

      search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
      st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
    
      st.subheader(fruit_chosen + 'Nutrition Information')
      smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
      sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

 
  my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order+"""')"""

  st.write(my_insert_stmt)
  #st.stop()



time_to_insert = st.button ('Submit order')

if time_to_insert:
    st.write(my_insert_stmt)  # This line is indented correctly
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")







