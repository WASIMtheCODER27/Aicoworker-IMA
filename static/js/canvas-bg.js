/**
 * AI CareerPilot - Animated Canvas Background & Visual Effects
 * Provides a futuristic cyber-horizon particle mesh with reactive cursor ripples.
 */

(function () {
  'use strict';

  const canvas = document.getElementById('bg-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let width = (canvas.width = window.innerWidth);
  let height = (canvas.height = window.innerHeight);

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Particle Mesh Configuration
  const PARTICLE_COUNT = Math.min(Math.floor((width * height) / 18000), 75);
  const particles = [];
  const ripples = [];

  const mouse = {
    x: width / 2,
    y: height / 2,
    targetX: width / 2,
    targetY: height / 2,
    isActive: false
  };

  class Particle {
    constructor() {
      this.reset();
    }

    reset() {
      this.x = Math.random() * width;
      this.y = Math.random() * height;
      this.vx = (Math.random() - 0.5) * 0.6;
      this.vy = (Math.random() - 0.5) * 0.6;
      this.radius = Math.random() * 1.8 + 0.8;
      this.alpha = Math.random() * 0.4 + 0.15;
      this.baseAlpha = this.alpha;
      // Vibrant neon palette: Cyan (#00f0ff), Deep Purple (#8a2be2), Electric Green (#00ff9d)
      const colors = ['rgba(0, 240, 255, ', 'rgba(138, 43, 226, ', 'rgba(0, 255, 157, '];
      this.colorPrefix = colors[Math.floor(Math.random() * colors.length)];
    }

    update() {
      if (prefersReducedMotion) return;

      this.x += this.vx;
      this.y += this.vy;

      // Wrap boundaries
      if (this.x < 0) this.x = width;
      if (this.x > width) this.x = 0;
      if (this.y < 0) this.y = height;
      if (this.y > height) this.y = 0;

      // React to mouse proximity
      if (mouse.isActive) {
        const dx = mouse.x - this.x;
        const dy = mouse.y - this.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 140) {
          const force = (140 - dist) / 140;
          this.x -= (dx / dist) * force * 1.5;
          this.y -= (dy / dist) * force * 1.5;
          this.alpha = Math.min(0.85, this.baseAlpha + force * 0.5);
        } else {
          this.alpha = this.baseAlpha;
        }
      }
    }

    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = this.colorPrefix + this.alpha + ')';
      ctx.shadowBlur = 6;
      ctx.shadowColor = this.colorPrefix + '0.6)';
      ctx.fill();
      ctx.shadowBlur = 0;
    }
  }

  class ClickRipple {
    constructor(x, y) {
      this.x = x;
      this.y = y;
      this.radius = 2;
      this.maxRadius = Math.random() * 60 + 90;
      this.alpha = 0.6;
      this.color = Math.random() > 0.5 ? 'rgba(0, 240, 255, ' : 'rgba(168, 85, 247, ';
    }

    update() {
      this.radius += 2.8;
      this.alpha *= 0.94;
      return this.alpha > 0.02 && this.radius < this.maxRadius;
    }

    draw() {
      ctx.save();
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.strokeStyle = this.color + this.alpha + ')';
      ctx.lineWidth = 1.5;
      ctx.shadowBlur = 8;
      ctx.shadowColor = this.color + '0.7)';
      ctx.stroke();
      ctx.restore();
    }
  }

  // Initialize Particles
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    particles.push(new Particle());
  }

  // Draw Connecting Constellation Lines
  function drawConnections() {
    const maxDist = 110;
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < maxDist) {
          const lineAlpha = (1 - dist / maxDist) * 0.16;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(138, 43, 226, ${lineAlpha})`;
          ctx.lineWidth = 0.8;
          ctx.stroke();
        }
      }
    }
  }

  // Draw Ambient Cyber Horizon Grid Gradient
  function drawHorizonGlow() {
    const gradient = ctx.createRadialGradient(
      width / 2, height * 0.25, 50,
      width / 2, height * 0.45, Math.max(width, height) * 0.85
    );
    gradient.addColorStop(0, 'rgba(45, 12, 75, 0.35)');
    gradient.addColorStop(0.5, 'rgba(10, 10, 22, 0.6)');
    gradient.addColorStop(1, 'rgba(4, 5, 11, 0.95)');

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, width, height);
  }

  // Animation Loop
  let animationFrameId;
  function animate() {
    ctx.clearRect(0, 0, width, height);

    // Render Atmospheric Glow
    drawHorizonGlow();

    // Smooth Mouse Tracking
    mouse.x += (mouse.targetX - mouse.x) * 0.1;
    mouse.y += (mouse.targetY - mouse.y) * 0.1;

    // Connect & Draw Particles
    drawConnections();
    for (let i = 0; i < particles.length; i++) {
      particles[i].update();
      particles[i].draw();
    }

    // Update & Render Click Ripples
    for (let i = ripples.length - 1; i >= 0; i--) {
      if (ripples[i].update()) {
        ripples[i].draw();
      } else {
        ripples.splice(i, 1);
      }
    }

    if (!prefersReducedMotion) {
      animationFrameId = requestAnimationFrame(animate);
    }
  }

  // Listeners
  window.addEventListener('resize', () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
    if (prefersReducedMotion) {
      drawHorizonGlow();
      drawConnections();
    }
  });

  window.addEventListener('mousemove', (e) => {
    mouse.targetX = e.clientX;
    mouse.targetY = e.clientY;
    mouse.isActive = true;
  });

  window.addEventListener('mouseleave', () => {
    mouse.isActive = false;
  });

  // Click Wave Effect
  window.addEventListener('click', (e) => {
    if (ripples.length < 10) {
      ripples.push(new ClickRipple(e.clientX, e.clientY));
    }
  });

  // Start Animation
  animate();

  // Tasteful Text Scramble Effect on Hover
  const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!<>-_\\/[]{}—=+*^?#________";
  function attachScrambleEffect(el) {
    let interval = null;
    const originalText = el.getAttribute('data-text') || el.innerText;

    el.addEventListener('mouseenter', () => {
      let iteration = 0;
      clearInterval(interval);

      interval = setInterval(() => {
        el.innerText = originalText
          .split("")
          .map((letter, index) => {
            if (index < iteration) {
              return originalText[index];
            }
            return letters[Math.floor(Math.random() * letters.length)];
          })
          .join("");

        if (iteration >= originalText.length) {
          clearInterval(interval);
        }
        iteration += 1 / 2;
      }, 30);
    });
  }

  document.querySelectorAll('.scramble-hover').forEach(attachScrambleEffect);

})();
