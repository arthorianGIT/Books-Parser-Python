import requests
from dotenv import load_dotenv
import os
import csv
import json

load_dotenv('.env')
api_key = os.getenv('api_key')

def parser(criteria: str, key_word: str):
    params = {}
    user_key = input('Wanna add your api key to this soft? (yes, no): ')
    if user_key.lower().strip() == 'yes':
        user_api_key = input('Paste here your api key: ')
        with open('.env', 'w') as file:
            file.write(f"api_key='{user_api_key}'")
        print('Now reuse a soft with your key ^)')
    else:
        global api_key
        params['key'] = api_key
        params['q'] = f'{criteria}:{key_word}'

        response = requests.get('https://www.googleapis.com/books/v1/volumes', params=params)

        if response.status_code == 200:
            data = response.json()
            for number, book in enumerate(data['items']):
                print('-' * 10)
                print(f'{number + 1}: {book['volumeInfo']['title']}')
            print('-' * 10)
            choice_book = int(input('Please choice a book from titles: '))
            print('-' * 10)
            print(f'Title: {data['items'][choice_book - 1]['volumeInfo']['title']}')
            print(f'Authors: {', '.join(data['items'][choice_book - 1]['volumeInfo']['authors'])}')
            print(f'Publish date: {data['items'][choice_book - 1]['volumeInfo']['publishedDate']}')
            print('-' * 10)

            save_choice = input('Do you want to save info? (yes, no) ').lower().strip()

            if save_choice == 'yes':
                book_data = {
                    'Title': data['items'][choice_book - 1]['volumeInfo']['title'],
                    'Authors': ', '.join(data['items'][choice_book - 1]['volumeInfo']['authors']),
                    'Publish date': data['items'][choice_book - 1]['volumeInfo']['publishedDate']
                }
                while True:
                    print('1: Json')
                    print('2: Csv')
                    file_choice = int(input('Choose format from given: '))

                    if file_choice == 1:
                        try:
                            with open('saved-books.json', 'r') as file:
                                books = json.load(file)
                        except FileNotFoundError:
                            books = []
                        
                        books.append(book_data)

                        with open('saved-books.json', 'w') as file:
                            json.dump(books, file, indent=4)

                        print('Successfuly saved!')
                        break
                    elif file_choice == 2:
                        try:
                            with open('saved-books.csv', 'r') as file:
                                content = csv.reader(file)
                                books = list(content)
                        except FileNotFoundError:
                            books = []
                        
                        books.append([data['items'][choice_book - 1]['volumeInfo']['title'],
                                    ', '.join(data['items'][choice_book - 1]['volumeInfo']['authors']),
                                    data['items'][choice_book - 1]['volumeInfo']['publishedDate']])
                        
                        with open('saved-books.csv', 'w', newline='') as file:
                            writer = csv.writer(file)
                            for row in books:
                                writer.writerow(row)

                        print('Successfuly saved!')
                        break
                    else:
                        print('Not right choice, choose from menu')
                        continue
            else:
                print('Exiting...')
        else:
            print(f'Error: {response.status_code}')

criteria = input('Your choice of criteria? (Title, Author, Publisher, Subject): ').lower().strip()

if criteria == 'title':
    key_word = input('Enter a key word title: ')
    parser('intitle', key_word)
elif criteria == 'author':
    key_word = input('Enter a key word author: ')
    parser('inauthor', key_word)
elif criteria == 'publisher':
    key_word = input('Enter a key word publisher: ')
    parser('inpublisher', key_word)
elif criteria == 'subject':
    key_word = input('Enter a key word subject: ')
    parser('subject', key_word)