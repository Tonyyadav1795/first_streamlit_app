import streamlit as st
import pandas as pd
import requests
import snowflake.connector

# Changed title as per the image instruction
st.title('View Our Fruit List')

st.header('Breakfast Menu')
st.text('🥣Omega 3 & Blueberry Oatmeal')
st.text('🥗Kale, Spinach & Rocket Smoothie')
st.text('🐔Hard-Boiled Free-Range Egg')
st.text('🥑🍞Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Assuming fruit_macros.txt is a CSV file with a 'Fruit' column
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page
st.dataframe(fruits_to_show)

# Function to get data from Fruityvice API
def get_fruityvicedata(this_fruit_choice):
    fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{this_fruit_choice}")
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

st.header('Fruityvice Fruit Advice!')
fruit_choice = st.text_input('What fruit would you like information about?')
if fruit_choice:
    back_from_function = get_fruityvicedata(fruit_choice)
    st.dataframe(back_from_function)

# Connect to Snowflake
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])

# Function to get fruit load list from Snowflake
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM fruit_load_list")
        return my_cur.fetchall()

# Function to insert a new fruit into Snowflake
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values (%s)", (new_fruit,))
        return f"Thanks for adding {new_fruit}"

# Add a button to load the fruit list
# Changed button label as per the image instruction
if st.button('Add Your Favorites'):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    st.dataframe(my_data_rows)

# Input for adding a new fruit
add_my_fruit = st.text_input('What fruit would you like to add?')
if st.button('Add a Fruit to the List') and add_my_fruit:
    back_from_function = insert_row_snowflake(add_my_fruit)
    st.text(back_from_function)

# Adding new fruits as specified
insert_row_snowflake("jackfruit")
insert_row_snowflake("papaya")
insert_row_snowflake("guava")
insert_row_snowflake("kiwi")

# Close the Snowflake connection
my_cnx.close()
