from typing import List

from filter.point import Point
from filter.poisson_disc_sampling import poisson_disc_samples

# ----------------------------------------------------------------
def get_poisson_points( image_height : int, image_width : int, poisson_radius : float, poisson_random_seed : int ) -> List[ Point ]:
    poisson_coords = poisson_disc_samples( image_width, image_height, poisson_radius, poisson_random_seed )
    poisson_points = [ Point( int( point[0] ), int( point[1] ) ) for point in poisson_coords ]
    return poisson_points