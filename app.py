# Import necessary libraries
import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('/content/news_df.csv')
    return df

# Main function
def main():
  st.title('📰 News Finder App')

  df = load_data()

  # Ensure columns exist
  required_cols = ['Category', 'SubCategory', 'NewsID', 'Title', 'URL']
  if not all(col in df.columns for col in required_cols):
      st.error("Required columns are missing in the DataFrame.")
      return

  # Sidebar filters
  st.sidebar.header('Filter Options')

  # Category selection
  categories = sorted(df['Category'].unique())
  selected_category = st.sidebar.selectbox('Select Category', categories)

  # SubCategory selection
  subcategories = sorted(df[df['Category'] == selected_category]['SubCategory'].unique())
  selected_subcategory = st.sidebar.selectbox('Select SubCategory', subcategories)

  # Filter data
  filtered_df = df[(df['Category'] == selected_category) & (df['SubCategory'] == selected_subcategory)]

  st.subheader(f'Results for {selected_category} → {selected_subcategory}')
  st.write(f"Total results: {len(filtered_df)}")

  # Display table
  if not filtered_df.empty:
    # Create clickable links for the URL column
    def make_clickable(val):
        return f'<a target="_blank" href="{val}">{val}</a>'

    # Apply the function to the URL column
    filtered_df['URL'] = filtered_df['URL'].apply(make_clickable)

    # Display the DataFrame as HTML to render the links
    st.write(filtered_df[['NewsID', 'Title', 'URL']].to_html(escape=False, index=False), unsafe_allow_html=True)
  else:
      st.warning('No results found.')

if __name__ == '__main__':
  main()
