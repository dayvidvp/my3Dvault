import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget,
                            QAction, QFileDialog, QListWidget)

from PyQt5.QtWidgets import QHBoxLayout  # Import QHBoxLayout

from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set main window's properties
        self.setWindowTitle("My 3D Mini Vault")
        #determine the current screen size
        screen = app.primaryScreen()
        size = screen.size()
        self.setGeometry(0, 0, size.width(), size.height() - 50)

        # Create and set the central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        # Create a vertical layout
        layout = QVBoxLayout()

        # Add a label widget
        self.label = QLabel("Select a directory to display 3D print files")
        layout.addWidget(self.label)

        # Add a list widget for displaying file names
        self.file_list_widget = QListWidget()
        layout.addWidget(self.file_list_widget)

        # Modify layout to include a horizontal layout
        main_layout = QHBoxLayout()  # Main layout that will include your original layout and the preview
        main_layout.addLayout(layout)  # Add your original vertical layout

        # Create a preview widget (this could be QLabel or any other QWidget)
        self.preview_widget = QLabel("3D Model Preview")
        self.preview_widget.setFixedSize(400, 600)  # Set fixed size for the preview widget

        # Add the preview widget to the main layout
        main_layout.addWidget(self.preview_widget)

        # Set the main layout on the central widget
        central_widget.setLayout(main_layout)

        # Create a menu bar
        self.create_menu_bar()

    def create_menu_bar(self):
        # Create a menu bar with two actions: open and exit
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')

        # Add 'Open Directory' action
        open_action = QAction('&Open Directory', self)
        open_action.triggered.connect(self.open_directory)
        file_menu.addAction(open_action)

        # Add 'Exit' action
        exit_action = QAction('&Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def open_directory(self):
        # Open a dialog to select a directory
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.label.setText(f"Selected Directory: {directory}")
            self.list_files_in_directory(directory)

    def list_files_in_directory(self, directory):
        # This function will be updated to scan for 3D print files in all subdirectories
        # list only stl files
        self.file_list_widget.clear()
        import os
        # get all stl files in the main and sub directories in a dictionary
        all_files = {}

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".stl"):
                    all_files[file] = os.path.join(root, file)
        print(all_files)
        # add all stl files to the list widget
        for file in all_files:
            self.file_list_widget.addItem(file)

        # add a label to show the number of files
        self.label.setText(f"Selected Directory: {directory} - {len(all_files)} files")


    # create a preview window that preview a 3D model
    def preview_3d_model(self, file):

        # Create a new plot
        figure = pyplot.figure()
        axes = figure.add_subplot(projection='3d')

        # Load the STL files and add the vectors to the plot
        your_mesh = mesh.Mesh.from_file(file)
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))

        # Auto scale to the mesh size
        scale = your_mesh.points.flatten()
        axes.auto_scale_xyz(scale, scale, scale)

        # Show the plot to the screen
        pyplot.show()

# Create an instance of QApplication
app = QApplication(sys.argv)

# Create an instance of the application's GUI
window = MainWindow()
window.show()

# Start the application's event loop
sys.exit(app.exec_())
