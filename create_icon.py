from PIL import Image

img = Image.open("assets/usb.png")

img.save(
    "assets/usb.ico",
    sizes=[
        (256,256),
        (128,128),
        (64,64),
        (32,32),
        (16,16)
    ]
)

print("Icon created successfully")