import sys
import math
from datetime import datetime, date
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDateTimeEdit
from PyQt6.QtCore import Qt, QDateTime, QPoint
from PyQt6.QtGui import QPainter, QPen, QColor



def calculate_biorhythm(days, cycle):
    """
    Calculates the biorhythm value for a specific cycle
    """
    return math.sin(2 * math.pi * days / cycle)

def days_between_dates(date1, date2):
    """
    Calculates the number of days between two dates
    """
    return (date2 - date1).days

class BiorhythmWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Biorhythm Calculator")
        # Set the window size
        self.setFixedSize(800, 500)
        # Bildschirmauflösung automatisch ermitteln und Fenster zentrieren
        screen = QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.geometry()
            screen_width = screen_geometry.width()
            screen_height = screen_geometry.height()
            x = int((screen_width - 800) / 2)
            y = int((screen_height - 500) / 2)
            self.move(x, y)
        else:
            self.move(100, 100)  # Fallback-Position
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Upper Area (input)
        input_widget = QWidget()
        input_layout = QHBoxLayout(input_widget)
        
        # Birthdate input box
        birthday_label = QLabel("Birthdate:")
        self.birthday_edit = QDateTimeEdit()
        self.birthday_edit.setDisplayFormat("dd.MM.yyyy")
        self.birthday_edit.setCalendarPopup(True)
        self.birthday_edit.setDate(QDateTime.currentDateTime().date())
        self.birthday_edit.dateChanged.connect(self.update_biorhythm)
        
        # Adding the input fields to the layout
        input_layout.addWidget(birthday_label)
        input_layout.addWidget(self.birthday_edit)
        input_layout.addStretch()
        
        layout.addWidget(input_widget)
        
        # Area for drawing the biorhythm curves
        self.draw_widget = DrawWidget()
        layout.addWidget(self.draw_widget)

    def update_biorhythm(self):
        """
        Updates the biorhythm curves based on the date entered  
        """
        birth_date = self.birthday_edit.date().toPyDate()
        current_date = date.today()  # Current Date
        
        days = days_between_dates(birth_date, current_date)
        
        # Calculate 29 days for display (-14 to +14)
        physical_data = []
        emotional_data = []
        intellectual_data = []
        
        for i in range(-14, 15):
            day = days + i
            physical_data.append(calculate_biorhythm(day, 23))
            emotional_data.append(calculate_biorhythm(day, 28))
            intellectual_data.append(calculate_biorhythm(day, 33))
        
        self.draw_widget.update_curves(physical_data, emotional_data, intellectual_data)

class DrawWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 450)
        self.physical_data = []
        self.emotional_data = []
        self.intellectual_data = []
        
    def update_curves(self, physical, emotional, intellectual):
        """
        Actualizes the data points for the curves
        """
        self.physical_data = physical
        self.emotional_data = emotional
        self.intellectual_data = intellectual
        self.update()  # Draw new widges
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Horizontal Middle line
        painter.setPen(QPen(Qt.GlobalColor.black, 1))
        painter.drawLine(0, self.height()//2, self.width(), self.height()//2)
        
        # Vertical Middle line
        middle_x = self.width()//2
        painter.drawLine(middle_x, 0, middle_x, self.height())
        
        # Vertical help lines
        painter.setPen(QPen(QColor(162, 181, 205), 1))
        spacing = self.width()//29
        
        for i in range(-14, 15):
            x = middle_x + (i * spacing)
            painter.drawLine(x, 0, x, self.height())
            
            if i % 6 == 0:
                painter.drawText(x-10, self.height()-10, str(i))
        
        # draw the biorhythm curves
        if self.physical_data:
            # Physical Curve (Red)
            painter.setPen(QPen(Qt.GlobalColor.red, 2))
            self._draw_curve(painter, self.physical_data, middle_x, spacing)
            
            # Emotional Curve (Green)
            painter.setPen(QPen(Qt.GlobalColor.green, 2))
            self._draw_curve(painter, self.emotional_data, middle_x, spacing)
            
            # Intellectual Curve (Blue)
            painter.setPen(QPen(Qt.GlobalColor.blue, 2))
            self._draw_curve(painter, self.intellectual_data, middle_x, spacing)
            
            # Legend
            legend_y = 20
            # Psychical
            painter.setPen(QPen(Qt.GlobalColor.red, 2))
            painter.drawLine(10, legend_y, 30, legend_y)
            painter.drawText(35, legend_y + 5, "Psychical: (23 Days)")
            # Emotional
            painter.setPen(QPen(Qt.GlobalColor.green, 2))
            painter.drawLine(10, legend_y + 20, 30, legend_y + 20)
            painter.drawText(35, legend_y + 25, "Emotional: (28 Days)")
            # Intellectual
            painter.setPen(QPen(Qt.GlobalColor.blue, 2))
            painter.drawLine(10, legend_y + 40, 30, legend_y + 40)
            painter.drawText(35, legend_y + 45, "Intellectual: (33 Days)")
    
    def _draw_curve(self, painter, data, middle_x, spacing):
        """
        Helper method to draw a single curve
        """
        points = []
        for i, value in enumerate(data):
            x = middle_x + (i - 14) * spacing
            y = self.height()//2 - (value * self.height()//4)
            points.append(QPoint(x, int(y)))
        
        for i in range(len(points)-1):
            painter.drawLine(points[i], points[i+1])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BiorhythmWindow()
    window.show()
    sys.exit(app.exec())
