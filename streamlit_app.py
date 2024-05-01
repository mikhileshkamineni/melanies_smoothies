# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))

pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)

# Define the orders
orders = [
    ('Kevin', 'Apples, Lime, Ximenia', False, 7976616299844859825),
    ('Divya', 'Dragon Fruit, Guava, Figs, Jackfruit, Blueberries', True, -6112358379204300652),
    ('Xi', 'Vanilla Fruit, Nectarine', True, 1016924841131818535)
]

# Insert the orders into the database
for order in orders:
    name_on_order, ingredients, order_filled, hash_ing = order
    if ingredients:  # Ensure ingredients is not None or empty
        my_insert_stmt = "INSERT INTO ORDERS (name_on_order, ingredients, order_filled, hash_ing) VALUES (:1, :2, :3, :4)"
        params = [name_on_order, ingredients, order_filled, hash_ing]
        session.sql(my_insert_stmt, params).collect()

st.success('Orders have been created!', icon="✅")
