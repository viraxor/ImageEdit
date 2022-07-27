from PIL import Image, ImageOps, ImageEnhance, ImageFilter

def _limit(command, param):
    if command == "quantize":
        return 256
    elif command == "rotate":
        return 360
    elif command == "autocontrast":
        return 50
    elif command == "posterize":
        return 8
    elif command == "solarize":
        return 255
    elif command == "unsharp_mask":
        if param == "percent":
            return 200
    elif command in ["brightness", "color", "contrast", "sharpness"]:
        return 200
    elif command == "geek":
        if param == "minus":
            return 255
        elif param == "times":
            return 30
    elif command == "hue":
        return 128

def spread(image, distance=50):
    return image.effect_spread(distance)
    
def quantize(image, colors=128):
    return image.convert("RGB").quantize(colors)
    
def rotate(image, degrees=45):
    return image.rotate(degrees)
    
def autocontrast(image, cutoff=0):
    return ImageOps.autocontrast(image.convert("RGB"), cutoff)
    
def equalize(image):
    return ImageOps.equalize(image.convert("RGB"))
    
def flip(image):
    return ImageOps.flip(image)
    
def grayscale(image):
    return ImageOps.grayscale(image.convert("RGB"))
    
def invert(image):
    return ImageOps.invert(image.convert("RGB"))

def mirror(image):
    return ImageOps.mirror(image)
    
def posterize(image, bits=4):
    return ImageOps.posterize(image.convert("RGB"), bits)
    
def solarize(image, threshold=128):
    return ImageOps.solarize(image.convert("RGB"), threshold)
    
def brightness(image, factor=50):
    return ImageEnhance.Brightness(image.convert("RGB")).enhance(factor / 100)
    
def color(image, factor=50):
    return ImageEnhance.Color(image.convert("RGB")).enhance(factor / 100)
    
def contrast(image, factor=50):
    return ImageEnhance.Contrast(image.convert("RGB")).enhance(factor / 100)
    
def sharpness(image, factor=50):
    return ImageEnhance.Sharpness(image.convert("RGB")).enhance(factor / 100)
    
def gaussian_blur(image, radius=2):
    return image.filter(ImageFilter.GaussianBlur(radius))
    
def unsharp_mask(image, radius=2, percent=150, threshold=3):
    return image.filter(ImageFilter.UnsharpMask(radius, percent, threshold))

def _run_total_rgb(x):
    if x >= 128: x = 255
    else: x = 0
    return x

def total_rgb(image):
    return Image.eval(image, _run_total_rgb)
    
def geek(image, minus=254, times=15):
    return Image.eval(image, (lambda x: minus - x * times))
