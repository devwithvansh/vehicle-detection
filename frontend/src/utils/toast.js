export function toast(message) {
  window.dispatchEvent(new CustomEvent('toast', { detail: message }))
}
