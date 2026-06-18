from PIL import Image
from tkinter import filedialog, Tk
import os

# Hide the root Tkinter window (we only want the dialog)
root = Tk()
root.withdraw()

# Folder where ASCII text files will be saved
SAVE_FOLDER = r"D:\python coding\Image to ASCII\ASCII"

# Create folder if not exists
os.makedirs(SAVE_FOLDER, exist_ok=True)

# ASCII characters from dark to light
ASCII_CHARS = "@%#*+=-:. "

def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)
    return image.resize((new_width, new_height))

def grayify(image):
    return image.convert("L")

def pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_str = ""
    for pixel in pixels:
        ascii_str += ASCII_CHARS[pixel * len(ASCII_CHARS) // 256]
    return ascii_str

def get_next_filename():
    files = os.listdir(SAVE_FOLDER)
    numbers = []

    for f in files:
        if f.startswith("ASCII_") and f.endswith(".txt"):
            try:
                num = int(f.replace("ASCII_", "").replace(".txt", ""))
                numbers.append(num)
            except:
                pass
    
    next_num = max(numbers) + 1 if numbers else 1
    return os.path.join(SAVE_FOLDER, f"ASCII_{next_num}.txt")


def image_to_ascii(path, new_width=100):
    try:
        image = Image.open(path)
    except Exception as e:
        print("Could not open image:", e)
        return
    
    image = resize_image(image, new_width)
    image = grayify(image)
    ascii_str = pixels_to_ascii(image)

    pixel_count = len(ascii_str)
    ascii_img = "\n".join(
        ascii_str[i:(i + image.width)] for i in range(0, pixel_count, image.width)
    )

    print("\nConverted:", path)

    # Create auto-numbered filename
    output_path = get_next_filename()

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ascii_img)

    print("Saved as:", output_path)


# -------------------------------
# OPEN FILE BROWSER (MULTIPLE SELECT)
# -------------------------------

file_paths = filedialog.askopenfilenames(
    title="Select Images",
    filetypes=[("Image Files", "*.jpg *.png *.jpeg *.bmp *.webp *.gif")]
)

if not file_paths:
    print("No files selected!")
else:
    print("\nSelected", len(file_paths), "images\n")
    for file_path in file_paths:
        image_to_ascii(file_path, new_width=100)

    print("\n✔ ALL IMAGES PROCESSED SUCCESSFULLY ✔")
