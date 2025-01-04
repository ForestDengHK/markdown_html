export async function onRequest(context) {
  const { request } = context;
  const url = new URL(request.url);
  
  // Handle static files
  if (url.pathname.startsWith('/static/')) {
    return context.env.ASSETS.fetch(request);
  }

  // Forward all other requests to the Flask app
  try {
    const response = await fetch(`http://127.0.0.1:5000${url.pathname}${url.search}`, {
      method: request.method,
      headers: request.headers,
      body: request.body
    });
    return response;
  } catch (error) {
    return new Response(`Server Error: ${error.message}`, { status: 500 });
  }
} 