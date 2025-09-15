# import mysql.connector
# from mysql.connector import Error

# def connect_db():
#     return mysql.connector.connect(
#         host='localhost',
#         user='root',
#         password='root',
#         database='diary_app'
#     )

# def add_entry():
#     keyword = input("Enter keyword (title): ").strip()
#     content = input("Write your diary entry:\n").strip()
    
#     try:
#         conn = connect_db()
#         cursor = conn.cursor()
#         query = "INSERT INTO entries (keyword, content) VALUES (%s, %s)"
#         cursor.execute(query, (keyword, content))
#         conn.commit()
#         print("Entry added successfully!")
#     except Error as e:
#         print(f"Error: {e}")
#     finally:
#         cursor.close()
#         conn.close()

# def search_entries():
#     keyword = input("Enter keyword to search: ").strip()
    
#     try:
#         conn = connect_db()
#         cursor = conn.cursor()
#         query = """
#             SELECT id, date, keyword, content FROM entries 
#             WHERE keyword LIKE %s OR content LIKE %s
#             ORDER BY date DESC
#         """
#         search_pattern = f"%{keyword}%"
#         cursor.execute(query, (search_pattern, search_pattern))
#         results = cursor.fetchall()

#         if results:
#             for row in results:
#                 print(f"\nID: {row[0]}\nDate: {row[1]}\nKeyword: {row[2]}\nContent: {row[3]}\n{'-'*40}")
#         else:
#             print("No entries found matching the keyword.")
#     except Error as e:
#         print(f"Error: {e}")
#     finally:
#         cursor.close()
#         conn.close()

# def view_all_entries():
#     try:
#         conn = connect_db()
#         cursor = conn.cursor()
#         query = "SELECT id, date, keyword, content FROM entries ORDER BY date DESC"
#         cursor.execute(query)
#         results = cursor.fetchall()

#         if results:
#             for row in results:
#                 print(f"\nID: {row[0]}\nDate: {row[1]}\nKeyword: {row[2]}\nContent: {row[3]}\n{'-'*40}")
#         else:
#             print("No diary entries yet.")
#     except Error as e:
#         print(f"Error: {e}")
#     finally:
#         cursor.close()
#         conn.close()

# def delete_entry():
#     entry_id = input("Enter entry ID to delete: ").strip()
    
#     try:
#         conn = connect_db()
#         cursor = conn.cursor()
#         query = "DELETE FROM entries WHERE id = %s"
#         cursor.execute(query, (entry_id,))
#         conn.commit()
#         if cursor.rowcount:
#             print("Entry deleted successfully!")
#         else:
#             print("No entry found with that ID.")
#     except Error as e:
#         print(f"Error: {e}")
#     finally:
#         cursor.close()
#         conn.close()

# def main():
#     print("=== Personal Diary CLI ===")
#     while True:
#         print("\nOptions:")
#         print("1. Add new entry")
#         print("2. Search entries by keyword or content")
#         print("3. View all entries")
#         print("4. Delete entry by ID")
#         print("5. Exit")

#         choice = input("Choose an option (1-5): ").strip()

#         if choice == '1':
#             add_entry()
#         elif choice == '2':
#             search_entries()
#         elif choice == '3':
#             view_all_entries()
#         elif choice == '4':
#             delete_entry()
#         elif choice == '5':
#             print("Goodbye!")
#             break
#         else:
#             print("Invalid choice. Try again.")
#         input('')
#         print("\033c", end="")

# if __name__ == "__main__":
#     main()

import mysql.connector
from mysql.connector import Error
from datetime import datetime

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='diary_app'
    )

def add_entry():
    keyword = input("Enter keyword (title): ").strip()
    content = input("Write your diary entry:\n").strip()
    
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "INSERT INTO entries (keyword, content) VALUES (%s, %s)"
        cursor.execute(query, (keyword, content))
        conn.commit()
        print("Entry added successfully!")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

