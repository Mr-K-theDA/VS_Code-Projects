import streamlit as st
import mysql.connector
import pandas as pd

# Function to execute SQL queries and return results as DataFrame
def query_db(query):
    mydb = mysql.connector.connect(
        host="gateway01.us-west-2.prod.aws.tidbcloud.com",
        port=4000,
        user="4Mh7uwfcjjxZn5F.root",
        password="yFIpQwQZrVaY6hMD",
        database="guvi",
        ssl_ca=r'C:/Users/remor/Downloads/isrgrootx1.pem',
        ssl_verify_cert=True 
    )
    mycursor = mydb.cursor()
    mycursor.execute(query)
    rows = mycursor.fetchall()
    colnames = [desc[0] for desc in mycursor.description]
    mycursor.close()
    mydb.close()
    return pd.DataFrame(rows, columns=colnames)

# Streamlit app
st.set_page_config(page_title="BookScape Explorer", layout="wide")

st.title("📚 BookScape Explorer")
st.markdown("Explore a variety of insights about books in the BookScape database")

# Sidebar for SQL queries
st.sidebar.header("Select a Query to Run")
queries = {
    "Check Availability of eBooks vs Physical Books": "SELECT isEbook, COUNT(*) AS count FROM books GROUP BY isEbook;",
    "Find the Publishers with the Most Books Published": "SELECT book_publishers, COUNT(*) AS count FROM books GROUP BY book_publishers ORDER BY count DESC LIMIT 1;",
    "Identify the Publishers with the Highest Average Rating": "SELECT book_publishers, AVG(averageRating) AS avg_rating FROM books GROUP BY book_publishers HAVING COUNT(*) > 10 ORDER BY avg_rating DESC LIMIT 1;",
    "Get the Top 5 Most Expensive Books by Retail Price": "SELECT book_title, amount_retailPrice FROM books ORDER BY amount_retailPrice DESC LIMIT 5;",
    "Find Books Published After 2010 with at Least 500 Pages": "SELECT book_title, year, pageCount FROM books WHERE year > '2010' AND pageCount >= 500;",
    "List Books with Discounts Greater than 20%": "SELECT book_title, amount_listPrice, amount_retailPrice, (amount_listPrice - amount_retailPrice) / amount_listPrice * 100 AS discount FROM books WHERE (amount_listPrice - amount_retailPrice) / amount_listPrice * 100 > 20;",
    "Find the Average Page Count for eBooks vs Physical Books": "SELECT isEbook, AVG(pageCount) AS avg_pageCount FROM books GROUP BY isEbook;",
    "Find the Top 3 Authors with the Most Books": "SELECT book_authors, COUNT(*) AS count FROM books GROUP BY book_authors ORDER BY count DESC LIMIT 3;",
    "List Publishers with More than 10 Books": "SELECT book_publishers, COUNT(*) AS count FROM books GROUP BY book_publishers HAVING COUNT(*) > 10;",
    "Find the Average Page Count for Each Category": "SELECT categories, AVG(pageCount) AS avg_pageCount FROM books GROUP BY categories;",
    "Retrieve Books with More than 3 Authors": "SELECT book_title, book_authors FROM books WHERE LENGTH(book_authors) - LENGTH(REPLACE(book_authors, ',', '')) + 1 > 3;",
    "Books with Ratings Count Greater Than the Average": "SELECT book_title, ratingsCount FROM books WHERE ratingsCount > (SELECT AVG(ratingsCount) FROM books);",
    "Books with the Same Author Published in the Same Year": "SELECT book_authors, year, COUNT(*) AS count FROM books GROUP BY book_authors, year HAVING COUNT(*) > 1;",
    "Books with a Specific Keyword in the Title": "SELECT book_title FROM books WHERE book_title LIKE '%keyword%';",
    "Year with the Highest Average Book Price": "SELECT year, AVG(amount_retailPrice) AS avg_price FROM books GROUP BY year ORDER BY avg_price DESC LIMIT 1;",
    "Count Authors Who Published 3 Consecutive Years": "SELECT book_authors, COUNT(DISTINCT year) AS count FROM books GROUP BY book_authors HAVING COUNT(DISTINCT year) >= 3;",
    "Authors Who Published Books in the Same Year but Under Different Publishers": "SELECT book_authors, year, COUNT(DISTINCT book_publishers) AS count FROM books GROUP BY book_authors, year HAVING COUNT(DISTINCT book_publishers) > 1;",
    "Average Retail Price of eBooks vs Physical Books": "SELECT AVG(CASE WHEN isEbook THEN amount_retailPrice ELSE NULL END) AS avg_ebook_price, AVG(CASE WHEN NOT isEbook THEN amount_retailPrice ELSE NULL END) AS avg_physical_price FROM books;",
    "Books with Ratings More Than Two Standard Deviations Away from the Average": "SELECT book_title, averageRating, ratingsCount FROM books WHERE ABS(averageRating - (SELECT AVG(averageRating) FROM books)) > 2 * (SELECT STDDEV(averageRating) FROM books);",
    "Publishers with the Highest Average Rating Among Its Books": "SELECT book_publishers, AVG(averageRating) AS average_rating, COUNT(*) AS num_books FROM books GROUP BY book_publishers HAVING COUNT(*) > 10 ORDER BY average_rating DESC LIMIT 1;"
}

selected_query = st.sidebar.selectbox("Select a query", list(queries.keys()))

if st.sidebar.button("Run Query"):
    df = query_db(queries[selected_query])
    st.dataframe(df)

    # Show query results as a table
    st.write(f"## Query Results for: {selected_query}")
    st.write(df)

    # Show query results as a chart if applicable
    if "count" in df.columns:
        st.bar_chart(df.set_index(df.columns[0])["count"])
    elif "avg_rating" in df.columns:
        st.bar_chart(df.set_index(df.columns[0])["avg_rating"])
    elif "avg_pageCount" in df.columns:
        st.bar_chart(df.set_index(df.columns[0])["avg_pageCount"])


# Footer
st.markdown("---")
st.markdown("Designed with ❤️ by Mr_K")
