/**
 * Bean scatter positions.
 *
 * Every array is a hand-fixed literal — no `Math.random()` anywhere, at build
 * time or in the browser. Positions are percentages of the containing box, so
 * the layout is identical on every render (no hydration drift, no CLS).
 *
 * x / y   — percentage of the scatter box, measured from its top-left corner.
 *           Negative values deliberately place a bean outside the box.
 * size    — rendered bean size in px.
 * rotate  — degrees, clockwise.
 * opacity — 0..1.
 */

export interface Bean {
  readonly x: number;
  readonly y: number;
  readonly size: number;
  readonly rotate: number;
  readonly opacity: number;
}

/** ~28 beans around the big spotlight latte (box = 520 x 520). */
export const BEANS_FEATURE: readonly Bean[] = [
  { x: 3.5, y: 41.0, size: 20.5, rotate: 91, opacity: 0.88 },
  { x: 7.0, y: 48.4, size: 25.1, rotate: 17, opacity: 0.80 },
  { x: 26.0, y: 13.1, size: 14.6, rotate: 177, opacity: 0.99 },
  { x: 16.3, y: 36.9, size: 14.2, rotate: 95, opacity: 0.74 },
  { x: 26.8, y: 75.3, size: 20.5, rotate: 79, opacity: 0.96 },
  { x: 13.0, y: 32.1, size: 23.3, rotate: 82, opacity: 0.80 },
  { x: 52.2, y: 96.1, size: 23.9, rotate: 57, opacity: 0.78 },
  { x: 41.5, y: 94.2, size: 19.6, rotate: 152, opacity: 0.83 },
  { x: 66.3, y: 79.6, size: 16.9, rotate: 164, opacity: 0.85 },
  { x: 83.2, y: 39.2, size: 22.8, rotate: 140, opacity: 0.80 },
  { x: 8.8, y: 74.5, size: 24.6, rotate: 21, opacity: 0.79 },
  { x: 23.7, y: 25.8, size: 23.0, rotate: 21, opacity: 0.84 },
  { x: 14.5, y: 82.4, size: 25.2, rotate: 55, opacity: 0.97 },
  { x: 6.3, y: 65.4, size: 23.0, rotate: 18, opacity: 1.00 },
  { x: 17.8, y: 81.6, size: 18.6, rotate: 53, opacity: 0.74 },
  { x: 13.9, y: 40.2, size: 22.4, rotate: 67, opacity: 0.85 },
  { x: 92.2, y: 47.9, size: 26.1, rotate: 33, opacity: 0.76 },
  { x: 71.0, y: 81.1, size: 16.7, rotate: 133, opacity: 0.98 },
  { x: 44.2, y: 3.6, size: 22.4, rotate: 76, opacity: 0.75 },
  { x: 46.8, y: 12.8, size: 23.9, rotate: 46, opacity: 0.95 },
  { x: 21.3, y: 72.4, size: 24.1, rotate: 12, opacity: 0.78 },
  { x: 85.4, y: 24.7, size: 17.5, rotate: 50, opacity: 0.92 },
  { x: 73.3, y: 1.2, size: 14.4, rotate: 80, opacity: 0.57 },
  { x: 72.3, y: 11.1, size: 17.1, rotate: 24, opacity: 0.69 },
  { x: 96.7, y: 28.3, size: 17.9, rotate: 124, opacity: 0.78 },
  { x: 99.1, y: 1.4, size: 17.7, rotate: 87, opacity: 0.84 },
  { x: 77.2, y: 28.8, size: 12.7, rotate: 98, opacity: 0.84 },
  { x: 97.0, y: 21.5, size: 18.3, rotate: 143, opacity: 0.92 },
];

