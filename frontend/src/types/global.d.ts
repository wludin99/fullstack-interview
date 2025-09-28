declare global {
  var fetch: typeof globalThis.fetch;
  var require: NodeRequire;
  var global: typeof globalThis;
  var TextEncoder: typeof globalThis.TextEncoder;
  var TextDecoder: typeof globalThis.TextDecoder;
  var Response: typeof globalThis.Response;
  var Headers: typeof globalThis.Headers;
}

export {};
