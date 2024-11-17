import unittest
from unittest.mock import patch, mock_open
import os
import builtins

# Importing the functions to test
from notes_app import create_note, open_note, delete_note

class TestNotesApp(unittest.TestCase):

    @patch("builtins.input", side_effect=["note1.txt", "This is the content of the note."])
    @patch("builtins.open", new_callable=mock_open)
    def test_create_note_success(self, mock_file, mock_input):
        create_note()
        mock_file.assert_called_once_with("note1.txt", "w")
        mock_file().write.assert_called_once_with("This is the content of the note.")
    
    @patch("os.path.exists", return_value=True)
    @patch("builtins.input", side_effect=["note1.txt"])
    def test_create_note_file_exists(self, mock_input, mock_exists):
        with patch("builtins.print") as mock_print:
            create_note()
            mock_print.assert_called_with("A note with this name already exists.")
    
    @patch("builtins.input", side_effect=["note1.txt"])
    @patch("builtins.open", new_callable=mock_open, read_data="This is the content of the note.")
    @patch("os.path.exists", return_value=True)
    def test_open_note_success(self, mock_exists, mock_file, mock_input):
        with patch("builtins.print") as mock_print:
            open_note()
            mock_file.assert_called_once_with("note1.txt", "r")
            mock_print.assert_any_call("\n--- Content of note1.txt ---")
            mock_print.assert_any_call("This is the content of the note.")
    
    @patch("builtins.input", side_effect=["note1.txt"])
    @patch("os.path.exists", return_value=False)
    def test_open_note_file_not_found(self, mock_exists, mock_input):
        with patch("builtins.print") as mock_print:
            open_note()
            mock_print.assert_called_with("No note with this name found.")
    
    @patch("builtins.input", side_effect=["note1.txt"])
    @patch("os.path.exists", return_value=True)
    @patch("os.remove")
    def test_delete_note_success(self, mock_remove, mock_exists, mock_input):
        with patch("builtins.print") as mock_print:
            delete_note()
            mock_remove.assert_called_once_with("note1.txt")
            mock_print.assert_called_with("Note 'note1.txt' deleted successfully.")
    
    @patch("builtins.input", side_effect=["note1.txt"])
    @patch("os.path.exists", return_value=False)
    def test_delete_note_file_not_found(self, mock_exists, mock_input):
        with patch("builtins.print") as mock_print:
            delete_note()
            mock_print.assert_called_with("No note with this name found.")
    
    @patch("builtins.input", side_effect=["note2.txt", "Some content."])
    @patch("os.path.exists", return_value=False)
    @patch("builtins.open", new_callable=mock_open)
    def test_create_note_different_filename(self, mock_file, mock_exists, mock_input):
        create_note()
        mock_file.assert_called_once_with("note2.txt", "w")
        mock_file().write.assert_called_once_with("Some content.")
    
    @patch("builtins.input", side_effect=["note1.txt"])
    @patch("builtins.open", new_callable=mock_open, read_data="Another note content.")
    @patch("os.path.exists", return_value=True)
    def test_open_note_different_content(self, mock_exists, mock_file, mock_input):
        with patch("builtins.print") as mock_print:
            open_note()
            mock_file.assert_called_once_with("note1.txt", "r")
            mock_print.assert_any_call("\n--- Content of note1.txt ---")
            mock_print.assert_any_call("Another note content.")
    
    @patch("os.path.exists", side_effect=[False, True, True])
    @patch("os.remove")
    @patch("builtins.input", side_effect=["note1.txt", "note1.txt", "note1.txt"])
    def test_multiple_delete_scenarios(self, mock_input, mock_remove, mock_exists):
        with patch("builtins.print") as mock_print:
            delete_note()  # File doesn't exist
            mock_print.assert_called_with("No note with this name found.")
            
            delete_note()  # File exists
            mock_remove.assert_called_with("note1.txt")
            mock_print.assert_called_with("Note 'note1.txt' deleted successfully.")
    
    @patch("builtins.input", side_effect=["invalid|file<>name.txt", "Some note content."])
    @patch("builtins.print")
    def test_invalid_filename(self, mock_print, mock_input):
        create_note()
        mock_print.assert_called_with("Invalid filename. Please avoid special characters and try again.")

if __name__ == "__main__":
    unittest.main()
