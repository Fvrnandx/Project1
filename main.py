import json
import requests
import main_functions
import nltk
import streamlit as st
import pandas as pd
import numpy as np
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.probability import FreqDist
from wordcloud import WordCloud
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import plotly.express as px



st.title("Project 1")
st.header("Part A - the stories API")
st.text("This app uses the Top Stories API to display the most common words used")
st.text("in the top current articles based on a specified topic selected by the user")
st.text("The data is displayed as a line chart and as a wordcloud image.")
st.header("I - Topic Selection")

full_name = st.text_input("Enter name")
topics = st.selectbox("Pick a topic.",
                      ["", "arts", "automobiles", "books", "business", "fashion", "food", "health",
                       "home", "insider", "magazine", "movies", "ny region", "obituaries", "opinion",
                       "politics", "real estate", "science", "sports", "sunday review", "technology",
                       "theater", "t-magazine", "travel", "upshot", "us", "world"])
if full_name and topics:
    api_key_dict = main_functions.read_from_file("json_files/api_key.json")
    api_key = api_key_dict["my_key"]

    url = "https://api.nytimes.com/svc/topstories/v2/" + topics +".json?api-key=" + api_key
    response = requests.get(url).json()
    main_functions.save_to_file(response, "json_files/response.json")
    results = main_functions.read_from_file("json_files/response.json")

    firststring = ""
    for i in results["results"]:
        firststring = firststring + i["abstract"]

        words = word_tokenize(firststring)
        no_punc = []
        for w in words:
            if w.isalpha():
                no_punc.append(w.lower())


    fdist2 = FreqDist(no_punc)

    stopword = stopwords.words('english')
    clean_words = []

    for w in no_punc:
        if w not in stopword:
            clean_words.append(w)

        fdist3 = FreqDist(clean_words)



    st.text("Hi {}".format(full_name) + " you selected the {} topic.".format(topics))
    st.subheader("II - Frequency Distribution")

    if st.checkbox("Click here to generate Frequency Distribution"):
        common_wrds = pd.DataFrame(fdist3.most_common(10))
        df = pd.DataFrame({"words": common_wrds[0],
                           "count": common_wrds[1]})
        chart = px.bar(df, x="words",
                      y="count",
                      title='')
        st.plotly_chart(chart)

    st.subheader("III - Word Cloud")
    if st.checkbox("Click here to generate wordcloud"):
        display_word_box = WordCloud().generate(firststring)
        plt.figure(figsize=(12, 12))
        plt.imshow(display_word_box)
        plt.axis("off")
        plt.show()
        st.pyplot()
        st.set_option('deprecation.showPyplotGlobalUse', False)


st.header("Part B - Most Popular Articles")
st.text("Select if you want to se the most shared, emailed, or view articles")

set_of_articles = st.selectbox("Select your preferred set of articles",
             ['','shared','emailed','viewed'])

period_of_time = st.selectbox("Select the period of time (last days)",
             ['','1','7','30'])

if set_of_articles and period_of_time:
    api_key_dict = main_functions.read_from_file("json_files/api_key.json")
    api_key = api_key_dict["my_key"]

    secondurl = "https://api.nytimes.com/svc/mostpopular/v2/" + set_of_articles + "/" + period_of_time + ".json?api-key=" + api_key
    popular_articles = requests.get(secondurl).json()
    main_functions.save_to_file(popular_articles, "json_files/popular_articles.json")
    outcome = main_functions.read_from_file("json_files/popular_articles.json")

    secondstring = ""
    for i in outcome["results"]:
        secondstring = secondstring + i["abstract"]

        words = word_tokenize(secondstring)
        no_punct = []
        for w in words:
            if w.isalpha():
                no_punct.append(w.lower())

    fdist2 = FreqDist(no_punct)

    stopword = stopwords.words('english')
    clean_words = []

    for w in no_punct:
        if w not in stopword:
            clean_words.append(w)

        fdist3 = FreqDist(clean_words)


    display_word_box = WordCloud().generate(secondstring)
    plt.figure(figsize=(12, 12))
    plt.imshow(display_word_box)
    plt.axis("off")
    plt.show()
    st.pyplot()
    st.set_option('deprecation.showPyplotGlobalUse', False)



