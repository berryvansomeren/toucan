import cv2
import numpy as np
from scipy.spatial import Delaunay

#----------------------------------------------------------------
def get_delauney_image( image, seeds ):
    image_height, image_width = image.shape[:2]
    points = [(seed.x, seed.y) for seed in seeds]
    # add corner points of image
    points.extend([(0, 0), (image_width, 0), (0, image_height), (image_width, image_height)])
    delaunay_image = np.zeros((image_height, image_width, 3), np.uint8)
    delauney_triangulation = Delaunay(points)

    for simplex_index, simplex_vertex_indices in enumerate(delauney_triangulation.simplices):
        simplex_vertices = np.array([points[i] for i in simplex_vertex_indices])

        # determine mean color
        mask_image = np.zeros((image_height, image_width, 1), np.uint8)
        cv2.fillConvexPoly(mask_image, simplex_vertices, 1, cv2.LINE_AA)
        mean_color = cv2.mean(image, mask_image)

        # draw simplex in color
        cv2.fillConvexPoly(delaunay_image, simplex_vertices, mean_color, cv2.LINE_AA)

    return delaunay_image