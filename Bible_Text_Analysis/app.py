import streamlit as st
import streamlit.components.v1 as stc

import pandas as pd
import neattext.functions as nfx
import random

import matplotlib
matplotlib.use("Agg")
import altair as alt

import utils

@st.cache
def load_bible(data):
    df_bible = pd.read_csv(data)
    return df_bible

from utils import (
    HTML_BANNER,
    HTML_RANDOM_TEMPLATE,
    render_text_entites,
    get_tags,
    tag_visualizer,
    plot_word_freq_with_altair,
    get_most_common_tokens,
)

def main():
     stc.html(HTML_BANNER)
     menu = ["HOME", "MULTIVERSE", "ABOUT"]
     df = load_bible("data/KJV_Bible.csv")

     choice = st.sidebar.selectbox("MENU", menu)
     if choice == "HOME":
         st.subheader("SINGLE VERSE SEARCH")
         book_list = df["book"].unique().tolist()
         book_name = st.sidebar.selectbox("BOOK", book_list)
         chapter = st.sidebar.number_input("CHAPTER", 1)
         verse = st.sidebar.number_input("VERSE", 1)
         bible_df = df[df["book"] == book_name]
         
         # Layout
         c1, c2 = st.columns([2, 1])
         
         # Single Verse Layout
         with c1:
             try:
                 selected_passage = bible_df[
                     (bible_df["chapter"] == chapter) & (bible_df["verse"] == verse)
                 ]
                 passage_details = "{}  Chapter:{}  Verse:{}".format(book_name, chapter, verse)
                 st.info(passage_details)
                 passage = "{}".format(selected_passage["text"].values[0])
                 st.write(passage)
             except:
                st.warning("Book Out Of Range")

         with c2:
             chapter_list = range(10)
             verse_list = range(20)
             ch_choice = random.choice(chapter_list)
             vs_choice = random.choice(verse_list)
             random_book_name = random.choice(book_list)
             
             rand_bible_df = df[df["book"] == random_book_name]

             try:
                 randomly_selected_passage = rand_bible_df[
                     (rand_bible_df["chapter"] == ch_choice)
                     & (rand_bible_df["verse"] == vs_choice)
                     ]
                 mytext = randomly_selected_passage["text"].values[0]
             except:
                 mytext = rand_bible_df[
                     (rand_bible_df["chapter"] == 1) & (rand_bible_df["verse"] == 1)
                 ]["text"].values[0]

             stc.html(HTML_RANDOM_TEMPLATE.format(mytext), height=300)

        # Search Topic/Term
         search_term = st.text_input("TERM/TOPIC")
         with st.expander("VIEW RESULTS"):
             retrieved_df = df[df["text"].str.contains(search_term)]
             st.dataframe(retrieved_df[["book", "chapter", "verse", "text"]])

     elif choice == "MULTIVERSE":
         st.subheader("MultiVerse Retrieval")
         book_list = df["book"].unique().tolist()
         book_name = st.sidebar.selectbox("Book", book_list)
         chapter = st.sidebar.number_input("Chapter", 1)
         bible_df = df[df["book"] == book_name]
         all_verse = bible_df["verse"].unique().tolist()
         verse = st.sidebar.multiselect("Verse", all_verse, default=1)
         selected_passage = bible_df.iloc[verse]
         st.dataframe(selected_passage)
         passage_details = "{} Chapter::{} Verse::{}".format(book_name, chapter, verse)
         st.info(passage_details)

         # Layout
         col1, col2 = st.columns(2)
         # Join all text as a sentence
         docx = " ".join(selected_passage["text"].tolist())

         with col1:
             st.info("Details")
             for i, row in selected_passage.iterrows():
                 st.write(row["text"])

         with col2:
             st.success("Bible Text analysis")
             with st.expander("Visualize Pos Tags"):
                 tagged_docx = get_tags(docx)
                 processed_tags = tag_visualizer(tagged_docx)
                 # st.write(processed_tags)# Raw
                 stc.html(processed_tags, height=1000, scrolling=True)

             with st.expander("Keywords"):
                 processed_docx = nfx.remove_stopwords(docx)
                 keywords_tokens = get_most_common_tokens(processed_docx, 5)
                 st.write(keywords_tokens)

             #with st.expander("Pos Tags Plot"):
                 #tagged_docx = get_tags(docx)
                 #tagged_df = pd.DataFrame(tagged_docx, columns=["Tokens", "Tags"])
                 # st.dataframe(tagged_df)
                 #df_tag_count = tagged_df["Tags"].value_counts().to_frame("counts")
                 #df_tag_count["tag_type"] = df_tag_count.index
                 # st.dataframe(df_tag_count)

                 #c = alt.Chart(df_tag_count).mark_bar().encode(x="tag_type", y="counts")
                 #st.altair_chart(c, use_container_width=True)

         with st.expander("Word Freq Plot"):
             plot_word_freq_with_altair(docx)

     else:
         
         st.subheader("ABOUT")
         st.text("BUILD WITH STREAMLIT")
         st.text("BY JESSICA OCHOA")
         st.success("Isaiah 41:10 - So do not fear, for I am with you; do not be dismayed, for I am your God. I will strengthen you and help you; I will uphold you with my righteous right hand.")

if __name__ == "__main__":
    main()