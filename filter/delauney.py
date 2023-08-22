import cv2
import numpy as np
import svgwrite
from scipy.spatial import Delaunay

#----------------------------------------------------------------
def rgb_to_svg_color(rgb):
    return f'rgb({int(round(rgb[0]))},{int(round(rgb[1]))},{int(round(rgb[2]))})'

#----------------------------------------------------------------
def get_delauney_image( image, seeds ):
    image_height, image_width = image.shape[:2]
    points = [(seed.x, seed.y) for seed in seeds]
    # add corner points of image
    points.extend([(0, 0), (image_width, 0), (0, image_height), (image_width, image_height)])
    delauney_triangulation = Delaunay(points)

    cv_delaunay_image = np.zeros( (image_height, image_width, 3), np.uint8 )
    svg_delauney_image = svgwrite.Drawing( profile = 'full' )

    for simplex_index, simplex_vertex_indices in enumerate( delauney_triangulation.simplices ) :
        vertices = [ points[ i ] for i in simplex_vertex_indices ]
        np_vertices = np.array( vertices )

        # determine mean color
        mask_image = np.zeros( (image_height, image_width, 1), np.uint8 )
        cv2.fillConvexPoly( mask_image, np_vertices, 1, cv2.LINE_AA )
        mean_color = cv2.mean( image, mask_image )

        # draw on cv image
        cv2.fillConvexPoly( cv_delaunay_image, np_vertices, mean_color, cv2.LINE_AA )

        # draw on svg image
        polygon = svg_delauney_image.polygon( points = vertices, fill = rgb_to_svg_color( mean_color ) )
        polygon[ 'shape-rendering' ] = "crispEdges"
        svg_delauney_image.add( polygon )

    return cv_delaunay_image, svg_delauney_image
