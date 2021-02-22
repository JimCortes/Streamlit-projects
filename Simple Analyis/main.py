import streamlit as st
import numpy as np
import pandas as pd
import streamlit.components.v1 as stc 
from viewsint import Home
from viewsint import Descriptive
from viewsint import Second


st.title(f'NYC Property Sales')


dictypes = {

    "Home": Home,
    "General": Descriptive,
}



@st.cache(persist=True)
def load_data():
    data = pd.read_csv('nyc-rolling-sales.csv', index_col=0)
    return data

df = load_data()


def main():
    
    st.sidebar.title("NYC Property Analysis")
    st.sidebar.text("Descriptive")
    
    st.sidebar.title("Nav")
    analysis = st.sidebar.radio("Menu", list(dictypes.keys()))


    with st.spinner(f"Loading {analysis} ..."):
        dictypes[analysis].main()



if __name__ == "__main__":
    main()
