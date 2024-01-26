#Run in command prompt for better results (os.system('cls') may not work properly in some interpreters)
#Install the necessary modules before running the program.

from tabulate import tabulate
import isbnlib
import math
import os
import sys
import time


#Book Details
class Book:
    def __init__(self, ISBN, Book_Title, Book_Type, Quantity):
        self.ISBN = ISBN
        self.Book_Title = Book_Title
        self.Book_Type = Book_Type
        self.Quantity = Quantity


class Library_Management_System:
    def __init__(self):
        self.books = []

    #Create possible actions in the Library Management System
    def search_books(self, ISBN_list):
        headers = ["ISBN", "Book Title", "Type of Book", "Quantity Available"]
        if len(ISBN_list) != 0:
            books_data = [[book.ISBN, book.Book_Title, book.Book_Type, book.Quantity] for book in self.books if book.ISBN in ISBN_list]
            table_format = tabulate(books_data, headers, tablefmt="grid")
            print(table_format)
        else:
            print("No books are searched.")

    def view_books(self, sort_by, books):
        if books:
            headers = ["ISBN", "Book Title", "Type of Book", "Quantity Available"]
            sorted_books = sorted(books, key=lambda x: getattr(x, ["ISBN", "Book_Title", "Book_Type", "Quantity"][sort_by-1]))
            books_data = [[book.ISBN, book.Book_Title, book.Book_Type, book.Quantity] for book in sorted_books]
            table_format = tabulate(books_data, headers, tablefmt="grid")
            print(table_format)

    def add_book(self, new_book):
        self.books.append(new_book)

    def update_book_details(self, chosen_ISBN, Change_ISBN, Change_Title, Change_Type, Change_Quantity):
        for book in self.books:
            if book.ISBN == chosen_ISBN:
                book.ISBN = Change_ISBN if Change_ISBN is not None else book.ISBN
                book.Book_Title = Change_Title if Change_Title is not None else book.Book_Title
                book.Book_Type = Change_Type if Change_Type is not None else book.Book_Type
                book.Quantity = Change_Quantity if Change_Quantity is not None else book.Quantity
                break

    def remove_book(self, chosen_ISBN=None):
        self.books = [book for book in self.books if book.ISBN != chosen_ISBN]


#Error message for invalid inputs
def get_user_input(message, input_type):
    while True:
        user_input = input(message).strip()
        if input_type(user_input):
            return user_input
        print("\n\nInvalid input! Try again...")


#Main User interface
def perform_action(system):
    while True:
        action = get_user_input(
            '''The following actions may be performed in the system:
1. Search specific book(s)
2. View all books
3. Add new book(s)
4. Update existing book(s)
5. Remove existing book(s)

Choose an action (1/2/3/4/5): ''', lambda x: x in ['1', '2', '3', '4', '5'])

        os.system('cls')

        if action == '1':
            perform_book_search(system)
        elif action == '2':
            perform_view_books(system)
        elif action == '3':
            perform_add_book(system)
        elif action == '4':
            perform_update_book(system)
        elif action == '5':
            perform_remove_book(system)

        time.sleep(2)
        move_on = get_user_input("Would you like to perform more actions in the system (y/n)? ", lambda x: x.lower() in ['y', 'n'])

        if move_on == 'n':
            sys.exit()
        os.system('cls')


#Search book(s)
def perform_book_search(system):
    ISBN_list = []
    while True:
        print("Current ISBN Search List:", ', '.join(ISBN_list) if ISBN_list else "None")

        ISBN = get_user_input("Key in the ISBN of the book you would like to search: ", lambda x: (isbnlib.is_isbn10(x) == True or isbnlib.is_isbn13(x) == True))

        if ISBN in [book.ISBN for book in system.books]:
            if ISBN not in ISBN_list:
                ISBN_list.append(ISBN)
                print()
            else:
                print("\nISBN already exists in the search list!\n")
        else:
            print("\n\nThis ISBN does not exist in the system!\n")
            
        more = get_user_input("Would you like to search for more books (y/n)? ", lambda x: x.lower() in ['y', 'n'])
        if more == 'n' or more == 'N':
            os.system('cls')
            if len(ISBN_list) != 0:
                print("Shown below is a table filled with selected book(s):\n")
            system.search_books(ISBN_list)
            break
        elif more == 'y' or more == 'Y':
            os.system('cls')


