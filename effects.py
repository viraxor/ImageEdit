from PIL import Image, ImageOps, ImageEnhance, ImageFilter

def _limit(command, param):
    if param == "fade":
        return 100
    elif command == "quantize":
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

def spread(image, distance=50, fade=100):
    return Image.blend(image, image.effect_spread(distance), fade / 100)
    
def quantize(image, colors=128, fade=100):
    return Image.blend(image, image.quantize(colors).convert("RGB"), fade / 100)
    
def rotate(image, degrees=45, fade=100):
    return Image.blend(image, image.rotate(degrees), fade / 100)
    
def autocontrast(image, cutoff=0, fade=100):
    return Image.blend(image, ImageOps.autocontrast(image, cutoff), fade / 100)
    
def equalize(image, fade=100):
    return Image.blend(image, ImageOps.equalize(image), fade / 100)
    
def flip(image, fade=100):
    return Image.blend(image, ImageOps.flip(image), fade / 100)
    
def grayscale(image, fade=100):
    return Image.blend(image, ImageOps.grayscale(image).convert("RGB"), fade / 100)
    
def invert(image, fade=100):
    return Image.blend(image, ImageOps.invert(image), fade / 100)

def mirror(image, fade=100):
    return Image.blend(image, ImageOps.mirror(image), fade / 100)
    
def posterize(image, bits=4, fade=100):
    return Image.blend(image, ImageOps.posterize(image, bits).convert("RGB"), fade / 100)
    
def solarize(image, threshold=128, fade=100):
    return Image.blend(image, ImageOps.solarize(image, threshold), fade / 100)
    
def brightness(image, factor=50, fade=100):
    return Image.blend(image, ImageEnhance.Brightness(image).enhance(factor / 100), fade / 100)
    
def color(image, factor=50, fade=100):
    return Image.blend(image, ImageEnhance.Color(image).enhance(factor / 100), fade / 100)
    
def contrast(image, factor=50, fade=100):
    return Image.blend(image, ImageEnhance.Contrast(image).enhance(factor / 100), fade / 100)
    
def sharpness(image, factor=50, fade=100):
    return Image.blend(image, ImageEnhance.Sharpness(image).enhance(factor / 100), fade / 100)
    
def gaussian_blur(image, radius=2, fade=100):
    return Image.blend(image, image.filter(ImageFilter.GaussianBlur(radius)), fade / 100)
    
def unsharp_mask(image, radius=2, percent=150, threshold=3, fade=100):
    return Image.blend(image, image.filter(ImageFilter.UnsharpMask(radius, percent, threshold)), fade / 100)

def _run_total_rgb(x):
    if x >= 128: x = 255
    else: x = 0
    return x

def total_rgb(image, fade=100):
    return Image.blend(image, Image.eval(image, _run_total_rgb), fade / 100)
    
def geek(image, minus=254, times=15, fade=100):
    return Image.blend(image, Image.eval(image, (lambda x: minus - x * times)), fade / 100)
