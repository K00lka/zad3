import os
import re

def display_menu():
    print("\n--- Notes App ---")
    print("1. Create a new note")
    print("2. Open an existing note")
    print("3. Delete a note")
    print("4. Exit")

def create_note():
    filename = input("Enter the filename for the note (e.g., note1.txt): ")
    # Validate filename: no special characters like \ / : * ? " < > | and not empty
    if not re.match(r'^[\w\-. ]+$', filename):
        print("Invalid filename. Please avoid special characters and try again.")
        return
    if os.path.exists(filename):
        print("A note with this name already exists.")
        return
    content = input("Write your note content below:\n")
    with open(filename, 'w') as file:
        file.write(content)
    print(f"Note '{filename}' created successfully.")

def open_note():
    filename = input("Enter the filename of the note to open (e.g., note1.txt): ")
    if not os.path.exists(filename):
        print("No note with this name found.")
        return
    with open(filename, 'r') as file:
        content = file.read()
    print(f"\n--- Content of {filename} ---")
    print(content)

def delete_note():
    filename = input("Enter the filename of the note to delete (e.g., note1.txt): ")
    if not os.path.exists(filename):
        print("No note with this name found.")
        return
    os.remove(filename)
    print(f"Note '{filename}' deleted successfully.")

def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ")
        if choice == '1':
            create_note()
        elif choice == '2':
            open_note()
        elif choice == '3':
            delete_note()
        elif choice == '4':
            print("Exiting Notes App. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()