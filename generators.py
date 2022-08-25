from PIL import Image
import math

def _limit(command, param):
    if param == "fade":
        return 100
    elif command == "julia":
        if not param == "zoom":
            return 200
        else:
            return 100
    elif command == "multijulia":
        if param == "zoom":
            return 100
        elif param == "n":
            return 10
        else:
            return 200
    elif command == "grayscale_noise":
        return 127

def grayscale_noise(image, sigma=127, fade=100):
    return Image.blend(image, Image.effect_noise(image.size, sigma).convert("RGB"), fade / 100)
    
def mandelbrot(image, quality=100):
    return Image.effect_mandelbrot(image.size, (0, 0, image.width, image.height), quality).convert("RGB")

def _run_julia(w, h, cx, cy, move_x, move_y, zoom):
    julia_image = Image.new("RGB", (w, h), (255, 255, 255))
    julia_pixels = julia_image.load()

    for x in range(w):
        for y in range(h):
            zx = 1.5 * (x - w / 2) / (0.5 * zoom * w) + move_x
            zy = 1 * (y - h / 2) / (0.5 * zoom * h) + move_y
            i = 0
            while zx * zx + zy * zy < 4 and i < 255:
                tmp = zx * zx - zy * zy + cx
                zy = 2 * zx * zy + cy
                zx = tmp
                i += 1
            julia_pixels[x, y] = (i << 21) + (i << 10) + i * 8
    
    return julia_image

def julia(image, cx=179, cy=37, move_x=100, move_y=100, zoom=100):
    return _run_julia(image.width, image.height, (cx - 100) / 100, (cy - 100) / 100, (move_x - 100) / 100, (move_y - 100) / 100, zoom / 100)

def _run_multijulia(w, h, cx, cy, n, move_x, move_y, zoom):
    julia_image = Image.new("RGB", (w, h), (255, 255, 255))
    julia_pixels = julia_image.load()

    for x in range(w):
        for y in range(h):
            zx = 1.5 * (x - w / 2) / (0.5 * zoom * w) + move_x
            zy = (y - h / 2) / (0.5 * zoom * h) + move_y
            i = 0
            while zx * zx + zy * zy < 4 and i < 255:
                tmp = pow(zx * zx - zy * zy + cx, n / 2) * math.cos(n * math.atan2(zy, zx)) + cx
                zy = pow(zx * zx - zy * zy + cx, n / 2) * math.sin(n * math.atan2(zy, zx)) + cy
                zx = tmp
                i += 1
            julia_pixels[x, y] = (i << 21) + (i << 10) + i * 8
    
    return julia_image

def multijulia(image, cx=179, cy=37, n=4, move_x=100, move_y=100, zoom=100):
    return _run_multijulia(image.width, image.height, (cx - 100) / 100, (cy - 100) / 100, n, (move_x - 100) / 100, (move_y - 100) / 100, zoom / 100)
