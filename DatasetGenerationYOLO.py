import os
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, 
                             QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsPixmapItem, QMessageBox, QInputDialog)
from PyQt5.QtGui import QPixmap, QImage, QPen, QFont, QPainter
from PyQt5.QtCore import Qt, QRectF
from PIL import Image

class ImageLabelerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.image_folder = ""
        self.images_list = []
        self.current_image_index = 0
        self.labels = []
        self.start_x = None
        self.start_y = None
        self.rect_item = None
        self.image_name = ""

        # Create required folders if they do not exist
        os.makedirs('Dataset/Images', exist_ok=True)
        os.makedirs('Dataset/Labels', exist_ok=True)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('YOLO Image Labeler')
        self.setGeometry(100, 100, 1600, 900)  # Set a larger window size

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Header Label
        header_label = QLabel('YOLO Image Labeling Tool', self)
        header_label.setFont(QFont('Arial', 24, QFont.Bold))
        header_label.setStyleSheet("color: #333;")
        layout.addWidget(header_label)

        # Path Label
        self.path_label = QLabel('No folder selected', self)
        self.path_label.setFont(QFont('Arial', 14))
        self.path_label.setStyleSheet("color: #666;")
        layout.addWidget(self.path_label)

        # Buttons
        button_layout = QHBoxLayout()  # Horizontal layout for buttons
        self.select_path_button = QPushButton('Select Image Folder', self)
        self.select_path_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border: none; border-radius: 15px;")
        self.select_path_button.clicked.connect(self.select_image_folder)
        button_layout.addWidget(self.select_path_button)

        self.prev_button = QPushButton('Previous Image', self)
        self.prev_button.setStyleSheet("background-color: #FFC107; color: white; padding: 10px; border: none; border-radius: 15px;")
        self.prev_button.clicked.connect(self.prev_image)
        button_layout.addWidget(self.prev_button)

        self.next_button = QPushButton('Next Image', self)
        self.next_button.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; border: none; border-radius: 15px;")
        self.next_button.clicked.connect(self.next_image)
        button_layout.addWidget(self.next_button)

        self.exit_button = QPushButton('Exit', self)
        self.exit_button.setStyleSheet("background-color: #f44336; color: white; padding: 10px; border: none; border-radius: 15px;")
        self.exit_button.clicked.connect(self.exit_app)
        button_layout.addWidget(self.exit_button)

        layout.addLayout(button_layout)

        # Graphics View
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setStyleSheet("border: 1px solid #ccc;")
        layout.addWidget(self.view)

        # Set a stylish window
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
        """)

    def select_image_folder(self):
        self.image_folder = QFileDialog.getExistingDirectory(self, 'Select Image Folder')
        if self.image_folder:
            self.path_label.setText(os.path.basename(self.image_folder))
            
            # List images in the selected folder
            all_images = [f for f in os.listdir(self.image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            # List images already present in the dataset folder
            dataset_images = [f for f in os.listdir(os.path.join('Dataset', 'Images')) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            # Determine the next image to process
            if dataset_images:
                dataset_images.sort()
                all_images.sort()
                self.images_list = [img for img in all_images if img not in dataset_images]
            else:
                self.images_list = all_images
            
            if self.images_list:
                self.current_image_index = 0
                self.show_image()
            else:
                QMessageBox.information(self, 'No New Images', 'No new images to process.')

    def show_image(self):
        if not self.images_list:
            QMessageBox.information(self, 'No Images', 'No images found in the selected folder.')
            return

        if self.current_image_index >= len(self.images_list):
            QMessageBox.information(self, 'End', 'All images have been processed.')
            return

        self.image_name = self.images_list[self.current_image_index]
        image_path = os.path.join(self.image_folder, self.image_name)
        image = Image.open(image_path)
        image = image.convert("RGB")
        image_qt = QImage(image.tobytes(), image.width, image.height, image.width * 3, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image_qt)

        self.scene.clear()
        self.pixmap_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.pixmap_item)

        # Set the scene rect to the size of the pixmap
        self.scene.setSceneRect(QRectF(pixmap.rect()))

        # Set view to the size of the scene
        self.view.setScene(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setRenderHint(QPainter.SmoothPixmapTransform)

        # Set the view to fit the image in actual size
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setRenderHint(QPainter.Antialiasing)

        # Ensure event handlers are correctly set
        self.pixmap_item.setAcceptedMouseButtons(Qt.LeftButton)
        self.pixmap_item.mousePressEvent = self.on_canvas_click
        self.pixmap_item.mouseMoveEvent = self.on_mouse_drag
        self.pixmap_item.mouseReleaseEvent = self.on_mouse_release

        # Reset rectangle item
        self.rect_item = None
        self.start_x, self.start_y = None, None

    def on_canvas_click(self, event):
        self.start_x = event.pos().x()
        self.start_y = event.pos().y()
        self.rect_item = QGraphicsRectItem()
        
        # Define the pen style for the rectangle
        pen = QPen(Qt.red, 2, Qt.SolidLine)  # Set a fixed width and style
        self.rect_item.setPen(pen)
        
        self.scene.addItem(self.rect_item)

    def on_mouse_drag(self, event):
        if self.start_x is not None and self.start_y is not None:
            current_x = event.pos().x()
            current_y = event.pos().y()
            self.rect_item.setRect(QRectF(self.start_x, self.start_y, current_x - self.start_x, current_y - self.start_y))

    def on_mouse_release(self, event):
        if self.start_x is not None and self.start_y is not None:
            class_name, ok = QInputDialog.getText(self, 'Class Name', 'Enter class name:')
            if ok and class_name:
                # Get image dimensions
                image_item = self.pixmap_item
                image_width = image_item.pixmap().width()
                image_height = image_item.pixmap().height()

                # Calculate YOLO format values
                rect = self.rect_item.rect()
                x_center = (rect.x() + rect.width() / 2) / image_width
                y_center = (rect.y() + rect.height() / 2) / image_height
                width = rect.width() / image_width
                height = rect.height() / image_height

                # Save label in YOLO format
                label_entry = f"{class_name} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n"
                label_file_name = os.path.splitext(self.image_name)[0] + '.txt'
                label_file_path = os.path.join('Dataset', 'Labels', label_file_name)

                # Save annotation immediately
                with open(label_file_path, 'a') as label_file:
                    label_file.write(label_entry)

                # Save the image to Dataset/Images
                image_save_path = os.path.join('Dataset', 'Images', self.image_name)
                image = self.pixmap_item.pixmap().toImage()
                image.save(image_save_path)

                # Remove from images_list to avoid re-processing
                if self.image_name in self.images_list:
                    self.images_list.remove(self.image_name)

                QMessageBox.information(self, 'Label Added', f'Label added: {class_name}')
            else:
                # Remove the rectangle if no name is provided
                self.scene.removeItem(self.rect_item)
                self.rect_item = None
                QMessageBox.warning(self, 'Error', 'Class name cannot be empty.')

            self.start_x, self.start_y = None, None

    def next_image(self):
        if not self.image_folder or not self.images_list:
            QMessageBox.critical(self, 'Error', 'No images loaded.')
            return

        # Go to the next image
        self.current_image_index += 1
        if self.current_image_index >= len(self.images_list):
            self.current_image_index = len(self.images_list) - 1
            QMessageBox.information(self, 'End', 'You are at the last image.')
        self.show_image()

    def prev_image(self):
        if not self.image_folder or not self.images_list:
            QMessageBox.critical(self, 'Error', 'No images loaded.')
            return

        # Go to the previous image
        self.current_image_index -= 1
        if self.current_image_index < 0:
            self.current_image_index = 0
            QMessageBox.information(self, 'Start', 'You are already at the first image.')
        self.show_image()

    def exit_app(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageLabelerApp()
    ex.show()
    sys.exit(app.exec_())
