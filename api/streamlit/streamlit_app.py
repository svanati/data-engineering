# Import python packages
import requests
import streamlit as st

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!")

st.write(
        """**Choose the fruits you want in your custom Smoothie!**
                """
)

name_on_order = st.text_input("Name on Smoothie:")

if name_on_order:
    st.write("The name on your Smoothie will be:", name_on_order)

if ingredients_list:
        ingredients_list = ''

        for fruit_chosen in ingrediants_list:
                smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
                sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
