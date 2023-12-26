from PIL import Image
from rembg import remove



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