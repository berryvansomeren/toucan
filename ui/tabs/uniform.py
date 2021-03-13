from PySide6 import QtWidgets

from ui.slider              import get_slider
from ui.image_widget        import ImageWidget
from filter.cv_draw_points  import cv_draw_points
from filter.poisson         import get_poisson_points

# ----------------------------------------------------------------
class TabUniform( QtWidgets.QWidget ):

    main_window             = None

    clean_cv_image          = None
    slider_poisson_radius   = None

    # ----------------------------------------------------------------
    def __init__(self, main_window):
        super().__init__()
        self.create_layout()
        self.process()
        self.main_window = main_window

    # ----------------------------------------------------------------
    def create_layout( self ) -> None:
        self.slider_poisson_radius      = get_slider( 5, 100, 20 )
        self.slider_poisson_random_seed = get_slider( 0, 20, 0 )

        all_slider_layouts = [
            self.slider_poisson_radius,
            self.slider_poisson_random_seed,
        ]
        for slider_layout in all_slider_layouts:
            slider_layout.valueChanged.connect( self.process )

        sliders_with_names = [
            ( self.slider_poisson_radius,       'Poisson Radius'        ),
            ( self.slider_poisson_random_seed,  'Poisson Random Seed'   ),
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
    def process( self ) -> None:
        if self.clean_cv_image is None:
            return

        poisson_points = get_poisson_points(
            *self.clean_cv_image.shape[:2],
            self.slider_poisson_radius.value(),
            self.slider_poisson_random_seed.value()
        )
        cv_image = cv_draw_points( self.clean_cv_image, poisson_points )
        self.image_widget.set_cv_image( cv_image )

        self.main_window.tab_result.set_poisson_points( poisson_points )

    # ----------------------------------------------------------------
    def set_cv_image( self, cv_image ) -> None:
        self.clean_cv_image = cv_image
        self.process()