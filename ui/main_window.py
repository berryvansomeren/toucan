import numpy as np
from PySide6 import QtGui, QtWidgets

from ui.tabs.edges import TabEdges
from ui.tabs.help import TabHelp
from ui.tabs.load import TabLoad
from ui.tabs.uniform import TabUniform
from ui.tabs.result import TabResult
from ui.tabs.keypoints import TabKeypoints

# ----------------------------------------------------------------
def run() -> int:
    app = QtWidgets.QApplication( [ ] )

    window = MainWindow()
    window.resize( 800, 600 )
    window.show()

    exit_code = app.exec_()
    return exit_code

# ----------------------------------------------------------------
class MainWindow( QtWidgets.QWidget ):

    tab_help        = None
    tab_load        = None
    tab_uniform     = None
    tab_edges       = None
    tab_keypoints   = None
    tab_result      = None

    # ----------------------------------------------------------------
    def __init__( self ):
        super().__init__()
        self.setWindowTitle( 'Toucan: low-poly filter' )
        self.setWindowIcon( QtGui.QIcon( 'ui/toucan_icon_100_100.png' ) )
        self.create_layout()

    # ----------------------------------------------------------------
    def create_layout( self ):
        tab_widget = QtWidgets.QTabWidget()

        # we keep references to these tabs because we need ot refer them later
        self.tab_help       = TabHelp()
        self.tab_load       = TabLoad       ( self )
        self.tab_uniform    = TabUniform    ( self )
        self.tab_edges      = TabEdges      ( self )
        self.tab_keypoints  = TabKeypoints  ( self )
        self.tab_result     = TabResult     ( self )

        all_tabs = [
            ( self.tab_help,        'Help'      ),
            ( self.tab_load,        'Load'      ),
            ( self.tab_uniform,     'Uniform'   ),
            ( self.tab_edges,       'Edges'     ),
            ( self.tab_keypoints,   'Keypoints' ),
        ]
        for tab, name in all_tabs:
            tab_widget.addTab( tab, name )

        result_tab_widget = QtWidgets.QTabWidget()
        result_tab_widget.addTab( self.tab_result, 'Result' )

        root_layout = QtWidgets.QHBoxLayout()
        root_layout.addWidget( tab_widget,          1 )
        root_layout.addWidget( result_tab_widget,   1 )

        # finally set the layout
        self.setLayout( root_layout )

    # ----------------------------------------------------------------
    def set_cv_image( self, image : np.ndarray ) -> None:
        tabs_to_update = [
            self.tab_uniform,
            self.tab_edges,
            self.tab_keypoints,
            self.tab_result,
        ]
        for tab in tabs_to_update:
            tab.set_cv_image( image )