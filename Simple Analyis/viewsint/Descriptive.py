import streamlit as st
from main import df
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time


def main():
    st.markdown(" ### Shape  ")
    shape = pd.DataFrame({"Rows": [df.shape[0]],
        "Columns" : [df.shape[1]]})
    datos = pd.DataFrame(df.dtypes)
    st.write(shape)
    st.markdown(" ### Data type  ")
    st.write(datos)

    df["SALE PRICE"] = df["SALE PRICE"].replace(" -  ",0).astype(float)
    df["YEAR BUILT"] = df["YEAR BUILT"].replace(" -  ",0).astype(int)
    

    #Graph    
    
    NEIGHBORHOOD = df.groupby(df["NEIGHBORHOOD"]).size().sort_values(ascending=False).head(10)
    st.markdown(" ##  TOP 10 Neighborhood")
    fig, ax = plt.subplots()
    NEIGHBORHOOD.plot(kind='barh',rot=0, color=['b'])


    st.pyplot(fig)
    
    
    YEAR1 = df.groupby(df["YEAR BUILT"]).size().sort_values(ascending=False).head(10)
    st.markdown(" ##  Top 10 Year Built")
    st.bar_chart(YEAR1)
    st.write("0 means that is not information about building year")


    st.markdown(" #  Data Explore")


    # Neighborhood Filter
    st.markdown(" ##  Neighborhood")
    neighborhoodselectors = st.selectbox("Neighborhood",(df["NEIGHBORHOOD"].unique()))
    datacount = (df["NEIGHBORHOOD"].values == neighborhoodselectors).sum()
    data = df[df["NEIGHBORHOOD"] == neighborhoodselectors]
    dataavg = round(data["SALE PRICE"].mean(),2)
    buildingclass = data.groupby(data["BUILDING CLASS CATEGORY"]).size().sort_values(ascending=False)


    st.write("There are",datacount,"sales")
    st.write("There avg sales prices is","${:,.2f}".format(dataavg),"dollars")
    st.write("Bulding Category",buildingclass)


    # Year Filter
    st.markdown(" ##  Construction date")
    year = df["YEAR BUILT"].unique()
    yearselectors = st.selectbox("Year Built",year)
    datayearcount = (df["YEAR BUILT"].values == yearselectors).sum()
    datayear = df[df["YEAR BUILT"] == yearselectors]
    dataavgyear = round(datayear["SALE PRICE"].mean(),2)
    buildingclassyear = datayear.groupby(datayear["BUILDING CLASS CATEGORY"]).size().sort_values(ascending=False)


    st.write("There are",datayearcount,"sales")
    st.write("There avg sales prices is","${:,.2f}".format(dataavgyear),"dollars")
    st.write("Bulding Category",buildingclassyear)
    

    

    



    


    





    


    

    
