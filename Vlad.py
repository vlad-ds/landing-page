import streamlit as st
import streamlit.components.v1 as components
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from maps import get_folium_map
from streamlit_folium import folium_static
from scipy import stats
import random


'''
# Hi, I'm Vlad.
### Let's [work together](mailto:vlad.datasci@gmail.com).
___
'''

'''
## Let's start with the most important thing...
'''

from mentions import get_mentions, plot_mentions

dogs = get_mentions('dogs')
cats = get_mentions('cats')
dogs_mentions = dogs['mentions']
cats_mentions = cats['mentions']
dates = [x[0] for x in dogs_mentions]
dates = [x[0] for x in dogs_mentions]

import plotly.graph_objects as go

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=dates,
    y=[x[1] for x in dogs_mentions],
    name = 'Dogs', # Style name/legend entry with html tags
    connectgaps=True, # override default to connect the gaps
))
fig.add_trace(go.Scatter(
    x=dates,
    y=[x[1] for x in cats_mentions],
    name='Cats',
    connectgaps=True
))

fig.update_layout(title='Cats vs. Dogs in News Headlines (Past 15 days)',
                   xaxis_title='Day',
                   yaxis_title='Headlines',
                   template='ggplot2')

st.plotly_chart(fig, use_container_width=True)


topic = st.radio('Random headline', ('cats', 'dogs'))
if topic == 'cats':
  title, url = random.choice(cats['headlines'])
  st.write(f'''[{title}]({url})''')
else:
  title, url = random.choice(dogs['headlines'])
  st.write(f'''[{title}]({url})''')

'''Source: [NewsAPI](https://newsapi.org/)'''

'''
## Now that we got *that* out of the way, I can tell you a few things about me.
'''

'''
## I'm into **Data Engineering**

```bash
>> history | tail -n 5
```
'''

if st.checkbox('🪐 2021 - My Next Adventure?', value=1):
    st.write('''
      I am open for work in Berlin or remotely. Scroll down to see **what I can offer**.
      ''')

if st.checkbox('💻 2021 - Data Science Bootcamp @Le Wagon Berlin', value=0):
    st.write('''
      For my final project, I am collaborating with my teammates
      to build **Find Your Dream Job**, a tool that allows job hunters to analyse job postings
      and gain insights on the job market. After co-creating and pitching the project,
      my contributions include:

      * Scraping job offers with **Selenium Web Driver**
      * Converging data sources into an **SQL** database
      * Designing the **ETL pipeline** to automate extraction, processing and analysis
      * **Packaging** and **refactoring** our code (including NLP algorithms)
      * Deploying the backend with **Docker** and **Google Cloud Platform**
      * Designing the API with **FastAPI** and connecting it to the frontend

      I also met a host of wonderful people who have inspired me to keep learning and striving.
      ''')

if st.checkbox('🚅 2020 - Mobility Research @One Health (Remote)'):
    st.write('''
      This project taught me the importance of writing flexible, reusable code.
      I analysed the impact of the pandemic lockdowns on Italian mobility in 2020.
      I managed data on over 10 million trips from cellphone records (XDR).
      I programmed an algorithm that computed the difference in mobility from a
      baseline rate. Then I packaged the **ETL pipeline** in a **Python** library and wrote
      extensive **documentation**.
        ''')

if st.checkbox('📊 2019 - Data Science for Social Good @ISI Foundation'):
    st.write('''
      Being at ISI felt like doing a whole PhD in one year.

      I studied the scientific response to COVID-19 and other epidemic emergencies.

      I collected data by scraping the web, calling APIs, and using **MongoDB** to
      manage a massive database of scientific publications.

      I cleaned, preprocessed and transformed the data. I ran complex statistical
      anaylses. I surveyed the literature and reproduced complex algorithms. I worked
      with graphs and Markovian simulations.

      Finally, I wrote a paper and learned to make publication-ready plots.
        ''')


if st.checkbox('🧑🏻‍🤝‍🧑🏻  2018 - Social Network Analysis @Turin'):
    st.write('''
      As a sociology student, I was very excited about a course that taught
      Game Theory and **Social Network Analysis**. I had learned **Python** on my own,
      and now was the perfect chance to apply it.

      I met a professor who had gathered data on the social interactions of
      his students over three years. We reconstructed their networks and found
      clear evidence of the impact of network position on academic performance.

      After graduation, I received a grant to complete this project.
      I also interned in a data consultancy
      company where I worked on surveying and reconstructing employee relations.
        ''')

img = 'https://i.ibb.co/sPkpLk8/Screenshot-from-2021-02-27-15-05-17.png'
git_link = 'https://github.com/vlad-ds'

st.write("## I love **programming**")
st.markdown("[My Github](https://github.com/vlad-ds).")

