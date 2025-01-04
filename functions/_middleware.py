from flask import Flask, Request
from app import app as flask_app

def onRequest(context):
    """
    Middleware to handle all routes
    """
    try:
        request = context.get('request', {})
        flask_request = Request.from_values(
            base_url=request.get('url', ''),
            method=request.get('method', 'GET'),
            headers=dict(request.get('headers', {})),
            input_stream=request.get('body', '').encode() if request.get('body') else None
        )
        
        with flask_app.request_context(flask_request):
            response = flask_app.full_dispatch_request()
            return response
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e),
            'headers': {'Content-Type': 'text/plain'}
        } 