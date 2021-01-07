import collections
import colorsys
import copy
import cv2
from enum import Enum
import numpy as np
import random
from scipy.spatial import Delaunay

import poisson_disc_sampling

Color = collections.namedtuple("Color", "r, g, b")
Point = collections.namedtuple("Point", "x, y")

TWEAK_MENU_WINDOW = "Tweak Menu"

class Trackbars( Enum ):
    poisson_radius          = "Poisson R"
    poisson_k               = "Poisson K"
    sift_n_points           = "SIFT Pts"
    sift_n_octave_layers    = "SIFT Octs"
    sift_contrast_threshold = "SIFT Cont"
    sift_edge_threshold     = "SIFT Edge"
    sift_sigma              = "SIFT Sigma"
    bilateral_diameter      = "Bi Dia"
    bilateral_sigma_color   = "Bi S Color"
    bilateral_sigma_space   = "Bi S Space"
    canny_diameter          = "Canny Dia"
    canny_sigma_1           = "Canny S 1"
    canny_sigma_2           = "Canny S 2"
    delaunay_n_seeds        = "Dlny Seeds"
    random_seed             = "Rand Seed"

#----------------------------------------------------------------
def get_trackbar( trackbar ):
    value = cv2.getTrackbarPos(trackbar.value, TWEAK_MENU_WINDOW)
    assert value != None
    return value

#----------------------------------------------------------------
def show_image( name, image, block = True ):
    cv2.imshow( name, image )
    if block:
        cv2.waitKey()

#----------------------------------------------------------------
def for_every_pixel( image, f ):
    result = copy.deepcopy( image )
    height, width = image.shape[:2]
    for y in range( height ):
        for x in range( width ):
            pixel = image[ y ][ x ]
            result[ y ][ x ] = f( x, y, pixel )
    return result

#----------------------------------------------------------------
def get_blank_rgb_image(
    height : int,
    width : int
):
    blank_image = np.zeros((height, width, 3), np.uint8)
    blank_image.fill( 255 )
    return blank_image

#----------------------------------------------------------------
def get_poisson_points( image ):
    image_height, image_width = image.shape[:2]
    poisson_radius  = get_trackbar(Trackbars.poisson_radius)
    poisson_coords = poisson_disc_sampling.poisson_disc_samples( image_width, image_height, poisson_radius )
    poisson_points = [ Point( int( point[0] ), int( point[1] ) ) for point in poisson_coords ]
    poisson_image = copy.deepcopy(image)
    colors = get_colors(len(poisson_points))
    for point_index, point in enumerate(poisson_points):
        cv2.circle(
            poisson_image,
            center=(point.x, point.y),
            radius=1,
            color=colors[point_index],
            thickness=-1,
            lineType=cv2.LINE_AA
        )
    cv2.imshow("Poisson", poisson_image)
    return poisson_points

#----------------------------------------------------------------
def get_bilateral_image(image):
    bilateral_diameter = get_trackbar(Trackbars.bilateral_diameter)
    bilateral_sigma_color = get_trackbar(Trackbars.bilateral_sigma_color)
    bilateral_sigma_space = get_trackbar(Trackbars.bilateral_sigma_space)
    bilateral_image = cv2.bilateralFilter(image, bilateral_diameter, bilateral_sigma_color, bilateral_sigma_space)
    cv2.imshow("Bilateral", bilateral_image)
    return bilateral_image

#----------------------------------------------------------------
def get_canny_image(image):
    canny_diameter = get_trackbar(Trackbars.canny_diameter)
    canny_1 = get_trackbar(Trackbars.canny_sigma_1)
    canny_2 = get_trackbar(Trackbars.canny_sigma_2)
    image_canny_edges = cv2.Canny(image, canny_1, canny_2, canny_diameter)
    cv2.imshow("Canny", image_canny_edges)
    return image_canny_edges

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
def get_edge_points(edge_coords):
    n_seeds_trackbar = get_trackbar(Trackbars.delaunay_n_seeds)
    n_seeds = int(( n_seeds_trackbar / 100) * len(edge_coords))
    random_seed = get_trackbar(Trackbars.random_seed)

    n_seeds = max(n_seeds, 1)
    random.seed(random_seed)
    seeds = []
    for i in range(n_seeds):
        x, y = random.choice(edge_coords)
        seeds.append(Point(x, y))
    return seeds

#----------------------------------------------------------------
def get_colors(n):
    s = 1
    v = 1
    h_increment = 1.0 / n
    colors = []
    for i in range( n ):
        h = i * h_increment
        color = colorsys.hsv_to_rgb( h, s, v )
        colors.append( np.multiply( color, 255 ) )
    return colors

