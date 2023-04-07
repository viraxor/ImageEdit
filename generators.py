from PIL import Image
import math

def _limit(command, param):
    if param == "fade":
        return 100
    elif command == "multijulia":
        if param == "zoom":
            return 100
        elif param == "n":
            return 10
        else:
            return 200
    elif command in ["tricorn", "julia", "mandelbrot", "burning_ship"]:
        if param != "zoom":
            return 200
        else:
            return 100
    elif command == "grayscale_noise":
        return 127

def grayscale_noise(image, sigma=127, fade=100):
    return Image.blend(image, Image.effect_noise(image.size, sigma).convert("RGB"), fade / 100)

def _run_mandelbrot(w, h, zoom, move_x, move_y):
    mandelbrot_image = Image.new("RGB", (w, h), (255, 255, 255))
    mandelbrot_pixels = mandelbrot_image.load()

    for px in range(w):
        for py in range(h):
            x0 = 1.5 * (px - w / 2) / (0.5 * zoom * w) + move_x
            y0 = 1 * (py - h / 2) / (0.5 * zoom * h) + move_y
            x = 0
            y = 0

            i = 0
            while x * x + y * y < 4 and i < 255:
                tmp = x * x - y * y + x0
                y = 2 * x * y + y0
                x = tmp
                i += 1

            mandelbrot_pixels[px, py] = (i << 21) + (i << 10) + i * 8

    return mandelbrot_image
    
def mandelbrot(image, zoom=100, move_x=100, move_y=100):
    return _run_mandelbrot(image.width, image.height, zoom / 100, (move_x - 100) / 100, (move_y - 100) / 100)
        
def _run_tricorn(w, h, zoom, move_x, move_y):
    tricorn_image = Image.new("RGB", (w, h), (255, 255, 255))
    tricorn_pixels = tricorn_image.load()
    
    for px in range(w):
        for py in range(h):
            x = 1.5 * (px - w / 2) / (0.5 * zoom * w) + move_x
            y = 1 * (py - h / 2) / (0.5 * zoom * h) + move_y
            
            zx = x
            zy = y
            
            i = 0
            while zx * zx + zy * zy < 4 and i < 255:
                xtemp = zx * zx - zy * zy + x
                zy = -2 * zx * zy + y
                zx = xtemp
                
                i += 1
                
            tricorn_pixels[px, py] = (i << 21) + (i << 10) + i * 8
            
    return tricorn_image
    
def tricorn(image, zoom=100, move_x=100, move_y=100):
    return _run_tricorn(image.width, image.height, zoom / 100, (move_x - 100) / 100, (move_y - 100) / 100)

def _run_burning_ship(w, h, zoom, move_x, move_y):
    tricorn_image = Image.new("RGB", (w, h), (255, 255, 255))
    tricorn_pixels = tricorn_image.load()
    
    for px in range(w):
        for py in range(h):
            x = 1.5 * (px - w / 2) / (0.5 * zoom * w) + move_x
            y = 1 * (py - h / 2) / (0.5 * zoom * h) + move_y
            
            zx = x
            zy = y
            
            i = 0
            while zx * zx + zy * zy < 4 and i < 255:
                xtemp = zx * zx - zy * zy + x
                zy = abs(2 * zx * zy) + y
                zx = xtemp
                
                i += 1
                
            tricorn_pixels[px, py] = (i << 21) + (i << 10) + i * 8
            
    return tricorn_image
    
def burning_ship(image, zoom=100, move_x=100, move_y=100):
    return _run_burning_ship(image.width, image.height, zoom / 100, (move_x - 100) / 100, (move_y - 100) / 100)

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

def julia(image, cx=179, cy=37, zoom=100, move_x=100, move_y=100):
    return _run_julia(image.width, image.height, (cx - 100) / 100, (cy - 100) / 100, (move_x - 100) / 100, (move_y - 100) / 100, zoom / 100)

def _run_multijulia(w, h, cx, cy, n, move_x, move_y, zoom):
    julia_image = Image.new("RGB", (w, h), (255, 255, 255))
    julia_pixels = julia_image.load()

    for x in range(w):
        for y in range(h):
            zx = 1.5 * (x - w / 2) / (0.5 * zoom * w) + move_x
            zy = 1 * (y - h / 2) / (0.5 * zoom * h) + move_y
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