def search_entries():
    print("\nSearch by:")
    print("1. Keyword")
    print("2. Content")
    print("3. Date (YYYY-MM-DD)")
    choice = input("Choose search type (1-3): ").strip()
    
    try:
        conn = connect_db()
        cursor = conn.cursor()

        if choice == '1':
            keyword = input("Enter keyword to search: ").strip()
            query = """
                SELECT id, date, keyword FROM entries 
                WHERE keyword LIKE %s ORDER BY date DESC
            """
            cursor.execute(query, (f"%{keyword}%",))
        
        elif choice == '2':
            content = input("Enter content keyword to search: ").strip()
            query = """
                SELECT id, date, keyword FROM entries 
                WHERE content LIKE %s ORDER BY date DESC
            """
            cursor.execute(query, (f"%{content}%",))

        elif choice == '3':
            date_str = input("Enter date (YYYY-MM-DD): ").strip()
            query = """
                SELECT id, date, keyword FROM entries 
                WHERE DATE(date) = %s ORDER BY date DESC
            """
            cursor.execute(query, (date_str,))
        else:
            print("Invalid choice.")
            return

        results = cursor.fetchall()

        if not results:
            print("No entries found.")
            return

        print("\nMatched Entries:")
        for row in results:
            print(f"ID: {row[0]} | Date: {row[1]} | Keyword: {row[2]}")

        entry_id = input("\nEnter entry ID for more options (or press Enter to cancel): ").strip()
        if entry_id:
            entry_submenu(entry_id)

    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

def entry_submenu(entry_id):
    while True:
        print("\nOptions for Entry ID", entry_id)
        print("1. View full details")
        print("2. Edit entry")
        print("3. Delete entry")
        print("4. Go back")

        choice = input("Choose an option (1-4): ").strip()

        if choice == '1':
            view_entry(entry_id)
        elif choice == '2':
            update_entry(entry_id)
        elif choice == '3':
            delete_entry(entry_id)
            break
        elif choice == '4':
            break
        else:
            print("Invalid choice.")
        input('')
        print("\033c", end="")

def view_entry(entry_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "SELECT id, date, keyword, content FROM entries WHERE id = %s"
        cursor.execute(query, (entry_id,))
        row = cursor.fetchone()

        if row:
            print(f"\nID: {row[0]}\nDate: {row[1]}\nKeyword: {row[2]}\nContent: {row[3]}")
        else:
            print("Entry not found.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

def update_entry(entry_id):
    new_keyword = input("Enter new keyword (leave blank to keep unchanged): ").strip()
    new_content = input("Enter new content (leave blank to keep unchanged): ").strip()

    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Fetch current data
        cursor.execute("SELECT keyword, content FROM entries WHERE id = %s", (entry_id,))
        row = cursor.fetchone()
        if not row:
            print("Entry not found.")
            return

        updated_keyword = new_keyword if new_keyword else row[0]
        updated_content = new_content if new_content else row[1]

        query = "UPDATE entries SET keyword = %s, content = %s WHERE id = %s"
        cursor.execute(query, (updated_keyword, updated_content, entry_id))
        conn.commit()
        print("Entry updated successfully!")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

def delete_entry(entry_id=None):
    if not entry_id:
        entry_id = input("Enter entry ID to delete: ").strip()

    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "DELETE FROM entries WHERE id = %s"
        cursor.execute(query, (entry_id,))
        conn.commit()
        if cursor.rowcount:
            print("Entry deleted successfully!")
        else:
            print("No entry found with that ID.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

def view_all_entries():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "SELECT id, date, keyword FROM entries ORDER BY date DESC"
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            for row in results:
                print(f"ID: {row[0]} | Date: {row[1]} | Keyword: {row[2]}")
        else:
            print("No diary entries yet.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

def main():
    print("=== Personal Diary CLI ===")
    while True:
        print("\nMain Menu:")
        print("1. Add new entry")
        print("2. Search entries")
        print("3. View all entries")
        print("4. Delete entry by ID")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == '1':
            add_entry()
        elif choice == '2':
            search_entries()
        elif choice == '3':
            view_all_entries()
        elif choice == '4':
            delete_entry()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
