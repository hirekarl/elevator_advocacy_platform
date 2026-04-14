# Maya Feedback Log

## Design System Violations (2026-04-13)
A Gemini session introduced several violations that required a correction pass:

1. **`bg` is not a valid CSS property in React inline styles.** A `getStatusBadgeStyle()` function returned `{ bg: string, color: string }` spread into inline styles — `bg` was silently ignored, so badge backgrounds never rendered. Use `backgroundColor` or, better, a CSS class.

2. **Never hardcode hex values in JSX inline styles.** `style={{ backgroundColor: '#0d1b2a' }}` was found in two places. Use `var(--c-navy)` or a CSS class. The design system tokens exist precisely to avoid this.

3. **Do not inline `fontFamily: 'Syne, sans-serif'` on arbitrary divs.** The CSS design system applies Syne automatically to `h1`–`h6`. For non-heading elements that need Syne, add a CSS class (e.g., `.home-building-title { font-family: 'Syne', sans-serif; }`).

4. **Do not override Bootstrap variant styles inline.** The UNSAFE report button had `style={{ backgroundColor: '#dc3545' }}` which used Bootstrap's default red instead of the design system's `var(--c-red)` (`#c8281c`). The CSS override on `.btn-danger` handles this — remove the inline style.

5. **Bootstrap Alert inline style overrides.** `<Alert style={{ backgroundColor: '#e8eef5', color: '#0d1b2a' }}>` — the design system has a `.alert-info` CSS override. Use the variant prop and let CSS do its job.

## Correct Pattern Reference
```css
/* Add to index.css — never inline */
.my-new-component { background-color: var(--c-navy); }
.my-status-pill.pill-danger { background-color: var(--c-red); color: #fff; }
```
```tsx
{/* In JSX — use className, not style */}
<div className="my-new-component">...</div>
<span className={`my-status-pill ${getPillClass(status)}`}>...</span>
```
