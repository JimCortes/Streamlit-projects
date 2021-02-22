import pandas as pd
import streamlit as st
import yfinance as yf
import streamlit.components.v1 as stc 
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np


title = """
<div style="font-size:60px;font-Verdana;background-color:#fff;text-align:center;">
		<span style='color:Red'>NETFLIX</span>
		
</div>

"""
df = pd.read_csv("netflix_titles.csv")
df['genere']=df['listed_in'].apply(lambda genere:genere.split(',')[0])
df['yearadded']=df['date_added'].apply(lambda date_added:str(date_added).split(',')[-1])



stc.html(title)

st.write(df)
st.write("There are rows: {} and columns: {}".format(df.shape[0],df.shape[1]))

st.markdown("# Type of Show")
fig, ax = plt.subplots(figsize=(7, 2))
labels = ['Movies', 'TV shows']
graphtype = df.groupby(df["type"]).size()
ax.pie(graphtype,labels = labels,autopct='%1.2f%%',startangle=70,textprops={'size': 'smaller'})
st.pyplot(fig)


st.markdown("## Ratings")

st.markdown("""
- TV-Y: Designed to be appropriate for all children
- TV-Y7: Suitable for ages 7 and up
- G: Suitable for General Audiences
- TV-G: Suitable for General Audiences
- PG: Parental Guidance suggested
- TV-PG: Parental Guidance suggested
- Teens PG-13: Parents strongly cautioned. May be Inappropriate for ages 12 and under.
- TV-14: Parents strongly cautioned. May not be suitable for ages 14 and under.
- R: Restricted. May be inappropriate for ages 17 and under.
- TV-MA: For Mature Audiences. May not be suitable for ages 17 and under.
- NC-17: Inappropriate for ages 17 and under

""")


st.markdown("## Ratings Movies")
ratingsize =  df.groupby([df["type"],df["rating"]]).size()

fig1, ax1 = plt.subplots(nrows=1,ncols=1, sharex=True, sharey=False, figsize=(11, 5))


ratingmovie = dict(ratingsize["Movie"].sort_values(ascending=False))
ax1.bar(list(ratingmovie.keys()),list(ratingmovie.values()), align='center')

st.pyplot(fig1)



st.markdown("## Ratings TV Shows")

fig2, ax2 = plt.subplots(nrows=1,ncols=1, sharex=True, sharey=False, figsize=(11, 5))


ratingshow = dict(ratingsize["TV Show"].sort_values(ascending=False))
ax2.bar(list(ratingshow.keys()),list(ratingshow.values()), align='center')

st.pyplot(fig2)


st.markdown("## Genere TV Show")

fig3, ax3 = plt.subplots(nrows=1,ncols=1, sharex=True, sharey=False, figsize=(11, 8))

generesize =  df.groupby([df["type"],df["genere"]]).size().sort_values(ascending=False)
genereshow = dict(generesize["TV Show"].sort_values())

ax3.barh(list(genereshow.keys()),list(genereshow.values()), align='center')
st.pyplot(fig3)


st.markdown("## Genere Movie")

fig4, ax4 = plt.subplots(nrows=1,ncols=1, sharex=True, sharey=False, figsize=(11, 8))

generesize =  df.groupby([df["type"],df["genere"]]).size().sort_values(ascending=False)
generemovie = dict(generesize["Movie"].sort_values())

ax4.barh(list(generemovie.keys()),list(generemovie.values()), align='center')
st.pyplot(fig4)

st.markdown("## Tv show / Movie added by year")
yearsize = df.groupby([df["yearadded"], df['type']]).size().unstack().fillna(0)
fig5, ax5 = plt.subplots(nrows=1,ncols=1, figsize=(11, 8))
moviesize, tvshowsize = yearsize['Movie'], yearsize['TV Show']
ax5.bar(moviesize.index, moviesize,label='Movie')
ax5.bar(tvshowsize.index, tvshowsize, bottom=moviesize, label='TV Show')
ax5.legend()


st.pyplot(fig5)


