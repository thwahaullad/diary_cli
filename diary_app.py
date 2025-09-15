import mysql.connector
from mysql.connector import Error

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
    keyword = input("Enter keyword to search: ").strip()
    
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = """
            SELECT id, date, keyword, content FROM entries 
            WHERE keyword LIKE %s OR content LIKE %s
            ORDER BY date DESC
        """
        search_pattern = f"%{keyword}%"
        cursor.execute(query, (search_pattern, search_pattern))
        results = cursor.fetchall()

        if results:
            for row in results:
                print(f"\nID: {row[0]}\nDate: {row[1]}\nKeyword: {row[2]}\nContent: {row[3]}\n{'-'*40}")
        else:
            print("No entries found matching the keyword.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

def view_all_entries():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "SELECT id, date, keyword, content FROM entries ORDER BY date DESC"
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            for row in results:
                print(f"\nID: {row[0]}\nDate: {row[1]}\nKeyword: {row[2]}\nContent: {row[3]}\n{'-'*40}")
        else:
            print("No diary entries yet.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

def delete_entry():
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

def main():
    print("=== Personal Diary CLI ===")
    while True:
        print("\nOptions:")
        print("1. Add new entry")
        print("2. Search entries by keyword or content")
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
        input('')
        print("\033c", end="")

if __name__ == "__main__":
    main()
