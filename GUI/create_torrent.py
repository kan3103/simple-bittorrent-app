import os
from PyQt6 import QtWidgets
import sys
import requests
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
from api import Client

class CreateTorrentDialog(QtWidgets.QDialog):
    def __init__(self, client, parent=None):
        self.client = client
        super().__init__(parent)
        self.setWindowTitle("Create Torrent")
        self.setGeometry(100, 100, 600, 400)  

        layout = QtWidgets.QVBoxLayout(self)

        label = QtWidgets.QLabel("Choose files to create a torrent:")
        layout.addWidget(label)

        self.file_list = QtWidgets.QListWidget(self)
        layout.addWidget(self.file_list)

        button_layout = QtWidgets.QHBoxLayout()
        
        select_button = QtWidgets.QPushButton("Add Files", self)
        select_button.clicked.connect(self.add_files)
        button_layout.addWidget(select_button)

        remove_button = QtWidgets.QPushButton("Remove Selected File", self)
        remove_button.clicked.connect(self.remove_selected_file)
        button_layout.addWidget(remove_button)

        layout.addLayout(button_layout)

        torrent_name_label = QtWidgets.QLabel("Torrent Name:")
        layout.addWidget(torrent_name_label)

        self.torrent_name_input = QtWidgets.QLineEdit(self)
        self.torrent_name_input.setPlaceholderText("Enter torrent name here...")
        layout.addWidget(self.torrent_name_input)

        self.create_button = QtWidgets.QPushButton("Create Torrent", self)
        self.create_button.clicked.connect(self.create_torrent)
        layout.addWidget(self.create_button)

        cancel_button = QtWidgets.QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.reject)
        layout.addWidget(cancel_button)
        self.torrent = None
        self.selected_files = []

    def add_files(self):
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Select Files", "", "All Files (*.*)")
        if files:
            for file in files:
                if file not in self.selected_files:
                    self.selected_files.append(file)
                    self.file_list.addItem(file)

    def remove_selected_file(self):
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please select a file to remove.")
            return
        
        for item in selected_items:
            self.selected_files.remove(item.text())
            self.file_list.takeItem(self.file_list.row(item))

    def create_torrent(self):
        torrent_name = self.torrent_name_input.text().strip()
        if not torrent_name:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please enter a torrent name.")
            return
        if not self.selected_files:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please select at least one file.")
            return
        dir = self.client.make_dir(torrent_name, self.selected_files)
        self.torrent = self.client.create_torrent(dir)
        QtWidgets.QMessageBox.information(self, "Success", "Torrent file created successfully!")
        self.accept()

