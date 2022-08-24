from PIL import Image
import random

def _limit(command, param):
    if param == "fade":
        return 100
    elif command in ["grayscale_noise", "color_noise"]:
        return 127

def grayscale_noise(image, sigma=127, fade=100):
    return Image.blend(image, Image.effect_noise(image.size, sigma).convert("RGB"), fade / 100)
    
def mandelbrot(image, quality=100, fade=100):
    return Image.blend(image, Image.effect_mandelbrot(image.size, (0, 0, image.width, image.height), quality).convert("RGB"), fade / 100)
