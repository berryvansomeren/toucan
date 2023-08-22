import numpy as np
from pathlib import Path
from typing import List

from PySide6 import QtCore, QtWidgets

from filter.delauney    import get_delauney_image
from filter.io_cv_image import save_cv_image
from filter.point       import Point
from ui.image_widget    import ImageWidget
from ui.popup_message   import popup_message

# ----------------------------------------------------------------
class TabResult( QtWidgets.QWidget ):

    main_window                     = None

    clean_cv_image : np.ndarray     = None

    save_button                     = None
    image_widget                    = None

    poisson_points  : List[ Point ] = None
    sift_points     : List[ Point ] = None
    edge_points     : List[ Point ] = None

    # ----------------------------------------------------------------
    def __init__( self, main_window ):
        super().__init__()
        self.create_layout()
        self.main_window = main_window
        self.process()

    # ----------------------------------------------------------------
    def create_layout( self ) -> None:

        # The image widget comes below the button for saving
        self.image_widget = ImageWidget()

        # Button for saving the result
        self.save_button = QtWidgets.QPushButton( 'Save image as...' )
        self.save_button.clicked.connect( self.button_function_save_result )

        # create root layout
        root_layout = QtWidgets.QVBoxLayout()
        root_layout.addWidget( self.image_widget )
        root_layout.addWidget( self.save_button )

        # finally set the layout
        self.setLayout( root_layout )

    # ----------------------------------------------------------------
    def set_poisson_points( self, poisson_points : List[ Point ] ):
        self.poisson_points = poisson_points
        self.process()

    # ----------------------------------------------------------------
    def set_sift_points( self, sift_points : List[ Point ] ):
        self.sift_points = sift_points
        self.process()

    # ----------------------------------------------------------------
    def set_edge_points( self, edge_points : List[ Point ] ):
        self.edge_points = edge_points
        self.process()

    # ----------------------------------------------------------------
    def set_cv_image( self, cv_image ) -> None:
        self.clean_cv_image = cv_image
        self.process()

    # ----------------------------------------------------------------
    def process( self ) -> None:
        if self.clean_cv_image is None:
            return

        def extend_if_not_none( extendee, extender ):
            if extender is not None:
                extendee.extend( extender )

        vertices = []
        extend_if_not_none( vertices, self.poisson_points   )
        extend_if_not_none( vertices, self.sift_points      )
        extend_if_not_none( vertices, self.edge_points      )

        cv_image, svg_image = get_delauney_image( self.clean_cv_image, vertices )
        self.image_widget.set_cv_image( cv_image )
        self.svg_image = svg_image

    # ----------------------------------------------------------------
    @QtCore.Slot()
    def button_function_save_result( self ):
        if self.image_widget.image is None:
            popup_message( 'You have not loaded an image yet (see the Load tab)' )
            return

        original_file_path = self.main_window.tab_load.chosen_image_path
        stem = str( original_file_path.stem )
        suggested_save_url_str = str( original_file_path.parent ) + '/' + stem + '_low_poly.png'
        suggested_save_url = QtCore.QUrl.fromLocalFile( suggested_save_url_str )
        save_url, save_filters = QtWidgets.QFileDialog.getSaveFileUrl(
            self,
            'Choose a file to save to',
            suggested_save_url,
            filter = 'Images (*.png *.jpg)' # todo: need to fix this filter
        )
        save_url = save_url.toLocalFile()
        save_url_is_valid = True
        if not save_url:
            save_url_is_valid = False
            # todo: add more checks based on the save_url, it could for example not have a file extension yet
        if save_url_is_valid:
            save_cv_image( save_url, self.image_widget.image.cv_image )
            svg_output_path = Path( save_url ).with_suffix('.svg')
            self.svg_image.saveas( svg_output_path )
            popup_message( f'Successfully saved results to "{save_url}" and "{svg_output_path}".' )
        else:
            popup_message( f'Could not save results to "{save_url}".' ) # todo: add reason to message