'''
My projects include:

* [**Find Your Dream Job**](https://github.com/mizzle-toe/find-your-dream-job). Automatically extract,
store and analyse job offers. Use NLP techniques to find relevant job postings and identify skill
requirements.
* [**Spotify History**](https://github.com/vlad-ds/spoty-records). Extract your Spotify streaming history.
Use the Spotify API to obtain song features.
* [**Glasdoor Job Scraper**](https://github.com/vlad-ds/glassdoor-scrape). With Selenium Web Driver.
* [**Poetry Website**](https://lines-in-the-water.herokuapp.com/). A Node & Express app to store my poetry.
'''

#st.image('https://i.ibb.co/sPkpLk8/Screenshot-from-2021-02-27-15-05-17.png')


'''
## I use **statistics** to understand the world
'''
wj = st.number_input(label='Smokers who jog (out of 100)', min_value=1, max_value=100, step=1, value=50)
mj = st.number_input(label='Non-smokers who jog (out of 100)', min_value=1, max_value=100, step=1, value=50)

df_chi = pd.DataFrame({
  "Jog": [wj, mj, wj+mj],
  "Don't jog": [100-wj, 100-mj, (100-mj + 100-wj)],
  "Total": [100, 100, 200]
  },
  index=['Smokers', 'Non-smokers', 'Total'])

df_chi_red = df_chi.iloc[:-1, :-1]


df_chi_exp = pd.DataFrame({
  "Jog": [0, 0],
  "Don't jog": [0, 0]
  }, index=['Smokers', 'Non-smokers'])

df_chi_exp.iloc[0, 0] = df_chi.loc['Smokers', 'Total'] * df_chi['Jog'][-1] / 200
df_chi_exp.iloc[0, 1] = df_chi.loc['Smokers', 'Total'] * df_chi["Don't jog"][-1] / 200
df_chi_exp.iloc[1, 0] = df_chi.loc['Non-smokers', 'Total'] * df_chi['Jog'][-1] / 200
df_chi_exp.iloc[1, 1] = df_chi.loc['Non-smokers', 'Total'] * df_chi["Don't jog"][-1] / 200

df_chi

chi2 = ((df_chi_exp - df_chi_red)**2 / df_chi_exp).sum().sum()
pval = 1 - stats.chi2.cdf(chi2, 1)
p_display = str(round(pval, 2)) if pval >= .01 else "< 0.01"

st.text(f"The chi2 value is {round(chi2, 2)}, the p-value is {p_display}")

verdict = 'related' if pval < .05 else 'unrelated'

st.markdown(f"At 95% significance level, smoking and jogging seem to be **{verdict}**!")


'''
## I'm always learning new things...
'''

df = pd.DataFrame({
  'Course': ['Data Science Bootcamp', 'Full Stack Developer Bootcamp',
            'MySQL Bootcamp', 'Tableau Fundamentals', 'Java Summer Course'],
  'School': ['Le Wagon Berlin', 'FreeCodeCamp', 'Udemy', 'Visualitics', 'ForIT'],
  }, index=[2021, 2020, 2020, 2019, 2017])

df

'''
## I've lived in a few places
'''

#m = get_folium_map()
#folium_static(m, width=500)
st.image('https://i.ibb.co/0QnXVx4/Screenshot-from-2021-03-06-14-41-24.png')

'''
### I speak 🇬🇧 🇮🇹 🇪🇸 🇩🇪 🇷🇴 🇫🇷
'''

'''
## Things that inspire me
[Effective Altruism](https://www.effectivealtruism.org/) | [There is no speed limit](https://sive.rs/kimo) |
[The Pragmatic Programmer](https://www.goodreads.com/book/show/4099.The_Pragmatic_Programmer) |
[Deep Work](https://www.goodreads.com/book/show/25744928-deep-work)

I am passionate about teaching, especially when it involves breaking apart
difficult subjects.

I write essays and poetry.
'''

'''
## What I can offer

I am **open to work** in Berlin or remotely.

I am looking for a place where I can be challenged to improve every day.
Team work and mentorship are very important to me.

I love building robust and scalable systems to retrieve, transform and analyse data.
I aspire to grow into the role of **Data Engineer**.

I am currently working on [**Find Your Dream Job**](https://github.com/mizzle-toe/find-your-dream-job),
a tool that will allow job hunters to gather job postings and extract insights on the job market. This is my final
project for the Le Wagon Data Science Bootcamp. [Stay tuned](mailto:vlad.datasci@gmail.com)!

My next objective is to earn the **AWS Certified Developer** certification.

'''

'''
## Get in touch!

[Email](mailto:vlad.sci@gmail.com) |
[LinkedIn](https://www.linkedin.com/in/vlad-ds/) |
[Github](https://github.com/vlad-ds)

'''

#################
#    SIDEBAR    #
#st.sidebar.write('Hello world')
#################

