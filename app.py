import os
import sys

# 1. Import TensorFlow FIRST to prevent Windows C++ runtime DLL conflicts with PyQt5
import tensorflow as tf

import cv2
import numpy as np
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QImage, QPainter, QPen
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from src.predict import SketchPredictor


class DrawingCanvas(QWidget):

  def __init__(self, parent=None):
    super().__init__(parent)
    self.setFixedSize(400, 400)
    self.image = QImage(self.size(), QImage.Format_RGB32)
    self.image.fill(Qt.white)
    self.drawing = False
    self.brush_size = 10
    self.brush_color = Qt.black
    self.last_point = QPoint()

  def clear(self):
    self.image.fill(Qt.white)
    self.update()

  def set_brush_size(self, size):
    self.brush_size = size

  def mousePressEvent(self, event):
    if event.button() == Qt.LeftButton:
      self.drawing = True
      self.last_point = event.pos()

  def mouseMoveEvent(self, event):
    if (event.buttons() & Qt.LeftButton) and self.drawing:
      painter = QPainter(self.image)
      painter.setPen(
          QPen(
              self.brush_color,
              self.brush_size,
              Qt.SolidLine,
              Qt.RoundCap,
              Qt.RoundJoin,
          )
      )
      painter.drawLine(self.last_point, event.pos())
      self.last_point = event.pos()
      self.update()

  def mouseReleaseEvent(self, event):
    if event.button() == Qt.LeftButton:
      self.drawing = False

  def paintEvent(self, event):
    canvas_painter = QPainter(self)
    canvas_painter.drawImage(self.rect(), self.image, self.image.rect())

  def get_opencv_image(self):
    ptr = self.image.bits()
    ptr.setsize(self.image.byteCount())
    arr = np.array(ptr).reshape(self.height(), self.width(), 4)
    return cv2.cvtColor(arr, cv2.COLOR_BGRA2BGR)


class MainWindow(QMainWindow):

  def __init__(self):
    super().__init__()
    self.setWindowTitle("AI Sketch - Reconnaissance d'Objets (ANI-2083)")
    self.predictor = SketchPredictor()
    os.makedirs("gallery", exist_ok=True)

    layout = QVBoxLayout()

    self.result_label = QLabel(
        "Dessinez un objet puis cliquez sur 'Reconnaître'"
    )
    self.result_label.setAlignment(Qt.AlignCenter)
    self.result_label.setStyleSheet(
        "font-size: 16px; font-weight: bold; color: #1e293b; padding: 8px;"
    )
    layout.addWidget(self.result_label)

    self.canvas = DrawingCanvas()
    layout.addWidget(self.canvas, alignment=Qt.AlignCenter)

    slider_box = QHBoxLayout()
    slider_box.addWidget(QLabel("Épaisseur du trait :"))
    self.slider = QSlider(Qt.Horizontal)
    self.slider.setRange(4, 28)
    self.slider.setValue(10)
    self.slider.valueChanged.connect(self.canvas.set_brush_size)
    slider_box.addWidget(self.slider)
    layout.addLayout(slider_box)

    btn_box = QHBoxLayout()

    self.btn_rec = QPushButton("🔍 Reconnaître")
    self.btn_rec.clicked.connect(self.on_recognize)
    btn_box.addWidget(self.btn_rec)

    self.btn_clr = QPushButton("🗑️ Effacer")
    self.btn_clr.clicked.connect(self.on_clear)
    btn_box.addWidget(self.btn_clr)

    self.btn_save = QPushButton("💾 Enregistrer")
    self.btn_save.clicked.connect(self.on_save)
    btn_box.addWidget(self.btn_save)

    self.btn_art = QPushButton("🎨 Filtre Néon")
    self.btn_art.clicked.connect(self.on_filter)
    btn_box.addWidget(self.btn_art)

    layout.addLayout(btn_box)

    container = QWidget()
    container.setLayout(layout)
    self.setCentralWidget(container)

  def on_recognize(self):
    img = self.canvas.get_opencv_image()
    label, conf = self.predictor.predict(img)
    self.result_label.setText(
        f"Résultat : {label.upper()} ({conf} % de confiance)"
    )

  def on_clear(self):
    self.canvas.clear()
    self.result_label.setText(
        "Dessinez un objet puis cliquez sur 'Reconnaître'"
    )

  def on_save(self):
    img = self.canvas.get_opencv_image()
    path, _ = QFileDialog.getSaveFileName(
        self, "Sauvegarder", "gallery/dessin.png", "Images (*.png *.jpg)"
    )
    if path:
      cv2.imwrite(path, img)
      self.result_label.setText(f"Enregistré dans {os.path.basename(path)}")

  def on_filter(self):
    img = self.canvas.get_opencv_image()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    neon = cv2.applyColorMap(edges, cv2.COLORMAP_JET)
    cv2.imshow("Filtre Artistique - Contours Neon", neon)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
  app = QApplication(sys.argv)
  win = MainWindow()
  win.show()
  sys.exit(app.exec_())