export async function onRequest(context) {
  const { request } = context;
  
  // Forward all requests to Flask app
  try {
    // Create headers object from request headers
    const headers = {};
    for (const [key, value] of request.headers) {
      headers[key] = value;
    }

    // Get request body if present
    let body = null;
    if (request.body) {
      body = await request.text();
    }

    // Create response object
    return new Response(JSON.stringify({
      method: request.method,
      url: request.url,
      headers: headers,
      body: body
    }), {
      headers: {
        'content-type': 'application/json',
      },
    });
  } catch (err) {
    return new Response(`Error: ${err.message}`, { status: 500 });
  }
} 