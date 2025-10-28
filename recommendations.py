# Import necessary libraries
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@st.cache_data
def load_data():
    df = pd.read_csv('/content/news_df.csv')
    return df

def recommend_articles(news_id, df):
    if news_id not in df['NewsID'].values:
        st.error("News ID not found in the dataset.")
        return None

    # Find the category of the given news_id
    category = df.loc[df['NewsID'] == news_id, 'Category'].values[0]
    st.write(f"**Detected Category:** {category}")

    # Filter only that category
    cat_df = df[df['Category'] == category].dropna(subset=['Content']).reset_index(drop=True)

    if cat_df.empty:
        st.warning("No content available for recommendation.")
        return None

    # TF-IDF Vectorization
    tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
    tfidf_matrix = tfidf.fit_transform(cat_df['Content'])

    # Find index of selected article
    idx = cat_df[cat_df['NewsID'] == news_id].index[0]

    # Compute cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()

    # Get top 5 similar articles (excluding itself)
    similar_indices = cosine_sim.argsort()[-6:-1][::-1]

    recommendations = cat_df.iloc[similar_indices][['NewsID', 'Title', 'URL']]
    return recommendations

def main():
    st.title("🧠 News Recommendation Engine")

    df = load_data()
    st.write("Enter a News ID to find similar articles:")

    news_id = st.text_input("News ID:")

    if st.button("Find Recommendations"):
        if news_id.strip() == "":
            st.warning("Please enter a valid News ID.")
        else:
            try:
                news_id = int(news_id)
            except:
                pass  # allow string IDs if they exist

            recs = recommend_articles(news_id, df)
            if recs is not None:
                # Make clickable URLs
                recs['URL'] = recs['URL'].apply(lambda x: f'<a target="_blank" href="{x}">{x}</a>')
                st.write(recs.to_html(escape=False, index=False), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
