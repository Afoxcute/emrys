// Polyfills for server-side rendering
if (typeof global !== 'undefined') {
  // Node.js environment
  global.self = global;
  global.window = global;
  global.document = {};
  global.navigator = {};
  global.location = { href: 'http://localhost:3000' };
  global.history = {};
  global.localStorage = {
    getItem: () => null,
    setItem: () => {},
    removeItem: () => {},
    clear: () => {},
  };
  global.sessionStorage = {
    getItem: () => null,
    setItem: () => {},
    removeItem: () => {},
    clear: () => {},
  };
  global.fetch = require('node-fetch');
  global.Headers = require('node-fetch').Headers;
  global.Request = require('node-fetch').Request;
  global.Response = require('node-fetch').Response;
}

// Ensure self is defined
if (typeof self === 'undefined') {
  if (typeof global !== 'undefined') {
    global.self = global;
  } else if (typeof window !== 'undefined') {
    window.self = window;
  }
}
