import handler from './index.py';

export async function onRequest(context) {
  const { request } = context;
  
  try {
    // Call the Python handler
    const response = await handler(request);
    
    // Return the response
    return new Response(response.body, {
      status: response.statusCode,
      headers: response.headers
    });
  } catch (err) {
    return new Response(`Error: ${err.message}`, { 
      status: 500,
      headers: { 'Content-Type': 'text/plain' }
    });
  }
} 