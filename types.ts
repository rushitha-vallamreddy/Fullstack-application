"use client";
export function highlightJson(text: string): string {
  let parsed: any;
  try {
    parsed = JSON.parse(text);
  } catch {
    return escapeHtml(text);
  }
  const pretty = JSON.stringify(parsed, null, 2);
  return escapeHtml(pretty)
    .replace(
      /("(?:\\.|[^"\\])*")(\s*:)?/g,
      (_m, str, colon) =>
        colon
          ? `<span class="json-key">${str}</span>${colon}`
          : `<span class="json-string">${str}</span>`
    )
    .replace(/\b(true|false)\b/g, '<span class="json-bool">$1</span>')
    .replace(/\bnull\b/g, '<span class="json-null">null</span>')
    .replace(
      /(^|[^"\w])(-?\d+(?:\.\d+)?)/g,
      '$1<span class="json-number">$2</span>'
    );
}

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}