/** ~10 beans around the small rosetta that sits at the seam of the two phones. */
export const BEANS_ACCENT: readonly Bean[] = [
  { x: 87.1, y: 31.0, size: 14.4, rotate: 15, opacity: 0.88 },
  { x: 21.5, y: 64.8, size: 9.8, rotate: 35, opacity: 0.83 },
  { x: 55.5, y: 79.9, size: 9.1, rotate: 15, opacity: 0.91 },
  { x: 56.9, y: 17.3, size: 12.9, rotate: 112, opacity: 0.99 },
  { x: 25.7, y: 78.4, size: 11.2, rotate: 103, opacity: 0.90 },
  { x: 41.4, y: 70.2, size: 11.8, rotate: 129, opacity: 0.88 },
  { x: 17.2, y: 61.2, size: 10.1, rotate: 32, opacity: 0.80 },
  { x: 59.8, y: 27.6, size: 9.7, rotate: 18, opacity: 0.71 },
  { x: 44.7, y: 82.7, size: 13.9, rotate: 60, opacity: 0.81 },
  { x: 43.5, y: 76.2, size: 13.7, rotate: 99, opacity: 0.78 },
];

/** ~30 beans spilling out of the shell's bottom-left corner (box = 300 x 230). */
export const BEANS_FOOTER: readonly Bean[] = [
  { x: 1.4, y: 48.0, size: 9.3, rotate: 164, opacity: 0.79 },
  { x: 31.5, y: 75.2, size: 11.1, rotate: 132, opacity: 0.79 },
  { x: 41.8, y: 84.0, size: 14.7, rotate: 79, opacity: 0.58 },
  { x: -15.0, y: 88.9, size: 9.3, rotate: 118, opacity: 0.81 },
  { x: -19.2, y: 93.7, size: 8.3, rotate: 156, opacity: 0.92 },
  { x: -16.3, y: 103.7, size: 13.5, rotate: 176, opacity: 0.53 },
  { x: -3.7, y: 80.6, size: 12.9, rotate: 33, opacity: 0.94 },
  { x: 49.5, y: 54.2, size: 9.2, rotate: 120, opacity: 0.70 },
  { x: 28.6, y: 70.3, size: 11.2, rotate: 4, opacity: 0.57 },
  { x: 8.2, y: 89.3, size: 11.4, rotate: 134, opacity: 0.77 },
  { x: 53.6, y: 83.5, size: 10.6, rotate: 25, opacity: 0.53 },
  { x: 28.3, y: 38.6, size: 15.1, rotate: 118, opacity: 0.87 },
  { x: 22.9, y: 64.1, size: 14.8, rotate: 173, opacity: 0.62 },
  { x: 64.5, y: 52.0, size: 9.7, rotate: 124, opacity: 0.64 },
  { x: 55.7, y: 56.3, size: 15.4, rotate: 68, opacity: 0.94 },
  { x: 38.3, y: 89.6, size: 9.7, rotate: 30, opacity: 0.52 },
  { x: -14.7, y: 56.6, size: 9.8, rotate: 122, opacity: 0.56 },
  { x: 68.3, y: 78.9, size: 13.7, rotate: 99, opacity: 0.75 },
  { x: 64.9, y: 102.2, size: 14.6, rotate: 5, opacity: 0.79 },
  { x: 61.2, y: 82.1, size: 12.1, rotate: 117, opacity: 0.59 },
  { x: -9.5, y: 70.9, size: 12.8, rotate: 42, opacity: 0.59 },
  { x: 9.6, y: 33.2, size: 12.0, rotate: 169, opacity: 0.91 },
  { x: 39.3, y: 44.8, size: 14.4, rotate: 58, opacity: 0.68 },
  { x: -7.2, y: 28.2, size: 14.1, rotate: 131, opacity: 0.69 },
  { x: 18.7, y: 88.7, size: 9.5, rotate: 33, opacity: 0.74 },
  { x: 29.3, y: 91.2, size: 11.0, rotate: 143, opacity: 0.54 },
  { x: 0.5, y: 58.4, size: 14.9, rotate: 31, opacity: 0.58 },
  { x: 48.3, y: 44.8, size: 15.2, rotate: 175, opacity: 0.94 },
  { x: 31.7, y: 102.4, size: 15.3, rotate: 173, opacity: 0.64 },
  { x: 49.9, y: 93.3, size: 10.8, rotate: 30, opacity: 0.95 },
];
