from flask import Flask, request, send_file, render_template, jsonify
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', vehicle=VEHICLE_DATA)

@app.route('/remove-background', methods=['POST'])
def remove_background():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
            
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
            
        input_image = Image.open(file)
        output_image = remove(input_image)
        
        byte_io = io.BytesIO()
        output_image.save(byte_io, 'PNG')
        byte_io.seek(0)
        
        return send_file(
            byte_io,
            mimetype='image/png',
            as_attachment=False,
            download_name='removed_bg.png'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
