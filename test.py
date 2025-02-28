from pathlib import Path
from PIL import Image


filepath = Path("C:/Users/asrs/Desktop/ASRS/asrs-project/photo1.jpeg")

print(filepath)

image = Image.open(filepath)
