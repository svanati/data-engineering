# Import python packages
import streamlit as st

# Set the title of the Streamlit app
st.title("My Parents New Healthy Diner")

# Write a description to the app
st.write(
    """**Choose the fruits you want in your custom Smoothie!**
        """
)

# # Input field for the name on the smoothie order
# name_on_order = st.text_input("Name on Smoothie:")
#
# # Display the name on the smoothie if provided
# if name_on_order:
#     st.write("The name on your Smoothie will be:", name_on_order)
#
# # Establish a connection to Snowflake
# connection_parameters = {
#     "account": "<your_account>",
#     "user": "<your_user>",
#     "password": "<your_password>",
#     "role": "<your_role>",
#     "warehouse": "<your_warehouse>",
#     "database": "<your_database>",
#     "schema": "<your_schema>",
# }
# session = Session.builder.configs(connection_parameters).create()
#
# # Retrieve the available fruit options from the Snowflake table
# my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
#
# # Multiselect widget for choosing up to 5 ingredients
# ingredients_list = st.multiselect(
#     "Choose up to 5 ingredients:", my_dataframe.collect(), max_selections=5
# )
#
# # Concatenate the chosen ingredients into a string
# ingredients_string = " ".join(ingredients_list)
#
# # SQL statement to insert the order into the Snowflake table
# my_insert_stmt = f"""insert into smoothies.public.orders(ingredients, name_on_order)
#                      values ('{ingredients_string}', '{name_on_order}')"""
#
# # Button to submit the order
# time_to_insert = st.button("Submit Order")
#
# # Insert the order into the Snowflake table and display a success message
# if time_to_insert:
#     session.sql(my_insert_stmt).collect()
#     st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")
