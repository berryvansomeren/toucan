from PySide6 import QtWidgets

# ----------------------------------------------------------------
def popup_message( text : str ):
    message_box = QtWidgets.QMessageBox()
    message_box.setText( text )
    message_box.exec_()