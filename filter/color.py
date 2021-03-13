import colorsys
from dataclasses import dataclass

import numpy as np

# ----------------------------------------------------------------
@dataclass()
class Color:
    r : int
    g : int
    b : int

    def as_tuple( self ):
        return ( self.r, self.g, self.b )

#----------------------------------------------------------------
def get_colors( n ):
    s = 1
    v = 1
    h_increment = 1.0 / n
    colors = []
    for i in range( n ):
        h = i * h_increment
        color = colorsys.hsv_to_rgb( h, s, v )
        colors.append( np.multiply( color, 255 ) )

    result_colors = [ Color( r, g, b ) for r, g, b in colors ]
    return result_colors