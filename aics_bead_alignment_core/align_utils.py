from aicsimageio import AICSImage
import cv2 as cv


def align(
    raw_image_path_one, raw_image_path_two, scene="", eval_method="cv.TM_CCOEFF_NORMED"
) -> tuple:

    # Read in Images as AICSImage
    img1 = AICSImage(raw_image_path_one)
    img2 = AICSImage(raw_image_path_two)

    # AICS Image defaults to the first scene
    if scene != "":
        img1.set_scene(scene)
        img2.set_scene(scene)

    # Building images from AICSImage, C and Z can be varied if image is not accurate
    temp_image_1 = img1.get_image_data("XY", C=0, Z=0, S=0, T=0)
    temp_image_2 = img2.get_image_data("XY", C=0, Z=0, S=0, T=0)

    # Image Formatting
    temp_image_1 = cv.normalize(temp_image_1, None, 0, 255, cv.NORM_MINMAX).astype(
        "uint8"
    )
    temp_image_2 = cv.normalize(temp_image_2, None, 0, 255, cv.NORM_MINMAX).astype(
        "uint8"
    )

    # Creating a padded template (Padding 250 Pixels)
    template = temp_image_2[250:-250, 250:-250]
    # w, h = template.shape[::-1] # Likely used later to adjust (250)

    # Evaluate matches
    method = eval(eval_method)
    res = cv.matchTemplate(temp_image_1, template, method)
    _, _, min_loc, max_loc = cv.minMaxLoc(res)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc

    # Determining shift
    shift = [top_left[0] - 250, top_left[1] - 250]

    # adjust for rotation by AicsImage
    adjusted_shift = (-shift[1], shift[0])

    return adjusted_shift