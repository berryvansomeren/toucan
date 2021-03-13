import cv2

from filter.point import Point

#----------------------------------------------------------------
def get_sift_points(
    image,
    n_sift_points,
    n_sift_octave_layers,
    contrast_threshold,
    edge_threshold,
    sigma
):
    if n_sift_points == 0:
        return []

    sift = cv2.SIFT_create(
        n_sift_points,
        n_sift_octave_layers,
        contrast_threshold  / 100,
        edge_threshold,
        sigma               / 100
    )
    sift_points = sift.detect(image, None)
    sift_points = [ Point(int(point.pt[0]), int(point.pt[1])) for point in sift_points ]
    return sift_points