#----------------------------------------------------------------
def get_seed_image( image, seeds ):
    colors = get_colors(len(seeds))
    seed_image = copy.deepcopy(image)
    for seed_index, seed in enumerate(seeds):
        cv2.circle(
            seed_image,
            center=(seed.x, seed.y),
            radius=1,
            color=colors[seed_index],
            thickness=-1,
            lineType=cv2.LINE_AA
        )
    cv2.imshow("Seeds", seed_image)
    return seed_image

#----------------------------------------------------------------
def get_delauney_image( image, seeds ):
    image_height, image_width = image.shape[:2]
    points = [(seed.x, seed.y) for seed in seeds]
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
        # cv2.polylines(delaunay_image, [simplex_vertices], True, (0, 0, 0), 1, cv2.LINE_AA)

    cv2.imshow("Delauney", delaunay_image)
    return delaunay_image

#----------------------------------------------------------------
def get_sift_points( image ):
    n_sift_points           = get_trackbar(Trackbars.sift_n_points)
    n_sift_points = max( n_sift_points, 1 )
    n_sift_octave_layers    = get_trackbar(Trackbars.sift_n_octave_layers)
    sift_contrast_threshold = get_trackbar(Trackbars.sift_contrast_threshold) / 100
    sift_edge_threshold     = get_trackbar(Trackbars.sift_edge_threshold)
    sift_sigma              = get_trackbar(Trackbars.sift_sigma) / 100

    sift = cv2.SIFT_create(
        n_sift_points,
        n_sift_octave_layers,
        sift_contrast_threshold,
        sift_edge_threshold,
        sift_sigma
    )
    sift_points = sift.detect(image, None)
    sift_points = [ Point(int(point.pt[0]), int(point.pt[1])) for point in sift_points ]

    image_keypoints = copy.deepcopy(image)
    if sift_points:
        colors = get_colors(len(sift_points))
        for point_index, point in enumerate(sift_points):
            cv2.circle(
                image_keypoints,
                center=(point.x, point.y),
                radius=1,
                color=colors[point_index],
                thickness=-1,
                lineType=cv2.LINE_AA
            )
    cv2.imshow("SIFT", image_keypoints)
    return sift_points

#----------------------------------------------------------------
def combine_points(poisson_points, sift_points, edge_points):
    result = []
    if poisson_points:
        result.extend( poisson_points )
    if sift_points:
        result.extend( sift_points )
    if edge_points:
        result.extend( edge_points )
    return result

#----------------------------------------------------------------
def main() -> None:

    #TODO:
    # - add an overall uniform sampling (see mike bostock)

    image = cv2.imread( "C:/Users/somerb/Desktop/toucan2e_2.jpg" )
    #image = cv2.resize(image, (0,0), fx=0.5, fy=0.5)
    cv2.imshow("Original", image)

    image_gray = image # cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def on_trackbar(v):
        poisson_points  = get_poisson_points( image_gray )

        sift_points     = get_sift_points( image_gray)

        bilateral_image = get_bilateral_image(image_gray)
        canny_image     = get_canny_image( bilateral_image )
        edge_coords     = get_edge_coords( canny_image )
        edge_points     = get_edge_points(edge_coords)

        seeds           = combine_points( poisson_points, sift_points, edge_points )
        seed_image      = get_seed_image( image, seeds )
        delaunay_image  = get_delauney_image(image, seeds)

    cv2.namedWindow(TWEAK_MENU_WINDOW, cv2.WINDOW_NORMAL)
    #cv2.resizeWindow(TWEAK_MENU_WINDOW, 500, 600)

    for trackbar in [
        (Trackbars.poisson_radius,          100,     300      ),
        (Trackbars.sift_n_points,           20,     100     ),
        (Trackbars.sift_n_octave_layers,    3,      8       ),
        (Trackbars.sift_contrast_threshold, 4,      20      ),
        (Trackbars.sift_edge_threshold,     10,     20      ),
        (Trackbars.sift_sigma,              160,    200     ),
        (Trackbars.bilateral_diameter,      20,     30      ),
        (Trackbars.bilateral_sigma_color,   100,    300     ),
        (Trackbars.bilateral_sigma_space,   100,    300     ),
        (Trackbars.canny_diameter,          3,      30      ),
        (Trackbars.canny_sigma_1,           50,     200     ),
        (Trackbars.canny_sigma_2,           50,     200     ),
        (Trackbars.delaunay_n_seeds,        10,     50      ),
        (Trackbars.random_seed,             10,     100     ),
    ]:
        cv2.createTrackbar(trackbar[0].value, TWEAK_MENU_WINDOW, trackbar[1], trackbar[2], on_trackbar)

    on_trackbar(None)
    cv2.waitKey()

#----------------------------------------------------------------
if __name__ == "__main__":
    main()