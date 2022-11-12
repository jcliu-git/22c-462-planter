export function calcColor(min: number, max: number, val: number): string {
  var minHue = 255,
    maxHue = 0;
  var curPercent = (val - min) / (max - min);
  var colString = `rgb(${255 * (1 - curPercent)}, ${255 * curPercent}, 0)`;
  return colString;
}
