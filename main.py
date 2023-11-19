import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QFontDialog, QVBoxLayout, QWidget, QMenuBar, QMessageBox, QPlainTextEdit
from PyQt5.QtCore import QDateTime, QUrl
from PyQt5.QtGui import QIcon, QFont, QDesktopServices


class PlainTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super(PlainTextEdit, self).__init__(parent)

        # Set the border color to gray
        self.setStyleSheet("QPlainTextEdit { border: 1px solid lightgray; }")

        # Set default font size to 12
        default_font = QFont()
        default_font.setPointSize(12)
        self.setFont(default_font)

    def insertFromMimeData(self, mime_data):
        # Override insertFromMimeData to prevent the automatic formatting of pasted text
        cursor = self.textCursor()
        cursor.insertText(mime_data.text())
        self.setTextCursor(cursor)


class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize UI
        self.init_ui()

    def init_ui(self):
        # Create a QTextEdit widget
        self.text_edit = PlainTextEdit(self)
        self.setCentralWidget(self.text_edit)
        
        # Create Find dialog
        self.setWindowIcon(QIcon('icon.ico'))
        # Create a menu bar
        menubar = self.menuBar()

        # Create File menu
        file_menu = menubar.addMenu('File')

        new_action = QAction('New', self)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        new_window_action = QAction('New Window', self)
        new_window_action.triggered.connect(self.new_window)
        file_menu.addAction(new_window_action)

        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction('Save As...', self)
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        page_setup_action = QAction('Page Setup', self)
        page_setup_action.triggered.connect(self.page_setup)
        file_menu.addAction(page_setup_action)

        print_action = QAction('Print', self)
        print_action.triggered.connect(self.print_file)
        file_menu.addAction(print_action)

        file_menu.addSeparator()

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Create Edit menu
        edit_menu = menubar.addMenu('Edit')

        undo_action = QAction('Undo', self)
        undo_action.triggered.connect(self.text_edit.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction('Redo', self)
        redo_action.triggered.connect(self.text_edit.redo)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction('Cut', self)
        cut_action.triggered.connect(self.text_edit.cut)
        edit_menu.addAction(cut_action)

        copy_action = QAction('Copy', self)
        copy_action.triggered.connect(self.text_edit.copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction('Paste', self)
        paste_action.triggered.connect(self.text_edit.paste)
        edit_menu.addAction(paste_action)

        delete_action = QAction('Delete', self)
        delete_action.triggered.connect(self.text_edit.cut)  # Delete is equivalent to Cut
        edit_menu.addAction(delete_action)

        edit_menu.addSeparator()

        find_action = QAction('Find', self)
        find_action.triggered.connect(self.find_dialog)
        edit_menu.addAction(find_action)

        replace_action = QAction('Replace', self)
        replace_action.triggered.connect(self.replace)
        edit_menu.addAction(replace_action)

        edit_menu.addSeparator()

        goto_action = QAction('Go To', self)
        goto_action.triggered.connect(self.goto_dialog)
        edit_menu.addAction(goto_action)

        edit_menu.addSeparator()

        select_all_action = QAction('Select All', self)
        select_all_action.triggered.connect(self.text_edit.selectAll)
        edit_menu.addAction(select_all_action)

        time_date_action = QAction('Time/Date', self)
        time_date_action.triggered.connect(self.insert_time_date)
        edit_menu.addAction(time_date_action)

        # Create Font menu
        format_menu = menubar.addMenu('Format')

        font_action = QAction('Font...', self)
        font_action.triggered.connect(self.change_font)
        format_menu.addAction(font_action)

        # Create View menu
        view_menu = menubar.addMenu('View')

        # Create Help menu
        help_menu = menubar.addMenu('Help')

        view_help = QAction('View Help', self)
        view_help.triggered.connect(self.view_help)
        help_menu.addAction(view_help)

        send_feedback = QAction('Send Feedback', self)
        send_feedback.triggered.connect(self.send_feedback)
        help_menu.addAction(send_feedback)

        help_menu.addSeparator()

        about_notepad = QAction('About Notepad', self)
        about_notepad.triggered.connect(self.about_notepad)
        help_menu.addAction(about_notepad)

        # Set window properties
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Notepad')

    def view_help(self):
        feedback_url = 'https://github.com/abdullahCoder-Tech/Notepad'
        QDesktopServices.openUrl(QUrl(feedback_url))

    def send_feedback(self):
        # Open the feedback URL in the default web browser
        feedback_url = 'https://github.com/abdullahCoder-Tech/Notepad'
        QDesktopServices.openUrl(QUrl(feedback_url))

    def about_notepad(self):
        about_message = (
            "Notepad Application\n"
            "Author: Abdullah O. Mustapha\n"
            "Version: v1.0\n"
            "License: GNU General Public License\n"
            "\n\nAll Rights Reserved"
        )
        QMessageBox.information(self, 'About Notepad', about_message, QMessageBox.Ok)

    def new_file(self):
        self.text_edit.clear()

    def new_window(self):
        new_notepad = Notepad()
        new_notepad.show()

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.txt);;All Files (.)', options=options)
        if file_name:
            with open(file_name, 'r') as file:
                content = file.read()
                self.text_edit.setPlainText(content)

    def save_file(self):
        if not hasattr(self, 'current_file') or not self.current_file:
            self.save_file_as()
        else:
            with open(self.current_file, 'w') as file:
                file.write(self.text_edit.toPlainText())

    def save_file_as(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'Text Files (*.txt);;All Files (.)', options=options)
        if file_name:
            self.current_file = file_name
            self.save_file()

    def page_setup(self):
        QMessageBox.information(self, 'Info', 'Coming Soon', QMessageBox.Ok)

    def print_file(self):
        QMessageBox.information(self, 'Info', 'Coming Soon', QMessageBox.Ok)

    def change_font(self):
        font, ok = QFontDialog.getFont(self.text_edit.font(), self)
        if ok:
            self.text_edit.setFont(font)

    def goto_dialog(self):
        QMessageBox.information(self, 'Info', 'Coming Soon', QMessageBox.Ok)

    def replace(self):
        QMessageBox.information(self, 'Info', 'Coming Soon', QMessageBox.Ok)

    def find_dialog(self):
        QMessageBox.information(self, 'Info', 'Coming Soon', QMessageBox.Ok)


    def insert_time_date(self):
        current_date_time = QDateTime.currentDateTime().toString('MM/dd/yyyy hh:mm:ss AP')
        self.text_edit.textCursor().insertText(current_date_time)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    notepad = Notepad()
    notepad.show()
    sys.exit(app.exec_())