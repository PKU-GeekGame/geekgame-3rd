import itertools
from PIL import Image
import os
from pyzbar.pyzbar import decode

os.chdir(os.path.dirname(__file__))

image = Image.open("250.png")

file_names = ["015", "020", "014", "004", "003", "018"]
pos = [(100, 0), (0, 100), (100, 100), (150, 100), (200, 100), (100, 150), (100, 200), (200, 200)]

for a, b in [("012", "011"), ("011", "012")]:
  image.paste(Image.open(a + ".png"), (200, 150))
  for c, d in [("002", "010"), ("010", "002")]:
    image.paste(Image.open(c + ".png"), (150, 200))
    for permutations in itertools.permutations(file_names + [b, d]):
      if Image.open(permutations[-1] + ".png").getpixel((2, 2)) != 0:
        continue
      for i, name in enumerate(permutations):
        image.paste(Image.open(name + ".png"), pos[i])
      result = decode(image)
      if len(result) > 0:
        print(result[0].data.decode("ascii"))