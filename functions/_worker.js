export default {
  async fetch(request, env) {
    try {
      // Handle static files
      const url = new URL(request.url);
      if (url.pathname.startsWith('/static/')) {
        const response = await env.ASSETS.fetch(request);
        if (response.status === 200) {
          return response;
        }
      }

      // Forward to Flask application
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
}; 