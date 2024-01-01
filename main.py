import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QFontDialog, QMessageBox, QPlainTextEdit, QStatusBar, QInputDialog
from PyQt5.QtCore import QDateTime, QUrl, QTextCodec
from PyQt5.QtGui import QIcon, QFont, QDesktopServices
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter




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
        cursor = self.textCursor()
        cursor.insertText(mime_data.text())
        self.setTextCursor(cursor)


class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize UI
        self.init_ui()

        self.new_notepad = None

    def init_ui(self):
        # Create a QTextEdit widget
        self.text_edit = PlainTextEdit(self)
        self.setCentralWidget(self.text_edit)
        
        # Increase font size for the menu bar
        menubar = self.menuBar()
        menubar_font = menubar.font()
        menubar_font.setPointSize(11)  # Adjust the font size as needed
        menubar.setFont(menubar_font)

        # Create Find dialog
        self.setWindowIcon(QIcon('icon.ico'))
        # Create a menu bar
        menubar = self.menuBar()

        # Create File menu
        file_menu = menubar.addMenu('File')

        new_action = QAction('New', self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        new_window_action = QAction('New Window', self)
        new_window_action.setShortcut("Ctrl+Shift+N")
        new_window_action.triggered.connect(self.new_window)
        file_menu.addAction(new_window_action)

        open_action = QAction('Open', self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction('Save', self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction('Save As...', self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        page_setup_action = QAction('Page Setup', self)
        page_setup_action.triggered.connect(self.page_setup)
        file_menu.addAction(page_setup_action)

        print_action = QAction('Print', self)
        print_action.setShortcut("Ctrl+P")
        print_action.triggered.connect(self.print_file)
        file_menu.addAction(print_action)

        file_menu.addSeparator()

        exit_action = QAction('Exit', self)
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Create Edit menu
        edit_menu = menubar.addMenu('Edit')

        undo_action = QAction('Undo', self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.text_edit.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction('Redo', self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.text_edit.redo)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction('Cut', self)
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(self.text_edit.cut)
        edit_menu.addAction(cut_action)

        copy_action = QAction('Copy', self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.text_edit.copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction('Paste', self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.text_edit.paste)
        edit_menu.addAction(paste_action)

        delete_action = QAction('Delete', self)
        delete_action.setShortcut("Del")
        delete_action.triggered.connect(self.text_edit.cut)  # Delete is equivalent to Cut
        edit_menu.addAction(delete_action)

        edit_menu.addSeparator()

        goto_action = QAction('Go To', self)
        goto_action.triggered.connect(self.goto_dialog)
        edit_menu.addAction(goto_action)

        edit_menu.addSeparator()

        select_all_action = QAction('Select All', self)
        select_all_action.setShortcut("Ctrl+A")
        select_all_action.triggered.connect(self.text_edit.selectAll)
        edit_menu.addAction(select_all_action)

        time_date_action = QAction('Time/Date', self)
        time_date_action.setShortcut("Ctrl+T")
        time_date_action.triggered.connect(self.insert_time_date)
        edit_menu.addAction(time_date_action)

        # Create Font menu
        format_menu = menubar.addMenu('Format')

        font_action = QAction('Font...', self)
        font_action.triggered.connect(self.change_font)
        format_menu.addAction(font_action)

        wordWrap_action = QAction('Word wrap', self)
        wordWrap_action.setCheckable(True)
        format_menu.addAction(wordWrap_action)

        # Create View menu
        view_menu = menubar.addMenu('View')

        zoom_menu = view_menu.addMenu("Zoom...")
        zoom_in = zoom_menu.addAction('Zoom in')
        zoom_in.setShortcut("Ctrl+1")  # Adjust the shortcut as needed
        zoom_in.triggered.connect(self.zoom_in)

        zoom_out = zoom_menu.addAction('Zoom out')
        zoom_out.setShortcut("Ctrl+0")  # Adjust the shortcut as needed
        zoom_out.triggered.connect(self.zoom_out)


        # Create a status bar
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        # Create a QAction for the status bar
        status_bar_action = QAction('Status bar', self)
        status_bar_action.setCheckable(True)
        status_bar_action.setChecked(True)
        status_bar_action.triggered.connect(self.toggle_status_bar)
        view_menu.addAction(status_bar_action)

        self.update_status_bar
        self.text_edit.textChanged.connect(self.update_status_bar)

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
    
    def toggle_status_bar(self, checked):
        if checked:
            self.status_bar.show()
        else:
            self.status_bar.hide()
    def update_status_bar(self):
        cursor = self.text_edit.textCursor()
        block = cursor.block()
        line_number = block.blockNumber() + 1
        column_number = cursor.positionInBlock() + 1

        # Get plain text content
        plain_text = self.text_edit.toPlainText()

        # Use QTextCodec to detect the encoding
        codec = QTextCodec.codecForName("UTF-8")
        encoding = codec.name()

        status_text = f'Ln {line_number}, Col {column_number} | Encoding: {encoding}'
        self.status_bar.showMessage(status_text)

    def zoom_in(self):
        self.text_edit.zoomIn(1)
    def zoom_out(self):
        self.text_edit.zoomOut(1)
    def view_help(self):
        feedback_url = 'https://github.com/abdullahCoder-Tech/Notepad/blob/main/README.md'
        QDesktopServices.openUrl(QUrl(feedback_url))

    def send_feedback(self):
        # Open the feedback URL in the default web browser
        feedback_url = 'https://github.com/abdullahCoder-Tech/Notepad/issues/new'
        QDesktopServices.openUrl(QUrl(feedback_url))

    def about_notepad(self):
        about_message = (
            "About this app\n\n"
            "Author: Abdullah O. Mustapha\n"
            "Version: v1.0.1\n"
            "License: MIT License\n"
            "\n\n© 2023 Drop Dev. All rights reserved"
        )
        QMessageBox.information(self, 'About Notepad', about_message, QMessageBox.Ok)

    def new_file(self):
        self.text_edit.clear()

    # def new_window(self):
    #     new_notepad = Notepad()
    #     new_notepad.show()

    def new_window(self):
        # Check if a new window is already open
        if self.new_notepad is None or not self.new_notepad.isVisible():
            # Create a new instance of Notepad
            self.new_notepad = Notepad()
            self.new_notepad.show()
        else:
            # Bring the existing window to front
            self.new_notepad.raise_()

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.txt);;All Files (*)', options=options)
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
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'Text Files (*.txt);;C++ Files (*.cpp);;C Files(*.c);;Python Files (*.py);;All Files (*)', options=options)
        if file_name:
            self.current_file = file_name
            self.save_file()

    def page_setup(self):
        pass


    def print_file(self):
            printer = QPrinter(QPrinter.HighResolution)
            dialog = QPrintDialog(printer, self)
            if dialog.exec_() == QPrintDialog.Accepted:
                self.text_edit.print_(printer)

    def change_font(self):
        font, ok = QFontDialog.getFont(self.text_edit.font(), self)
        if ok:
            self.text_edit.setFont(font)
    def goto_dialog(self):
        # Get the total number of lines in the text editor
        total_lines = self.text_edit.document().blockCount()

        # Display an input dialog for the user to enter the line number
        line_number, ok = QInputDialog.getInt(self, 'Go To Line', 'Enter Line Number (1 - {}):'.format(total_lines), min=1, max=total_lines)

        if ok:
            # Move the cursor to the specified line
            cursor = self.text_edit.textCursor()
            cursor.movePosition(cursor.Start)
            for _ in range(line_number - 1):
                cursor.movePosition(cursor.NextBlock)

            self.text_edit.setTextCursor(cursor)

    def insert_time_date(self):
        current_date_time = QDateTime.currentDateTime().toString('MM/dd/yyyy hh:mm:ss AP')
        self.text_edit.textCursor().insertText(current_date_time)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    notepad = Notepad()
    notepad.show()
    sys.exit(app.exec_())