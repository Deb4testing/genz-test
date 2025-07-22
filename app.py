from flask import Flask, render_template, request, send_file
import os
from utils import extract_text_from_image, generate_test_cases

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB file upload limit

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        test_type = request.form['test_type']
        test_count = request.form['test_count']

        ui_file = request.files['ui_file']
        template_file = request.files['template_file']

        ui_path = os.path.join(app.config['UPLOAD_FOLDER'], ui_file.filename)
        template_path = os.path.join(app.config['UPLOAD_FOLDER'], template_file.filename)

        ui_file.save(ui_path)
        template_file.save(template_path)

        try:
            ui_elements = extract_text_from_image(ui_path)
            output_file = generate_test_cases(test_type, test_count, ui_elements, template_path)
        finally:
            if os.path.exists(ui_path): os.remove(ui_path)
            if os.path.exists(template_path): os.remove(template_path)

        return send_file(output_file, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
