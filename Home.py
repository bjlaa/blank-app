import os
import streamlit as st

st.set_page_config(
    page_title="Climate change project",
    page_icon="🥵",
)

st.write("# Predicting climate change effect in France")
st.write("## Le Wagon, Data Science, Batch 1835")

st.markdown(
    """
    The goal of this project is to train an algorythm in order to predict the evolution of temperatures in France over the next 50 years.

    ### Current evolution
    
    
""", unsafe_allow_html=True
)

image_path = os.path.join(os.path.dirname(__file__), 'images', 'white trend.png')
st.image(image_path)