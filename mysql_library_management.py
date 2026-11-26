import mysql.connector

class Library_Management:
    def __init__(self):
        try:
            self.con=mysql.connector.connect(user="root",password="ajin",host="localhost",database="library_management")
            self.cursor=self.con.cursor()
            print("Connection Established Successfully")
            print()
        except:
            print("FAILED TO CONNECT!!!")
            print()

    def add_book(self,title,author,category,total_copies,available_copies):
        try:
            if total_copies<0 or available_copies<0:
                print("error: Copies cannot be negative")
                print()
                return

            if available_copies > total_copies:
                print("Available copies cannot exceed total_copies")
                print()
                return

            query='''insert into books(title,author,category,total_copies,available_copies) values(%s,%s,%s,%s,%s);'''
            data=(title,author,category,total_copies,available_copies)
            self.cursor.execute(query,data)
            self.con.commit()
            print("Book inserted successfully")
            print()
        except:
            print("Book insertion failed!!!")
            print()


    def view_available_books(self):
        try:
            query='''select * from books where available_copies > 0 order by title asc limit 20;'''
            self.cursor.execute(query)
            records=self.cursor.fetchall()
            if records:
                for row in records:
                    print(row)
                print()
            else:
                print("No records found")
        except:
            print("FAILED TO READ!!")
            print()

    def search_book(self,id=None,keyword=None):
        try:
            if id:
                query='''select * from books where book_id = %s'''
                data=(id,)
            elif keyword:
                query='''select * from books where title like %s or author like %s;'''
                data=(f"%{keyword}%",f"%{keyword}%")
            else:
                print("Please provide a book_id or keyword")
                print()
                return

            self.cursor.execute(query,data)
            records=self.cursor.fetchall()
            if records:
                for row in records:
                    print(row)
                print()
            else:
                print("No records Found")
                print()
        except:
            print("Unable to read data!!")

    def update_book_availabilty(self,id,new_available):
        try:
            self.cursor.execute("select total_copies from books where book_id=%s;",(id,))
            record=self.cursor.fetchone()

            total_copies=record[0]

            if new_available<0:
                print("Copies cannot be negative!!")
                print()
                return
            if new_available>total_copies:
                print("Available copies cannot exceed total copies")
                print()
                return

            #update
            query='''update books set available_copies = %s where book_id = %s'''
            data=(new_available,id)
            self.cursor.execute(query,data)
            self.con.commit()

            if self.cursor.rowcount>0:
                print("Available copies updated successfully")
                print()
            else:
                print("No records updated")
        except:
            print("Updation Failed")

    def delete_book(self,id):
        try:
            confirm=input("Are you sure to delete the book(y/n): ")
            if confirm=="y":
                query = '''delete from books where book_id = %s'''
                data=(id,)
                self.cursor.execute(query,data)
                self.con.commit()
                if self.cursor.rowcount>0:
                    print("Book Deleted")
                    print()
                else:
                    print("Deletion failed")
            else:
                print("Deletion cancelled")
                print()
        except:
            print("Unable to delete: ")


    def library_summary(self):
        try:
            query='''select count(*),sum(available_copies),avg(total_copies) from books;'''
            self.cursor.execute(query)
            records=self.cursor.fetchall()
            if records:
                for row in records:
                    print(row)
                print()
            else:
                print("No records found")
        except:
            print("Unable to read")


obj = Library_Management()

while True:
    print("1. Add Book")
    print("2. View Available Books")
    print("3. Search Book")
    print("4. Update Book Availability")
    print("5. Delete Book")
    print("6. Library Summary")
    print("7. Exit")

    ch = int(input("Enter your choice: "))
    print()

    if ch == 1:
        title = input("Enter book title: ")
        author = input("Enter author name: ")
        category = input("Enter category: ")
        total_copies = int(input("Enter total copies: "))
        available_copies = int(input("Enter available copies: "))
        obj.add_book(title, author, category, total_copies, available_copies)

    elif ch == 2:
        obj.view_available_books()

    elif ch == 3:
        print("Search by:\n1. Book ID\n2. Title or Author")
        sub_ch = int(input("Enter choice (1/2): "))
        if sub_ch == 1:
            book_id = int(input("Enter Book ID: "))
            obj.search_book(id=book_id)
        elif sub_ch == 2:
            keyword = input("Enter title or author keyword: ")
            obj.search_book(keyword=keyword)
        else:
            print("Invalid search choice\n")

    elif ch == 4:
        book_id = int(input("Enter Book ID: "))
        new_available = int(input("Enter new available copies: "))
        obj.update_book_availabilty(book_id, new_available)

    elif ch == 5:
        book_id = int(input("Enter Book ID to delete: "))
        obj.delete_book(book_id)

    elif ch == 6:
        obj.library_summary()

    elif ch == 7:
        obj.cursor.close()
        obj.con.close()
        break

    else:
        print("Invalid choice. Please try again.")