#View all books
def perform_view_books(system):
    while True:
        books = system.books
        if len(books) != 0:
            sort_by = get_user_input(
                '''Shown below are ways in which the books can be sorted:
1. ISBN
2. Book Title
3. Type of Book
4. Quantity
    
Choose a method (1/2/3/4): ''', lambda x: x in ['1', '2', '3', '4'])
    
            os.system('cls')
    
            num_books = len(books)
            num_pages = math.ceil(num_books / 5)
            current_page = 1
            
            if sort_by == '1':
                method = 'ISBN'
            elif sort_by == '2':
                method = 'Title'
            elif sort_by == '3':
                method = 'Type'
            elif sort_by == '4':
                method = 'Quantity'
    
            while True:
                start_index = (current_page - 1) * 5
                end_index = min(start_index + 5, num_books)
                page_books = books[start_index:end_index]

                print(f'''Shown below is a table filled with books available in the library, sorted by {method}:\n''')
    
                system.view_books(int(sort_by), page_books)
    
                print(f"\nPage {current_page}/{num_pages}\n\n")
                time.sleep(1)
                move_decision = get_user_input("Would you like to view other pages (y/n)? ", lambda x: x.lower() in ['y', 'n'])
                print('\n')
                if move_decision == 'y':
                    while True:
                        move = get_user_input("Next/Previous/Search page (n/p/s)? ", lambda x: x.lower() in ['n', 'p', 's'])
                        if (move == 'n' and current_page == num_pages) or (move == 'p' and current_page == 1):
                            print("\n\nInvalid input! Try again...")
                            continue
                        else:
                            if move == 'n':
                                current_page += 1
                            elif move == 'p':
                                current_page -= 1
                            else:
                                print('\n')
                                current_page = int(get_user_input("Key in the page number: ", lambda x: x.isnumeric() and 1 <= int(x) <= num_pages))
                            break
                    os.system('cls')
                else:
                    print('\n')
                    return
        else:
            print("No books in the library.\n")
            return


#Add book(s)
def perform_add_book(system):
    while True:
        ISBN = get_user_input("Key in the ISBN of the new book: ", lambda x: (isbnlib.is_isbn10(x) == True or isbnlib.is_isbn13(x) == True))

        if ISBN in [book.ISBN for book in system.books]:
            print('''\nThis ISBN already exists in the system.
Action terminated.\n''')
            time.sleep(1)
            return

        os.system('cls')
        Title = input("Key in the book title: ").strip()
        os.system('cls')

        Type = get_user_input('''Here are the possible book types:
1. Paper Back
2. eBook
3. Hard Cover

Choose a book type (1/2/3): ''', lambda x: x in ['1', '2', '3'])
        Type = ["Paper Back", "eBook", "Hard Cover"][int(Type) - 1]
        os.system('cls')

        Quantity = int(get_user_input("Key in the number of books with this ISBN: ", lambda x: x.isnumeric() and int(x) >= 0))
        os.system('cls')

        new_book = Book(ISBN, Title, Type, Quantity)
        system.add_book(new_book)

        time.sleep(1)
        print(f'''Book has been added successfully!
Here are the details of the book added...
ISBN: {ISBN}
Title: {Title}
Type: {Type}
Quantity: {Quantity}\n''')
        back = get_user_input("Would you like to add another book to the system (y/n)? ", lambda x: x.lower() in ['y', 'n'])
        if back == 'y' or back == 'Y':
            os.system('cls')
        elif back == 'n' or back == 'N':
            break


