import os
import shutil
from app import app

def build():
    """Build static files for Cloudflare Pages."""
    # Create public directory
    if os.path.exists('public'):
        shutil.rmtree('public')
    os.makedirs('public')
    
    # Copy static files
    if os.path.exists('static'):
        shutil.copytree('static', 'public/static', dirs_exist_ok=True)
    
    print("Build completed successfully")

if __name__ == '__main__':
    build() 