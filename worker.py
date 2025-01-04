from app import app

def handle_request(request):
    """Handle incoming requests."""
    return app(request)

def main(request, env):
    """Main entry point for the Cloudflare Worker."""
    return handle_request(request) 