from flask import Flask, render_template, request, send_file
import io
import zipfile
from markitdown import MarkItDown
import os
import logging
from pathlib import Path

# Create static/images directory if it doesn't exist
if not os.path.exists('static/images'):
    os.makedirs('static/images')

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'  # Use /tmp for Cloudflare
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

# Initialize MarkItDown instance
md_converter = MarkItDown()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Ensure upload folder exists
@app.before_request
def setup_upload_folder():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

def convert_file(file_obj, filename):
    """Convert a file to markdown with proper error handling."""
    temp_path = None
    try:
        # Get the file content
        content = file_obj.read()
        file_obj.seek(0)  # Reset file pointer for potential reuse
        
        # Save content to temporary file
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(temp_path, 'wb') as f:
            f.write(content)
        
        file_size = len(content)
        logger.info(f"Converting file: {filename}, size: {file_size} bytes")
        
        # Convert using markitdown
        result = md_converter.convert(temp_path)
            
        if result is None:
            logger.error(f"Conversion failed for {filename}: converter returned None")
            raise ValueError("Conversion failed - no result returned")
            
        md_content = result.text_content
        if not md_content:
            logger.warning(f"Conversion resulted in empty content for {filename}")
            md_content = ""  # Return empty string instead of raising error
            
        # Clean up
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        
        return md_content
    except Exception as e:
        logger.error(f"Error converting {filename}: {str(e)}")
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        raise
    finally:
        # Ensure cleanup in all cases
        try:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
        except:
            pass

@app.route('/')
def home():
    return render_template('convert.html', active_page='convert')

@app.route('/convert', methods=['GET', 'POST'])
def convert():
    if request.method == 'POST':
        if 'files' not in request.files:
            return "No files uploaded", 400
            
        uploaded_files = request.files.getlist('files')
        if not uploaded_files or uploaded_files[0].filename == '':
            return "No files selected", 400

        # If only one file, return .md directly
        if len(uploaded_files) == 1:
            file_ = uploaded_files[0]
            try:
                md_content = convert_file(file_, file_.filename)
                logger.info(f"File converted successfully: {len(md_content)} bytes")
                
                md_filename = file_.filename.rsplit('.', 1)[0] + ".md"
                return send_file(
                    io.BytesIO(md_content.encode('utf-8')),
                    mimetype='text/markdown',
                    as_attachment=True,
                    download_name=md_filename
                )
            except Exception as e:
                logger.error(f"Error processing file {file_.filename}: {str(e)}")
                return f"Error converting file: {str(e)}", 500
        else:
            # Multiple files => zip them
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as z:
                for file_ in uploaded_files:
                    try:
                        md_content = convert_file(file_, file_.filename)
                        logger.info(f"File converted successfully: {len(md_content)} bytes")
                        
                        md_filename = file_.filename.rsplit('.', 1)[0] + ".md"
                        z.writestr(md_filename, md_content.encode('utf-8'))
                    except Exception as e:
                        logger.error(f"Error processing file {file_.filename}: {str(e)}")
                        return f"Error converting file {file_.filename}: {str(e)}", 500

            zip_buffer.seek(0)
            return send_file(
                zip_buffer,
                mimetype='application/zip',
                as_attachment=True,
                download_name='converted_files.zip'
            )

    return render_template('convert.html', active_page='convert')

@app.route('/donate')
def donate():
    return render_template('donate.html', active_page='donate')

@app.route('/updates')
def updates():
    return render_template('updates.html', active_page='updates')

@app.route('/about')
def about():
    return render_template('about.html', active_page='about')

@app.route('/robots.txt')
def robots():
    return send_file('robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    return send_file('sitemap.xml')

@app.route('/static/images/og-image.png')
def social_preview():
    # Check if the image already exists
    image_path = os.path.join('static', 'images', 'og-image.png')
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/png')
    
    # If image doesn't exist, return a default image or generate one
    # For now, we'll use a static file
    return send_file('static/images/og-image.png', mimetype='image/png')

if __name__ == '__main__':
    app.debug = False  # Disable debug mode in production
    app.run()