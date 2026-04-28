import qrcode
from PIL import Image, ImageDraw

# Load the image you want to overlay
overlay_image = Image.open("static/vllm-logo.png").convert("RGBA")

# Create a QR code instance
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=32,
    border=1,
)

# Add data to the QR code
qr.add_data("https://github.com/vllm-project/vllm")
qr.make(fit=True)

# Create an image from the QR code instance
qr_img: Image = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

# Resize the overlay image to fit within the QR code
# overlay_image = overlay_image.resize((qr_img.size[0] // 3, qr_img.size[1] // 3))
# overlay_image.thumbnail((qr_img.size[0] // 2, qr_img.size[1] // 2))
# overlay_image.thumbnail((qr_img.size[0], qr_img.size[1]))

# Calculate the position to paste the overlay image
position = (
    (qr_img.size[0] - overlay_image.size[0]) // 2,
    (qr_img.size[1] - overlay_image.size[1]) // 2,
)

qr_img.alpha_composite(overlay_image, position)
# img = Image.alpha_composite(qr_img, overlay_image)
# Save the final QR code image
qr_img.save("static/qr-vllm-project.png")
