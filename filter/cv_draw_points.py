import copy
import cv2
import numpy as np
from typing import List

from filter.color import get_colors
from filter.point import Point

# ----------------------------------------------------------------
def cv_draw_points( cv_image : np.ndarray, points : List[ Point ] ):
    result_image = copy.deepcopy( cv_image )
    if points:
        colors = get_colors( len( points ) )
        for point_index, point in enumerate( points ):
            cv2.circle(
                result_image,
                center      = ( int( point.x ), int( point.y) ),
                radius      = int( 2 ),
                color       = colors[point_index].as_tuple(),
                thickness   = -1, # filled
                lineType    = cv2.LINE_AA
            )
    return result_image