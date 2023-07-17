import cv2
from PIL import Image, ImageOps
import numpy as np
import imageio
import os

ASCII_CHARS = '@%#*+=-:. '

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width / 1.65
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def image_to_ascii(image):
    image = image.convert('L')
    pixels = np.array(image)
    ascii_str = ''
    for row in pixels:
        for pixel_value in row:
            ascii_str += ASCII_CHARS[pixel_value // 32]
        ascii_str += '\n'
    return ascii_str

def main():
    video_capture = cv2.VideoCapture(0)
    frames = []
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        image = ImageOps.mirror(image)  # Mirror the image for a more natural view
        image = resize_image(image)
        ascii_str = image_to_ascii(image)
        print(ascii_str)
        frames.append(np.array(image))
        if len(frames) >= 30:  # Number of frames to keep
            frames.pop(0)  # Remove the oldest frame
        if cv2.waitKey(1) == 27:  # Press Esc to exit
            break
    video_capture.release()
    cv2.destroyAllWindows()

    # Save frames as animated GIF in the same directory as the Python file
    file_path = os.path.join(os.getcwd(), 'output.gif')
    imageio.mimsave(file_path, frames, fps=10)

if __name__ == '__main__':
    main()
