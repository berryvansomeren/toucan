import copy
import cv2
from pathlib import Path

# ----------------------------------------------------------------
def load_cv_image( image_path ):
    cv_image = cv2.imread( str( image_path ) )
    assert cv_image is not None
    cv2.cvtColor( cv_image, cv2.COLOR_BGR2RGB, cv_image )
    return cv_image

# ----------------------------------------------------------------
def save_cv_image( image_path, cv_image ):
    result_image = copy.deepcopy( cv_image )
    cv2.cvtColor( result_image, cv2.COLOR_RGB2BGR, result_image )
    cv2.imwrite( image_path, result_image )
    assert Path( image_path ).exists()