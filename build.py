import os
import shutil
from app import app

def build():
    """Build static files for Cloudflare Pages."""
    # Create static directory if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')
    
    # Copy static files
    if os.path.exists('static'):
        for file in os.listdir('static'):
            src = os.path.join('static', file)
            dst = os.path.join('public', file)
            if os.path.isfile(src):
                shutil.copy2(src, dst)

if __name__ == '__main__':
    build() 