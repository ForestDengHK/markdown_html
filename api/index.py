from flask import Flask, Request
from app import app as flask_app
import os

def onRequest(context):
    """
    Entry point for Cloudflare Pages Functions
    """
    # Create a Flask request from Cloudflare's request
    request = Request.from_values(
        base_url=context["request"].url,
        method=context["request"].method,
        input_stream=context["request"].body,
        content_length=len(context["request"].body) if context["request"].body else 0,
        content_type=context["request"].headers.get("content-type", ""),
        headers=context["request"].headers,
    )
    
    # Process the request through Flask
    with flask_app.request_context(request):
        response = flask_app.full_dispatch_request()
        return response 