// app/static/js/spiral_noise.js
let weights = [];
let maxW = 0;
const DATE = "2025-04-25";

function preload() {
  // load your JSON weights array:
  weights = loadJSON(`/api/weights/${DATE}`, wrap);
}

function wrap(data) {
  // data is an array of {ticker,volatility,weight}
  weights = Object.values(data);
  maxW = max(weights.map(d => d.weight));
}

function setup() {
  createCanvas(windowWidth, windowHeight);
  noFill();
  strokeWeight(1.5);
  colorMode(HSB, 360, 100, 100, 1);
}

function draw() {
  background(0, 0, 10);
  translate(width / 2, height / 2);

  const R = min(width, height) * 0.4;
  const N = weights.length;
  const t = frameCount * 0.005;

  beginShape();
  for (let i = 0; i < N; i++) {
    // angle around circle
    const a = map(i, 0, N, 0, TWO_PI);
    // base radius
    const r0 = map(weights[i].weight, 0, maxW, R * 0.2, R);
    // noise offset
    const n = noise(cos(a) + 1, sin(a) + 1, t);
    // wiggle radius by noise scaled by volatility
    const wiggle = map(n, 0, 1, -20, 20) * weights[i].volatility * 30;
    const r = r0 + wiggle;
    // polar → Cartesian
    const x = r * cos(a);
    const y = r * sin(a);

    // hue ramps around circle
    const h = map(i, 0, N, 0, 360);
    stroke(h, 80, 90, 0.6);
    vertex(x, y);
  }
  endShape(CLOSE);
}

// handle resize
function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}