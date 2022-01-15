from cProfile import label
from turtle import width
import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import plotly.express as px
from difflib import get_close_matches
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt


st.markdown("<h1 style='text-align: center; color: blue;'>There is no friend as loyal as a book!</h1>", unsafe_allow_html=True)
img = Image.open("Boy-looking-at-Books.jpg")
st.image(img, width=700)

df = pd.read_csv('1000_books.csv', index_col=0)
# ['Titles', 'Authors', 'Published year', 'Places', 'Pages', 'Series', 'Awards','The Number of awards',
#                       'Reviews', 'Votes', 'Number of rated people', 'Average rating','Urls']
df["mean_norm_ratings"] = 1 + (((df["Average rating"]-df["Average rating"].mean())/(df["Average rating"].max() - df["Average rating"].min())) *9)
df["minmax_norm_ratings"] = 1 + ((df["Average rating"] - df["Average rating"].min())/(df["Average rating"].max() - df["Average rating"].min()) *9)
# df = df.astype(dict.fromkeys(df.columns[8:9], bool))


data_ = st.sidebar.radio(
     label="Do you want to see the whole data?",
     options=("No",'Yes'))

if data_ == 'Yes':
    st.markdown("<h1 style='text-align: center; color: white;'>The top 1000 books!</h1>", unsafe_allow_html=True)
    st.dataframe(df.style.highlight_max(axis=0))
    # st.dataframe(df.style.highlight_max(axis=0))
path = st.sidebar.text_input('Search for your book!!!')
if path:
    matches = list(get_close_matches(path, df['Titles'].values))
    st.text('That is the best choice!')
    st.dataframe((df.loc[df['Titles'].isin(matches)]).style.highlight_max(axis=0))

st.sidebar.subheader("Choose the top books")
top_book_ = st.sidebar.selectbox(
    label ="Select the top books",
    options = [5, 10, 20, 50, 100])
                            

st.sidebar.subheader("Choose the tops by...")
top_book_sel =st.sidebar.selectbox(
    label ="Select the top books",
    options =['The Number of awards','Reviews', 'Votes', 'Average rating',
       'Number of rated people','Pages'])


df_sorted = df.sort_values(by=[top_book_sel], ascending=False)
                           
confirm = st.sidebar.checkbox('confirm')
if confirm:
    st.text('Your top books!!!')
    st.dataframe(df_sorted.head(top_book_).style.highlight_max(axis=0))

st.sidebar.subheader("Description data")
show = st.sidebar.checkbox('SHOW')
if show:
    st.write(df.describe())
    vote = df.groupby("Years").agg({'minmax_norm_ratings': ['mean']})
    st.dataframe(vote.style.highlight_max(axis=0))

st.sidebar.subheader("Analyzing data by...")
Talvinder = st.sidebar.selectbox(
                label = 'Select the books number',
                options = [5, 10, 20, 50, 100])

if Talvinder==20:
    st.text('What are the top 20 books at the moment?')
    top_twenty = df.head(20)
    st.dataframe(top_twenty.style.highlight_max(axis=0))

    st.text('This graph shows the correlation between the top 20 books in order in comparison to its reviews')
    fig = px.bar(top_twenty, x="Titles", y="Reviews")
    # fig_widget = go.FigureWidget(fig)
    fig.update_layout(width=800, height=800)
    st.write(fig)

    st.text('This graph shows the relationship between the top 20 book compared to the number of people who voted')
    fig1 = px.bar(top_twenty, x="Titles", y="Number of rated people")
    fig1.update_layout(width=800, height=800)
    st.write(fig1)

    st.text('This table focuses purely on the 2 books which had very low votes')
    underated = top_twenty[top_twenty["Titles"].isin(['The Chronicles of Narnia (Chronicles of Narnia, #1-7)', 'J.R.R. Tolkien 4-Book Boxed Set: The Hobbit and The Lord of the Rings'])]
    b = underated[['Titles', 'Series', 'Published year', 'The Number of awards', 'Number of rated people']]
    st.dataframe(b.style.highlight_max(axis=0))

    st.text('This table shows the amount of people voting for books for each book based on the year it weas published')
    years = top_twenty.groupby('Published year').agg({'Number of rated people': ['mean']})
    st.dataframe(years.style.highlight_max(axis=0))

    st.text('This table shows the amount of reviews for each book based on the year it weas published')
    years_data = top_twenty[['Published year', 'Reviews']]
    sorted_years = years_data.sort_values(['Published year'], ascending=False)
    st.dataframe(sorted_years.style.highlight_max(axis=0))

    st.text('This graph compares the Reviews recieved for each published year')
    fig3 = px.line(sorted_years, x='Published year', y="Reviews")
    fig3.update_layout(width=800, height=600)
    st.write(fig3)

    st.text('This graph is portraying the awards each book has recieved')
    fig2 = px.bar(top_twenty, x="Titles", y="The Number of awards")
    fig2.update_layout(width=800, height=800)
    st.write(fig2) 
    
Vishwa = st.sidebar.checkbox('Analyzing')
if Vishwa:
    # st.text('checking the Author column containing the numerice values count')
    df.Authors.str.contains(r'[0-9]').value_counts()
    df['Average rating'] = pd.to_numeric(df['Average rating'],errors = 'coerce')
    df['minmax_norm_rating'] = 1 + (df['Average rating'] - df['Average rating'].min()) / (df['Average rating'].max() - df['Average rating'].min()) * 9

    st.text('Comparision between highest and lowest vs average')
    img = Image.open("output1.png")
    st.image(img, width=700)

    years_data = df[['Published year', 'Average rating']]
    sorted_years = years_data.sort_values(['Published year'], ascending=False)
    
    ac = px.scatter(sorted_years, x='Published year',
    y='Average rating'
            )
    st.write(ac)

    fig, ax = plt.subplots(figsize=(10,8))
    plt.boxplot(df['The Number of awards'])
    plt.xticks(fontsize=14, rotation=45)
    plt.yticks(fontsize=14)
    plt.xticks()
    plt.ylabel("Awards", fontsize=20)
    plt.title('Awards distribution', fontsize=20)
    plt.grid(True,linestyle='dashed')
    ax.set_xticks([])
    q = px.box(df['The Number of awards'])
    st.write(q)

    img1 = Image.open("output.png")
    st.image(img1, width=700)

    img2 = Image.open('graph4.png')
    st.image(img2, width=700)


about = st.sidebar.button("contributors")
if about:
    st.title("Fayyozjon Usmonov")
    st.title("Vishwanath Singa")
    st.title("Talvinder Singh Johal")
    st.markdown("<h1 style='text-align: center; color: blue;'>Thanks for your attention!</h1>", unsafe_allow_html=True)
    img2 = Image.open('12.png')
    st.image(img2, width=300)