from PIL import Image, ImageDraw, ImageFont


def watermark_text(input_image_path,
                   output_image_path,
                   text, pos):
    photo = Image.open(input_image_path)

    # make the image editable
    drawing = ImageDraw.Draw(photo)

    black = (235, 241, 245)  # Color
    font = ImageFont.truetype("Pillow/Tests/fonts/Arial.ttf", 150)  # Font
    drawing.text(pos, text, fill=black, font=font)
    photo.show()
    photo.save(output_image_path)


if __name__ == '__main__':
    img = 'boy.jpg'
    watermark_text(img, 'watermarked.jpg',
                   text='lenargasimov.dev',
                   pos=(100, 100))
