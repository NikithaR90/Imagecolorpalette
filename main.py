from flask import Flask, render_template, request
import numpy as np
from PIL import Image

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        image = Image.open(file)
        colors = get_top_colors(image)
        return render_template('result.html', colors=colors)


def get_top_colors(image):
    # Resize image to reduce computation time
    image = image.resize((100, 100))
    # Convert image to RGB
    image = image.convert('RGB')
    # Get colors from image
    data = np.array(image)
    colors, counts = np.unique(data.reshape(-1, 3), axis=0, return_counts=True)
    # Sort colors by frequency
    sorted_indices = np.argsort(-counts)
    top_colors = colors[sorted_indices][:10]  # Top 10 colors
    top_counts = counts[sorted_indices][:10]  # Counts of top 10 colors
    total_pixels = sum(top_counts)
    # Prepare colors with their percentages
    color_percentages = [{'color': '#%02x%02x%02x' % tuple(color), 'percentage': f"{(count / total_pixels) * 100:.2f}%"} for color, count in zip(top_colors, top_counts)]
    return color_percentages


if __name__ == '__main__':
    app.run(debug=True)
