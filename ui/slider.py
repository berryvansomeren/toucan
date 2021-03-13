from PySide6 import QtCore, QtWidgets

# ----------------------------------------------------------------
def get_slider( min_value : int, max_value : int, current_value : int ):
    slider = QtWidgets.QSlider( QtCore.Qt.Horizontal )
    slider.setMinimum( min_value )
    slider.setMaximum( max_value )
    slider.setValue( current_value )
    return slider