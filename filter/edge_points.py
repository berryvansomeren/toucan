import copy
import cv2
import random

from filter.point import Point

#----------------------------------------------------------------
def get_bilateral_image(
    cv_image,
    diameter,
    sigma_color,
    sigma_space
):
    result_image = copy.deepcopy( cv_image )
    result_image = cv2.bilateralFilter( result_image, diameter, sigma_color, sigma_space )
    return result_image

#----------------------------------------------------------------
def get_canny_image( cv_image, diameter, canny_1, canny_2 ):
    result_image = copy.deepcopy( cv_image )
    result_image_single_chanel = cv2.Canny( result_image, canny_1, canny_2, diameter)
    result_image = cv2.merge( ( result_image_single_chanel, result_image_single_chanel, result_image_single_chanel ) )
    return result_image_single_chanel, result_image

#----------------------------------------------------------------
def get_edge_coords( image ):
    image_height, image_width = image.shape[:2]
    edge_coords = []
    for y in range(image_height):
        for x in range(image_width):
            pixel = image[y][x]
            if pixel == 255:
                edge_coords.append([x, y])
    return edge_coords

#----------------------------------------------------------------
def get_edge_points( edge_coords, edge_point_percentage, random_seed ):
    n_seeds = int(( edge_point_percentage ) * len(edge_coords))
    random.seed(random_seed)
    seeds = []
    for i in range(n_seeds):
        x, y = random.choice(edge_coords)
        seeds.append(Point(x, y))
    return seeds