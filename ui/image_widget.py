import numpy as np
from typing import Any
from PySide6 import QtWidgets, QtGui

# ----------------------------------------------------------------
def cv_image_to_qt( cv_image ):
    qt_image = QtGui.QImage(
        cv_image.data,
        cv_image.shape[ 1 ],
        cv_image.shape[ 0 ],
        cv_image.strides[ 0 ],
        QtGui.QImage.Format_RGB888
    )
    return qt_image

# ----------------------------------------------------------------
class CvQtImagePair:
    cv_image : np.ndarray # we need to keep this in memory, because the qt image refers to it via pointer
    qt_image : Any

    def __init__( self, cv_image ):
        self.cv_image = cv_image
        self.qt_image = cv_image_to_qt( self.cv_image )

# ----------------------------------------------------------------
def get_coords_to_draw_centered( widget, cv_image ):
    x = ( widget.width()  / 2 ) - ( cv_image.shape[ 1 ] / 2 )
    y = ( widget.height() / 2 ) - ( cv_image.shape[ 0 ] / 2 )
    return x, y

# ----------------------------------------------------------------
class ImageWidget( QtWidgets.QWidget ):
    # This widget is responsible for displaying images and keeping them in memory

    image   = None
    painter = None

    def __init__( self ):
        super().__init__()
        self.painter = QtGui.QPainter()

    def paintEvent( self, QPaintEvent ):
        if self.image is not None:
            self.painter.begin( self )
            self.painter.drawImage( *get_coords_to_draw_centered( self, self.image.cv_image ), self.image.qt_image )
            self.painter.end()

    def set_cv_image( self, cv_image : np.ndarray ) -> None:
        self.image = CvQtImagePair( cv_image )
        self.update()