import '@testing-library/jest-dom';

// TextEncoder polyfill for MSW v2
// @ts-ignore
global.TextEncoder = global.TextEncoder || class TextEncoder {
  encode(input: string): Uint8Array {
    const utf8 = unescape(encodeURIComponent(input));
    const bytes = new Uint8Array(utf8.length);
    for (let i = 0; i < utf8.length; i++) {
      bytes[i] = utf8.charCodeAt(i);
    }
    return bytes;
  }
};

// @ts-ignore
global.TextDecoder = global.TextDecoder || class TextDecoder {
  decode(input: Uint8Array): string {
    const bytes = Array.from(input);
    const utf8 = String.fromCharCode.apply(null, bytes);
    return decodeURIComponent(escape(utf8));
  }
};

// Response polyfill for MSW v2
// @ts-ignore
global.Response = global.Response || class Response {
  constructor(body?: any, init?: ResponseInit) {
    this.body = body;
    this.status = init?.status || 200;
    this.statusText = init?.statusText || 'OK';
    this.headers = new Headers(init?.headers);
  }

  body: any;
  status: number;
  statusText: string;
  headers: Headers;

  async json() {
    return JSON.parse(this.body);
  }

  async text() {
    return this.body;
  }
};

// Headers polyfill
// @ts-ignore
global.Headers = global.Headers || class Headers {
  private headers: Map<string, string> = new Map();

  constructor(init?: HeadersInit) {
    if (init) {
      if (Array.isArray(init)) {
        init.forEach(([key, value]) => this.headers.set(key, value));
      } else if (typeof init === 'object') {
        Object.entries(init).forEach(([key, value]) => this.headers.set(key, value));
      }
    }
  }

  get(name: string): string | null {
    return this.headers.get(name) || null;
  }

  set(name: string, value: string): void {
    this.headers.set(name, value);
  }

  has(name: string): boolean {
    return this.headers.has(name);
  }
};

// Add missing polyfills for MSW v2
// @ts-ignore
global.BroadcastChannel = global.BroadcastChannel || class BroadcastChannel {
  constructor(name: string) {
    this.name = name;
  }
  name: string;
  postMessage() {}
  close() {}
  addEventListener() {}
  removeEventListener() {}
};

// @ts-ignore
global.TransformStream = global.TransformStream || class TransformStream {
  constructor() {}
};