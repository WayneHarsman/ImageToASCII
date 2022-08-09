import getopt
import sys
from PIL import Image, ImageOps, ImageEnhance

# don`t read this shit
def main(argv):
    path = ''
    xres, yres = 40, 20
    contrast = 1
    brightness = 1
    try:
        opts, args = getopt.getopt(argv, "hi:x:y:c:b:", ["ifile="])
    except getopt.GetoptError:
        print("conv -i <file path>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("conv -i <file path>")
        elif opt == '-i':
            path = arg
        elif opt == '-x':
            xres = int(arg)
        elif opt == '-y':
            yres = int(arg)
        elif opt == '-c':
            contrast = float(arg)
        elif opt == '-b':
            brightness = float(arg)

    convert(path, xres, yres, contrast, brightness)


def convert(path: str, x: int, y: int, contrast: float, brightness: float):
    original = Image.open(path)
    # prepare image
    contr_enhance = ImageEnhance.Contrast(original)
    original = contr_enhance.enhance(contrast)
    brigh_enchance = ImageEnhance.Brightness(original)
    original = brigh_enchance.enhance(brightness)
    grayscale = ImageOps.grayscale(original)

    width, height = original.size
    hor_step = width // x
    vert_step = height // y

    with open("symbols.txt", 'r') as file:
        symbols: str = file.read().rstrip()
    mapper = ASCIIMapper(symbols)

    for i in range(y):
        for j in range(x):
            area = (j * hor_step, i * vert_step, (j + 1) * hor_step, (i + 1) * vert_step)
            crop = grayscale.crop(area)
            exp = get_exposure(crop)
            sym = mapper.map_symbol(exp)
            print(sym, end='')
        print()


def get_exposure(image: Image) -> int:
    width, height = image.size
    exposure = 0
    for i in range(width):
        for j in range(height):
            exposure += image.getpixel((i, j))

    return int(exposure / (width * height))


class ASCIIMapper:
    def __init__(self, symbols):
        self.symbols = symbols
        self.step = 255 / len(symbols)

    def map_symbol(self, exposure: int) -> str:
        ind: int = int(exposure // self.step) - 1
        ind = max((0, ind))
        return self.symbols[ind]

if __name__ == '__main__':
    main(sys.argv[1:])
