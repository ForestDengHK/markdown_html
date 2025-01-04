export async function onRequest(context) {
  const { request, env } = context;
  
  try {
    // First try to serve static assets
    const url = new URL(request.url);
    const path = url.pathname;
    
    // Try to serve from static assets first
    try {
      const asset = await env.ASSETS.fetch(request);
      if (asset.status !== 404) {
        return asset;
      }
    } catch (e) {
      // Continue to dynamic handling if static asset not found
    }

    // For dynamic routes, return the index.html
    if (!path.startsWith('/static/') && !path.endsWith('.ico')) {
      const response = await env.ASSETS.fetch(`${url.origin}/index.html`);
      return new Response(response.body, {
        headers: {
          'content-type': 'text/html;charset=UTF-8',
        },
      });
    }

    // If nothing matched, return 404
    return new Response('Not Found', { status: 404 });
  } catch (err) {
    return new Response(`Internal Server Error: ${err.message}`, { 
      status: 500,
      headers: { 'content-type': 'text/plain' }
    });
  }
} 