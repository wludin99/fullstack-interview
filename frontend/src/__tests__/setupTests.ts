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