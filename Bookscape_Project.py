import requests
import mysql.connector
import random

def get_books(query, max_results=1000):
    api_key = "AIzaSyB_l2q_vtwMsLvh64501-EoJ_2BcSRduAA"  
    base_url = 'https://www.googleapis.com/books/v1/volumes'
    total_results = []

    for start_index in range(0, max_results, 40):
        url = f'{base_url}?q={query}&startIndex={start_index}&maxResults={min(40, max_results - start_index)}&key={api_key}'
        response = requests.get(url)

        if response.status_code == 200:
            books = response.json().get('items', [])
            total_results.extend(books)
        else:
            print(f"Error: {response.status_code} - {response.text}")
            break

    return total_results

def insert_books_into_db(books, search_key):
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

    dummy_publishers = ["Fictional House", "Imaginary Press", "Dummy Publishers Inc.", "Sample Books Ltd.", "Placeholder Publications"]

    for book in books:
        volume_info = book['volumeInfo']
        book_id = book.get('id', 'N/A')
        book_title = volume_info.get('title', 'No title available')
        book_subtitle = volume_info.get('subtitle', None)
        book_authors = ', '.join(volume_info.get('authors', ['No authors available']))
        
        # Use dummy publisher names if not available
        book_publishers = volume_info.get('publisher', random.choice(dummy_publishers))
        
        book_description = volume_info.get('description', None)
        industryIdentifiers = ', '.join([identifier['identifier'] for identifier in volume_info.get('industryIdentifiers', [])])
        text_readingModes = volume_info.get('readingModes', {}).get('text', False)
        image_readingModes = volume_info.get('readingModes', {}).get('image', False)
        pageCount = volume_info.get('pageCount', None)
        categories = ', '.join(volume_info.get('categories', []))
        language = volume_info.get('language', 'N/A')
        imageLinks = volume_info.get('imageLinks', {}).get('thumbnail', None)
        ratingsCount = volume_info.get('ratingsCount', 0)
        averageRating = volume_info.get('averageRating', 0.0)
        sale_info = book.get('saleInfo', {})
        country = sale_info.get('country', 'N/A')
        saleability = sale_info.get('saleability', 'N/A')
        isEbook = sale_info.get('isEbook', False)
        list_price = sale_info.get('listPrice', {})
        amount_listPrice = list_price.get('amount', None)
        currencyCode_listPrice = list_price.get('currencyCode', None)
        retail_price = sale_info.get('retailPrice', {})
        amount_retailPrice = retail_price.get('amount', None)
        currencyCode_retailPrice = retail_price.get('currencyCode', None)
        buyLink = sale_info.get('buyLink', None)

        try:
            mycursor.execute('''
                INSERT INTO books (book_id, search_key, book_title, book_subtitle, book_authors, book_publishers, book_description, industryIdentifiers,
                                  text_readingModes, image_readingModes, pageCount, categories, language, imageLinks, ratingsCount, averageRating,
                                  country, saleability, isEbook, amount_listPrice, currencyCode_listPrice, amount_retailPrice, currencyCode_retailPrice,
                                  buyLink)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (book_id, search_key, book_title, book_subtitle, book_authors, book_publishers, book_description, industryIdentifiers, text_readingModes,
                  image_readingModes, pageCount, categories, language, imageLinks, ratingsCount, averageRating, country, saleability, isEbook, amount_listPrice,
                  currencyCode_listPrice, amount_retailPrice, currencyCode_retailPrice, buyLink))
        except mysql.connector.errors.IntegrityError as e:
            print(f"IntegrityError: {e}")

    mydb.commit()
    mycursor.close()
    mydb.close()

# Example usage
books = get_books('science', max_results=1000)
insert_books_into_db(books, 'science')
