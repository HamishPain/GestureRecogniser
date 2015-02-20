__author__ = 'Finch ThinkPad'
from PIL import Image

class visualiser():
    def __init__(self, gene_length):
        self.gene_length = gene_length
        self.lifespan = 1
        self.history = []
        self.colour = []

    def collect_generation(self, generation_string, colour):
        self.history.append(generation_string)
        self.colour.append(colour)

    def build_visual(self):
        image = Image.new('RGBA', (self.gene_length, len(self.history)))
        pix = image.load()
        for i in range(self.gene_length):
            for j in range(len(self.history)):
                char = self.history[j][i]
                if char == '1':
                    image.putpixel((i,j), self.colour[j])
                else:
                    image.putpixel((i,j), (0, 0, 0))
        image.convert("RGB")
        image.save("visual.tiff", "TIFF")