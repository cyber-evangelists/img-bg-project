from PIL import Image
from rembg import remove
import math



def replace_background(input_path, background_path):
    # Read the input image
    input_image = Image.open(input_path).convert("RGBA")

    # Remove the image background using the "rembg" library
    removed_bg_image = remove(input_image, alpha_matting=True)
    print("background removed")
    # Load the new background image
    background_image = Image.open(background_path).convert("RGBA")

    # Resize the background image to match the input image size
    background_image = background_image.resize(input_image.size, Image.BICUBIC)

    # Paste the input image onto the new background
    new_image = Image.alpha_composite(background_image, removed_bg_image)
    print("Done")
    return new_image









# Define a function to automatically crop an image
def autocrop_image(img, border=0):
    """
    Automatically crop an image while preserving the original aspect ratio.

    Args:
        img (PIL.Image.Image): The input image.
        border (int): The width of the border to add around the cropped image.

    Returns:
        PIL.Image.Image: The cropped and bordered image.
    """
    # Get the bounding box of the image
    bbox = img.getbbox()

    # Crop the image to the contents of the bounding box
    img = img.crop(bbox)

    # Determine the scale and height of the cropped image
    (scale, height) = img.size

    # Add a border
    scale += border * 2
    height += border * 2

    # Create a new image object for the output image
    cropped_image = Image.new("RGBA", (scale, height), (0, 0, 0, 0))

    # Paste the cropped image onto the new image with a border
    cropped_image.paste(img, (border, border))

    # Return the cropped image
    return cropped_image


# Define a function to resize an image while maintaining the aspect ratio
def resize_image(img, myScale):
    """
    Resize an image while maintaining the aspect ratio.

    Args:
        img (PIL.Image.Image): The input image.
        myScale (int): The desired size for the larger dimension (width or height).

    Returns:
        PIL.Image.Image: The resized image.
    """

    img_width, img_height = img.size

    if img_height > img_width:  # Portrait image
        hpercent = (myScale / float(img_height))
        wsize = int((float(img_width) * float(hpercent)))
        resized_img = img.resize((wsize, myScale), Image.Resampling.LANCZOS)
    elif img_width > img_height:  # Landscape image
        wpercent = (myScale / float(img_width))
        hsize = int((float(img_height) * float(wpercent)))
        resized_img = img.resize((myScale, hsize), Image.Resampling.LANCZOS)

    return resized_img


# Define a function to resize the canvas and center the image
def resize_canvas(img, canvas_width, canvas_height):
    """
    Resize the canvas and center the image on it.

    Args:
        img (PIL.Image.Image): The input image.
        canvas_width (int): The width of the canvas.
        canvas_height (int): The height of the canvas.

    Returns:
        PIL.Image.Image: The image centered on the new canvas.
    """
    old_width, old_height = img.size

    # Center the image on the new canvas
    x1 = int(math.floor((canvas_width - old_width) / 2))
    y1 = int(math.floor((canvas_height - old_height) / 2))

    # Determine the background color based on the image mode
    mode = img.mode
    if len(mode) == 1:  # L, 1
        new_background = (255)
    if len(mode) == 3:  # RGB
        new_background = (255, 255, 255)
    if len(mode) == 4:  # RGBA, CMYK
        new_background = (255, 255, 255, 255)

    # Create a new image with the specified background color and dimensions
    newImage = Image.new(mode, (canvas_width, canvas_height), new_background)

    # Paste the image onto the new canvas, centering it
    newImage.alpha_composite(
        img, ((canvas_width - old_width) // 2, (canvas_height - old_height) // 2))

    # Return the new image
    return newImage

# Define a route to process images and remove the background
def remove_bg(img):
    print('inside')
    # Remove the image background using the "rembg" library
    removedBGimage = remove(img, True)
    print('removing')

    # Automatically crop the image
    # croppedImage = autocrop_image(removedBGimage, 0)
    # print('croping')
    # # Resize the cropped image to a specific size (700 pixels in this case)
    # resizedImage = resize_image(croppedImage, 700)
    # print('resizing')
    # # Create a new canvas with a specific size (1000x1000) and paste the image onto it
    # combinedImage = resize_canvas(resizedImage, 1000, 1000)
    print('resizing canvas')
    return removedBGimage