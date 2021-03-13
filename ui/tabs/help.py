from PySide6 import QtCore, QtWidgets

# ----------------------------------------------------------------
class TabHelp( QtWidgets.QWidget ):

    # ----------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.create_layout()

    # ----------------------------------------------------------------
    def create_layout( self ):
        help_text = (
            "<h1>Thanks for using Berry's low-poly filter <b style='color: #ef9126'>Toucan</b></h1>"
            "<p>"
                "Using this program you can give your images an artsy low-poly effect. "
                "Every step in the process has it's own tab in this window. "
                "It's recommended you go though them from left to right, "
                "but you can always go back to make changes. "
                "Here I'll walk you through what each of the steps do. "
                "The gist of it is that we place vertices in the image based on different criteria. "
                "In the end the delauney triangulation of these vertices is computed, "
                "and for each triangle the mean color of the underlying pixels is taken. "
                "If, BTW, some words are used that you don't understand, "
                "that's fine. Just toy around with all the sliders until you get something you like."
            "</p>"
            "<p style='color: #FF0000'>"
                "Warning: The operations in this program can be heavy, especially for larger images. "
                "It can happen that the program freezes for a while. Just give it some time to process"
            "</p>"
            "<ol>"
                "<li> <b>Load</b> - This tab is for loading the image you would like to work on.</li>"
                "<li> <b>Uniform</b> - Here we place vertices by uniformly sampling the image. This might already be enough for you to create a nice looking image, "
                    "so you could already take a look at the Result tab to see if you're already satisfied. "
                    "The other steps are to bring back a bit more detail.</li>"
                "<li> <b>Edges</b> - Here we detect edges in the image to place additional vertices on. This should make the contours of objects more clear in the resulting low-poly image."
                "<li> <b>Keypoints</b> - Here we use keypoint detection to determine points in the image that stand out the most. By adding these vertices we hope to capture the most important areas of the image better. This usually has little effect on the final result, but provides a final opportunity to include a few highlights in the image."
                "<li> <b>Result</b> - Here you can see the final result and <b style='color: #FF0000'>Save</b> it. </li>"
            "</ol>"
            "<p>"
                "Have fun!"
            "</p>"
        )

        help_label = QtWidgets.QTextEdit( help_text )
        help_label.setReadOnly(True)
        help_label.setAlignment( QtCore.Qt.AlignLeft )

        # create root layout
        root_layout = QtWidgets.QVBoxLayout()
        root_layout.addWidget( help_label )

        # finally set the layout
        self.setLayout( root_layout )