from flask import Flask, Request
from app import app as flask_app

def onRequest(context):
    """
    Entry point for Cloudflare Pages Functions
    """
    try:
        request = context.get('request', {})
        # Create Flask request
        flask_request = Request.from_values(
            base_url=request.get('url', ''),
            method=request.get('method', 'GET'),
            headers=dict(request.get('headers', {})),
            input_stream=request.get('body', '').encode() if request.get('body') else None
        )
        
        # Process the request through Flask
        with flask_app.request_context(flask_request):
            response = flask_app.full_dispatch_request()
            return {
                'statusCode': response.status_code,
                'headers': dict(response.headers),
                'body': response.get_data(as_text=True)
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Internal Server Error: {str(e)}',
            'headers': {'Content-Type': 'text/plain'}
        } 