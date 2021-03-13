from PySide6 import QtWidgets

from filter.edge_points     import get_bilateral_image, get_canny_image, get_edge_coords, get_edge_points
from filter.cv_draw_points  import cv_draw_points
from ui.slider              import get_slider
from ui.image_widget        import ImageWidget

# ----------------------------------------------------------------
class TabEdges( QtWidgets.QWidget ):

    clean_cv_image                  = None

    slider_bilateral                = None
    slider_bilateral_sigma_color    = None
    slider_bilateral_sigma_space    = None

    slider_canny_diamater           = None
    slider_canny_1                  = None
    slider_canny_2                  = None

    slider_n_edge_points            = None
    slider_random_seed              = None

    # ----------------------------------------------------------------
    def __init__( self, main_window ):
        super().__init__()
        self.create_layout()
        self.process()
        self.main_window = main_window

    # ----------------------------------------------------------------
    def create_layout( self ):

        self.slider_n_edge_points           = get_slider( 0, 100, 1 )
        self.slider_random_seed             = get_slider( 0, 20, 0 )

        self.slider_bilateral_diameter      = get_slider( 20, 30, 20 )
        self.slider_bilateral_sigma_color   = get_slider( 100, 300, 150 )
        self.slider_bilateral_sigma_space   = get_slider( 100, 300, 150 )

        self.slider_canny_diamater          = get_slider( 3, 30, 3 )
        self.slider_canny_1                 = get_slider( 50, 200, 100 )
        self.slider_canny_2                 = get_slider( 50, 200, 100 )

        all_slider_layouts = [
            self.slider_n_edge_points,
            self.slider_random_seed,

            self.slider_bilateral_diameter,
            self.slider_bilateral_sigma_color,
            self.slider_bilateral_sigma_space,

            self.slider_canny_diamater,
            self.slider_canny_1,
            self.slider_canny_2,
        ]
        for slider_layout in all_slider_layouts:
            slider_layout.valueChanged.connect( self.process )

        sliders_with_names = [
            ( self.slider_n_edge_points,            'Percentage of Edge Points' ),
            ( self.slider_random_seed,              'Edge Point Random Seed'    ),

            ( self.slider_bilateral_diameter,       'Bilateral Diameter'        ),
            ( self.slider_bilateral_sigma_color,    'Bilateral Sigma Color'     ),
            ( self.slider_bilateral_sigma_space,    'Bilateral Sigma Space'     ),

            ( self.slider_canny_diamater,           'Canny Diameter'            ),
            ( self.slider_canny_1,                  'Canny 1'                   ),
            ( self.slider_canny_2,                  'Canny 2'                   ),
        ]
        sliders_layout = QtWidgets.QGridLayout()
        for row_i, (slider, name) in enumerate( sliders_with_names ):
            sliders_layout.addWidget( QtWidgets.QLabel( name ), row_i, 0 )
            sliders_layout.addWidget( slider, row_i, 1 )

        # THe image widget comes below the bar for loading the image
        self.image_widget = ImageWidget()

        # create root layout
        root_layout = QtWidgets.QVBoxLayout()
        root_layout.addLayout( sliders_layout )
        root_layout.addWidget( self.image_widget )

        # finally set the layout
        self.setLayout( root_layout )

    # ----------------------------------------------------------------
    def set_cv_image( self, cv_image ) -> None:
        self.clean_cv_image = cv_image
        self.process()

    # ----------------------------------------------------------------
    def process( self ) -> None:
        if self.clean_cv_image is None:
            return

        cv_image = get_bilateral_image(
            self.clean_cv_image,
            self.slider_bilateral_diameter.value(),
            self.slider_bilateral_sigma_color.value(),
            self.slider_bilateral_sigma_space.value()
        )

        cv_canny_image_single_channel, cv_canny_image = get_canny_image(
            cv_image,
            self.slider_canny_diamater.value(),
            self.slider_canny_1.value(),
            self.slider_canny_2.value()
        )

        edge_coords = get_edge_coords( cv_canny_image_single_channel )

        edge_points_percentage  = self.slider_n_edge_points.value() / 100
        edge_points_random_seed = self.slider_random_seed,

        edge_points     = get_edge_points( edge_coords, edge_points_percentage, edge_points_random_seed )
        cv_result_image = cv_draw_points( cv_canny_image, edge_points )

        self.image_widget.set_cv_image( cv_result_image )
        self.main_window.tab_result.set_edge_points( edge_points )