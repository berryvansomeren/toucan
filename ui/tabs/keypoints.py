from PySide6 import QtWidgets

from filter.cv_draw_points  import cv_draw_points
from filter.sift            import get_sift_points
from ui.slider              import get_slider
from ui.image_widget        import ImageWidget

# ----------------------------------------------------------------
class TabKeypoints( QtWidgets.QWidget ):

    main_window               = None

    clean_cv_image            = None

    slider_n_points           = None
    slider_n_octave_layers    = None
    slider_contrast_threshold = None
    slider_edge_threshold     = None
    slider_sigma              = None

    # ----------------------------------------------------------------
    def __init__( self, main_window ):
        super().__init__()
        self.create_layout()
        self.process()
        self.main_window = main_window

    # ----------------------------------------------------------------
    def set_cv_image( self, cv_image ) -> None:
        self.clean_cv_image = cv_image
        self.process()

    # ----------------------------------------------------------------
    def create_layout( self ) -> None:
        self.slider_n_points            = get_slider( 0, 100, 20 )
        self.slider_n_octave_layers     = get_slider( 3, 8, 3 )
        self.slider_contrast_threshold  = get_slider( 4, 20, 4 )
        self.slider_edge_threshold      = get_slider( 10, 20, 10 )
        self.slider_sigma               = get_slider( 160, 200, 160 )

        all_slider_layouts = [
            self.slider_n_points,
            self.slider_n_octave_layers,
            self.slider_contrast_threshold,
            self.slider_edge_threshold,
            self.slider_sigma
        ]
        for slider_layout in all_slider_layouts:
            slider_layout.valueChanged.connect( self.process )

        sliders_with_names = [
            ( self.slider_n_points,             'SIFT Number of Points'      ),
            ( self.slider_n_octave_layers,      'SIFT Number of Octaves'     ),
            ( self.slider_contrast_threshold,   'SIFT Contrast Threshold'    ),
            ( self.slider_edge_threshold,       'SIFT Edge Thresholds'       ),
            ( self.slider_sigma,                'SIFT Sigma'                 ),
        ]
        sliders_layout = QtWidgets.QGridLayout()
        for row_i, ( slider, name ) in enumerate( sliders_with_names ):
            sliders_layout.addWidget( QtWidgets.QLabel( name ), row_i, 0 )
            sliders_layout.addWidget( slider,                   row_i, 1 )

        # THe image widget comes below the bar for loading the image
        self.image_widget = ImageWidget()

        # create root layout
        root_layout = QtWidgets.QVBoxLayout()
        root_layout.addLayout( sliders_layout )
        root_layout.addWidget( self.image_widget )

        # finally set the layout
        self.setLayout( root_layout )

    # ----------------------------------------------------------------
    def process( self ) -> None:
        if self.clean_cv_image is None:
            return

        points = get_sift_points(
            self.clean_cv_image,
            self.slider_n_points.value(),
            self.slider_n_octave_layers.value(),
            self.slider_contrast_threshold.value(),
            self.slider_edge_threshold.value(),
            self.slider_sigma.value()
        )
        cv_image = cv_draw_points( self.clean_cv_image, points )
        self.image_widget.set_cv_image( cv_image )
        self.main_window.tab_result.set_sift_points( points )
