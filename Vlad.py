import streamlit as st
import streamlit.components.v1 as components
import requests
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from map import get_map
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

st.plotly_chart(fig)


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
## I'm into **data science**

```bash
>> history | tail -n 5
```
'''

if st.checkbox('2021 - My Next Adventure?'):
    st.write('''
      I am open for work in Berlin or remotely. Scroll down to see **what I'm looking for.**
      ''')

if st.checkbox('2021 - Data Science Bootcamp @Le Wagon Berlin'):
    st.write('''
      Learning data science at Le Wagon Berlin
      has boosted my confidence and skills. I learned about machine learning,
      neural networks, and data engineering.
      For me the best part was learning how to structure and package
      Python code and how to build, deploy and monitor machine learning pipelines
      in the cloud.
      I also met a host of wonderful people, who have inspired me to keep striving.
      ''')

if st.checkbox('2020 - Mobility Research @One Health (Remote)'):
    st.write('''
      This project taught me the importance of writing flexible, reusable code.
      I analysed the impact of the pandemic lockdowns on Italian mobility in 2020.
      I had data on over 10 million trips from cellphone records (XDR).
      I programmed an algorithm that computed the difference in mobility from a
      baseline rate. Then I packaged the ETL pipeline in a Python library and wrote
      extensive documentation.
        ''')

if st.checkbox('2019 - Data Science for Social Good @ISI Foundation'):
    st.write('''
      Being at ISI felt like doing a PhD in one year.

      I studied the scientific response to COVID-19 and other epidemic emergencies.

      I collected data by scraping the web, calling APIs, and downloading a massive
      database of scientific publications from Amazon S3.

      I cleaned, preprocessed and transformed the data. I ran complex statistical
      anaylses. I surveyed the literature and reproduced complex algorithms. I worked
      with graphs and Markovian simulations.

      Finally, I wrote a paper and learned to make publication-ready plots.
        ''')


if st.checkbox('2018 - Social Network Analysis @Turin'):
    st.write('''
      As a sociology student, I was very excited about a course that taught
      Game Theory and Social Network Analysis. I had learned Python on my own,
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

html = f"<a href='{git_link}'><img src={img}></a>"
st.markdown(html, unsafe_allow_html=True)


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

st.text(f"The chi2 value is {round(chi2, 2)}, the p-value is {round(pval, 2)}")

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
map_ = get_map()

st.pydeck_chart(map_)

'''
### I speak 🇬🇧 🇮🇹 🇪🇸 🇩🇪 🇷🇴 🇫🇷
'''

'''
## Things that inspire me
[Effective Altruism](https://www.effectivealtruism.org/) |
[Deep Work](https://www.goodreads.com/book/show/25744928-deep-work) |
[There is no speed limit](https://sive.rs/kimo) |
[The Pragmatic Programmer](https://www.goodreads.com/book/show/4099.The_Pragmatic_Programmer)

I am passionate about teaching, especially when it involves breaking apart
difficult subjects.

My other passion is writing essays and poetry.

'''

'''
## What I'm looking for

I am **open to work** in Berlin or remotely.

I am looking for a place where I can be challenged to improve every day.
Team work and mentorship are very important to me.

I love building robust, scalable systems to retrieve, transform and analyse data.
I aspire to grow into the role of **Data Engineer**.

I am currently working on **Find Your Dream Job**, a tool that will allow job hunters
to gather job postings and extract insights on the job market. This is my final
project for the Le Wagon Data Science Bootcamp.

My next objective is to earn the **AWS Cloud Associate** certification.

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

