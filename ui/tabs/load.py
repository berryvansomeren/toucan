from pathlib import Path

from PySide6 import QtCore, QtWidgets

from filter.io_cv_image import load_cv_image
from ui.image_widget    import ImageWidget
from ui.popup_message   import popup_message

# ----------------------------------------------------------------
class TabLoad( QtWidgets.QWidget ):

    main_window             = None

    chosen_image_path       = None
    choose_image_line_edit  = None
    image_widget            = None

    # ----------------------------------------------------------------
    def __init__( self, main_window ):
        super().__init__()
        self.create_layout()
        self.main_window = main_window

    # ----------------------------------------------------------------
    def create_layout( self ):

        # first build the row for choosing input data
        choose_image_label = QtWidgets.QLabel( 'Chosen image url: ' )
        choose_image_label.setAlignment( QtCore.Qt.AlignCenter )

        self.choose_image_line_edit = QtWidgets.QLineEdit()

        choose_image_button = QtWidgets.QPushButton( 'Choose an image...' )
        choose_image_button.clicked.connect( self.button_function_choose_file )

        choose_image_layout = QtWidgets.QHBoxLayout()
        choose_image_layout.addWidget( choose_image_label,          1 )
        choose_image_layout.addWidget( self.choose_image_line_edit, 5 )
        choose_image_layout.addWidget( choose_image_button,         1 )

        # The image widget comes below the bar for loading the image
        self.image_widget = ImageWidget()

        # create root layout
        root_layout = QtWidgets.QVBoxLayout()
        root_layout.addLayout( choose_image_layout )
        root_layout.addWidget( self.image_widget )

        # finally set the layout
        self.setLayout( root_layout )

    # ----------------------------------------------------------------
    @QtCore.Slot()
    def button_function_choose_file( self ):
        chosen_file_url, chosen_file_filters = QtWidgets.QFileDialog.getOpenFileUrl(
            self,
            'Choose a file',
            '/home'
        )
        image_str = chosen_file_url.toLocalFile()

        if not image_str:
            popup_message( f'No image was loaded.' )
            return

        self.choose_image_line_edit.setText( image_str )
        image_path = Path( image_str )

        if not image_path.exists():
            popup_message( f'Could not load image "{image_path}"' )
            return

        self.chosen_image_path = image_path

        cv_image = load_cv_image( image_path )
        self.main_window.set_cv_image( cv_image )
        self.image_widget.set_cv_image( cv_image )