#Update book(s)
def perform_update_book(system):
    while True:
        chosen_ISBN = get_user_input("Key in the ISBN of the book to be modified: ", lambda x: (isbnlib.is_isbn10(x) == True or isbnlib.is_isbn13(x) == True))

        found = False
        for book in system.books:
            if book.ISBN == chosen_ISBN:
                found = True
                os.system('cls')
                
                #Gather update details
                change_ISBN = get_user_input("Would you like to modify the book's ISBN (y/n)? ", lambda x: x.lower() in ['y', 'n'])
                os.system('cls')
                change_ISBN = get_user_input("Key in the new ISBN: ", lambda x: (isbnlib.is_isbn10(x) or isbnlib.is_isbn13(x))) if change_ISBN == 'y' else None
                os.system('cls')
                change_Title = get_user_input("Would you like to modify the book's Title (y/n)? ", lambda x: x.lower() in ['y', 'n'])
                os.system('cls')
                change_Title = input("Key in the new Title: ").strip() if change_Title == 'y' else None
                os.system('cls')
                change_Type =  get_user_input("Would you like to modify the book's Type (y/n)? ", lambda x: x.lower() in ['y', 'n'])
                os.system('cls')
                change_Type = get_user_input('''Here are the possible book types:
1. Paper Back
2. eBook
3. Hard Cover

Choose a book type (1/2/3): ''', lambda x: x in ['1', '2', '3']) if change_Type  == 'y' else None
                change_Type = ["Paper Back", "eBook", "Hard Cover"][int(change_Type) - 1] if change_Type else None
                os.system('cls')
                change_Quantity = get_user_input("Would you like to modify the book's Quantity (y/n)? ", lambda x: x.lower() in ['y', 'n']) == 'y'
                os.system('cls')
                change_Quantity = int(get_user_input("Key in the new Quantity: ", lambda x: x.isnumeric() and int(x) >= 0)) if change_Title else None
                
                #Run update action
                system.update_book_details(chosen_ISBN, change_ISBN, change_Title, change_Type, change_Quantity)
                break

        time.sleep(1)
        if found:
            os.system('cls')
            print("System has updated the book successfully!\n")
        else:
            print("The system does not contain this ISBN!\n")

        back = get_user_input("Would you like to key in the ISBN of another book (y/n)? ", lambda x: x.lower() in ['y', 'n'])
        if back == 'n' or back == 'N':
            break
        else:
            os.system('cls')


#Remove book(s)
def perform_remove_book(system):
    while True:
        chosen_ISBN = get_user_input("Key in the ISBN of the book that you wish to remove: ", lambda x: (isbnlib.is_isbn10(x) == True or isbnlib.is_isbn13(x) == True))
        os.system('cls')

        found = False
        for book in system.books:
            if book.ISBN == chosen_ISBN:
                system.remove_book(chosen_ISBN)
                found = True
                break

        time.sleep(1)
        if found:
            print("System has removed the book successfully!\n")
        else:
            print("The system does not contain this ISBN!\n")

        back = get_user_input("Would you like to key in another ISBN (y/n)? ", lambda x: x.lower() in ['y', 'n'])
        if back == 'n' or back == 'N':
            break
        else:
            os.system('cls')


#Added books are based on Requirements
#Open User Interface
def main():
    system = Library_Management_System()
    
    book1 = Book("978-0134846019", "Data Analytics with Spark Using Python", "Paper Back", 6)
    book2 = Book("978-0133316032", "Children's reading", "eBook", 3)
    book3 = Book("978-1292100142", "Global Marketing, 7th Edition", "eBook", 8)
    book4 = Book("978-1587147029", "CCNA Cyber Ops SECFND #210-250 Official Cert Guide", "Hard Cover", 5)
    book5 = Book("0306406152", "Learn Data Analytics in 100 days", "Paper Back", 10)
    system.add_book(book1)
    system.add_book(book2)
    system.add_book(book3)
    system.add_book(book4)
    system.add_book(book5)
    

    os.system('cls')

    while True:
        print("Welcome to the Library Management System!\n")
        perform_action(system)


if __name__ == '__main__':
    main()
