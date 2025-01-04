from flask import Flask, Request
from app import app as flask_app

def onRequest(context):
    """
    Entry point for Cloudflare Pages Functions
    """
    try:
        # Get request data
        request = context.get('request', {})
        method = request.get('method', 'GET')
        headers = dict(request.get('headers', {}))
        url = request.get('url', '')
        body = request.get('body', '')

        # Create Flask request
        flask_request = Request.from_values(
            base_url=url,
            method=method,
            headers=headers,
            input_stream=body.encode() if body else None
        )

        # Handle the request through Flask
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
            'headers': {'Content-Type': 'text/plain'},
            'body': f'Internal Server Error: {str(e)}'
        } 