import os
import datetime
from datetime import timedelta
import exiftool
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QDialog, QCalendarWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QProgressBar
from PyQt5.QtGui import QFont, QPalette, QColor
# from qt_material import apply_stylesheet

class CalendarDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Date")
        self.setGeometry(100, 100, 400, 300)
        
        self.calendar_widget = QCalendarWidget(self)
        self.calendar_widget.clicked.connect(self.date_selected)
        
        layout = QVBoxLayout()
        layout.addWidget(self.calendar_widget)
        
        self.setLayout(layout)
        
        self.selected_date = datetime.date.today()
        
    def date_selected(self, date):
        self.selected_date = date.toPyDate()
        self.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Change Time and Date")
        self.setGeometry(100, 100, 600, 200)

        self.folder_label = QLabel(f"Folder: {wipPath}", self)
        self.folder_button = QPushButton("Select Folder", self)
        self.folder_button.clicked.connect(self.select_folder)
        
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(self.folder_button)
        
        self.date_label = QLabel("Date: ", self)

        self.date_entry = QLineEdit(self)
        self.date_entry.setText(datetime.date.today().strftime("%Y-%m-%d"))
        
        self.date_button = QPushButton("Select Date", self)
        self.date_button.clicked.connect(self.select_date)
        
        date_layout = QHBoxLayout()
        date_layout.addWidget(self.date_label)
        date_layout.addWidget(self.date_entry)
        date_layout.addWidget(self.date_button)
        
        self.time_label = QLabel("Start Time: ", self)
        
        self.time_entry = QLineEdit(self)
        self.time_entry.setText("07:00:00")
        
        time_layout = QHBoxLayout()
        time_layout.addWidget(self.time_label)
        time_layout.addWidget(self.time_entry)
        
        # Create the main layout
        main_layout = QVBoxLayout()
        
        # Add widgets and layouts to the main layout
        main_layout.addLayout(folder_layout)
        main_layout.addLayout(date_layout)
        main_layout.addLayout(time_layout)
        
        ok_button = QPushButton("Run", self)
        ok_button.clicked.connect(self.ok_button_clicked)
        
        # Add a Close button
        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.close)
        
        # Add the OK and Close buttons to a QHBoxLayout
        button_layout = QHBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(close_button)
        
        main_layout.addLayout(button_layout)

        # Add a QProgressBar widget
        self.progress_bar = QProgressBar(self)
        main_layout.addWidget(self.progress_bar)
        # Set the format of the progress bar
        self.progress_bar.setFormat("%p%")

        # Add a QLabel widget
        self.file_label = QLabel(self)
        main_layout.addWidget(self.file_label)
        
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        
        self.folder_path = wipPath
        self.selected_date = datetime.date.today()
        self.start_time = datetime.datetime.combine(datetime.date.today(), datetime.time(hour=7))
        
    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        self.folder_path = folder_path
        self.folder_label.setText(f"Folder: {folder_path}")
        
    def select_date(self):
        calendar_dialog = CalendarDialog(self)
        calendar_dialog.exec_()
        self.selected_date = calendar_dialog.selected_date
        self.date_entry.setText(self.selected_date.strftime("%Y-%m-%d"))
        
    def ok_button_clicked(self):
        wipPath = self.folder_path
        selected_date_str = self.date_entry.text()
        selected_date = datetime.datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        start_time_str = self.time_entry.text()
        start_time = datetime.datetime.combine(selected_date, datetime.datetime.strptime(start_time_str, '%H:%M:%S').time())
        change_modification_date(wipPath, subfolders, start_time, selected_date, self.progress_bar, self.file_label)
        # self.close() 

def get_numeric_part(filename):
    # Extract the numeric part of the filename
    numeric_part = ''.join(filter(str.isdigit, os.path.basename(filename)))
    
    # Convert the numeric part to an integer
    return int(numeric_part)

# Set the default folder to ~/Desktop/WIP/[TodaysDate]
wipPath = os.path.join(os.path.expanduser("~"), "Desktop", "WIP", datetime.datetime.now().strftime("%Y-%m-%d") + " DA")
subfolders = ["12", "13", "15", "20", "22", "24", "36"]

def change_modification_date(
    wipPath: str,
    subfolders: list,
    start_time: datetime.datetime,
    selected_date: datetime.date,
    progress_bar: QProgressBar,
    file_label: QLabel
):
    # Initialize ExifTool
    with exiftool.ExifTool() as et:
        # Create a list to store all image files from all subfolders
        all_image_files = []
        
        # Create a dictionary to store the time_per_image for each subfolder
        time_per_image_dict = {}
        
        for subfolder in subfolders:
            # Get the list of image files in the subfolder and sort them by filename
            subfolder_path = os.path.join(wipPath, subfolder)
            image_files = [os.path.join(subfolder_path, f) for f in os.listdir(subfolder_path) if f.endswith(('.jpg', '.jpeg', '.png', '.psd', '.tif', '.tiff'))]
            
            # Check if there are any image files in the subfolder
            if len(image_files) == 0:
                continue
            
            # Calculate the time it takes to edit one image in the subfolder
            num_files_with_01 = len([f for f in image_files if '_01' in f])
            time_per_image = (num_files_with_01 / int(subfolder)) * 60 * 60 / len(image_files)
            
            # Add the time_per_image to the dictionary
            time_per_image_dict[subfolder] = time_per_image
            
            # Add the image files to the all_image_files list
            all_image_files.extend(image_files)

        # Sort all image files by filename
        all_image_files.sort(key=get_numeric_part)

        # Set the range of the progress bar
        progress_bar.setRange(0, len(all_image_files))
        
        # Change the modification date, accessed date, EXIF dates, and XMP dates of all image files
        prev_modification_time = start_time
        first_file = True
        for i, image_file in enumerate(all_image_files):
            # Get the subfolder name from the image file path
            subfolder_name = os.path.basename(os.path.dirname(image_file))
            
            # Get the time_per_image for this image file based on its subfolder
            time_per_image = time_per_image_dict[subfolder_name]
            
            new_modification_time = prev_modification_time + timedelta(seconds=time_per_image)
            
            new_modification_time_str = new_modification_time.strftime('%Y:%m:%d %H:%M:%S')
            et.execute('-overwrite_original', f'-FileModifyDate={new_modification_time_str}', f'-DateTimeDigitized={new_modification_time_str}', f'-XMP:MetadataDate={new_modification_time_str}', f'-XMP:ModifyDate={new_modification_time_str}', f'-EXIF:ModifyDate={new_modification_time_str}', image_file)
            
            prev_modification_time = new_modification_time

            # Update the value of the progress bar
            progress_bar.setValue(i + 1)

            # Update the text of the file label
            if first_file:
                file_label.setText(f"Processing: {os.path.basename(image_file)} (first file)")
                first_file = False
            elif i == len(all_image_files) - 1:
                file_label.setText(f"Processing: {os.path.basename(image_file)} (last file)")
            else:
                file_label.setText(f"Processing: {os.path.basename(image_file)}")
        
        # Show a completion message
        start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time_str = prev_modification_time.strftime('%Y-%m-%d %H:%M:%S')

        file_label.setText(f" Completed!\n\n Time of the 1st file: {start_time_str}\n Time of the last file: {end_time_str}")

# Create an instance of the MainWindow class and show it
app = QApplication([])
main_window = MainWindow()
# apply_stylesheet(app, theme='light_teal.xml')

main_window.show()

# Wait for the
app.exec_()