/* ============================================
   ZIFORGE PORTFOLIO — main.js
   Scroll animations, nav behavior, background
   ============================================ */

(function () {
  'use strict';

  // --- Scroll Reveal ---
  function initReveal() {
    // Standard section reveals
    const sections = document.querySelectorAll('.reveal');
    const sectionObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            sectionObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
    );
    sections.forEach((el) => sectionObserver.observe(el));

    // Staggered children — each child gets its own observer with delay
    document.querySelectorAll('.reveal-children').forEach((container) => {
      const children = container.children;
      const childObserver = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add('visible');
              childObserver.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.05, rootMargin: '0px 0px -20px 0px' }
      );
      for (const child of children) {
        childObserver.observe(child);
      }
    });
  }

  // --- Nav: hide on scroll down, show on scroll up ---
  function initNav() {
    const nav = document.querySelector('nav');
    const toggle = document.querySelector('.nav-toggle');
    const links = document.querySelector('.nav-links');
    let lastScroll = 0;
    let ticking = false;

    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          const currentScroll = window.scrollY;
          if (currentScroll > 80) {
            nav.classList.toggle('hidden', currentScroll > lastScroll);
          } else {
            nav.classList.remove('hidden');
          }
          lastScroll = currentScroll;
          ticking = false;
        });
        ticking = true;
      }
    });

    // Mobile toggle
    if (toggle && links) {
      toggle.addEventListener('click', () => {
        links.classList.toggle('open');
        toggle.classList.toggle('active');
      });

      // Close menu on link click
      links.querySelectorAll('a').forEach((link) => {
        link.addEventListener('click', () => {
          links.classList.remove('open');
          toggle.classList.remove('active');
        });
      });
    }

    // Active link highlighting
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-links a');

    const sectionObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const id = entry.target.id;
            navLinks.forEach((link) => {
              link.classList.toggle(
                'active',
                link.getAttribute('href') === '#' + id
              );
            });
          }
        });
      },
      { threshold: 0.3 }
    );

    sections.forEach((section) => sectionObserver.observe(section));
  }

  // --- Background: Curl Noise Flow Field ---
  // Particles flowing through shifting fluid mediums across the entire viewport.
  // Divergence-free curl noise → no clumping, smooth organic flow.
  function initBackground() {
    const canvas = document.getElementById('bg-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width, height;
    let time = 0;

    // Particle count scales with viewport
    let particles = [];
    const TRAIL_LEN = 30;

    // Flow field resolution
    const FIELD_SCALE = 0.0015;
    const TIME_SCALE  = 0.0003;

    // Medium zones — horizontal bands with different properties
    // Each medium has: viscosity (speed multiplier), turbulence, colour blend
    const MEDIUMS = [
      { color: [232, 168, 53],  speed: 0.9, turb: 1.0, name: 'amber'  },  // amber — steady
      { color: [180, 100, 30],  speed: 1.8, turb: 2.2, name: 'hot'    },  // deep red — fast/turbulent
      { color: [91,  192, 190], speed: 0.5, turb: 0.6, name: 'cyan'   },  // cyan — viscous/slow
      { color: [200, 180, 80],  speed: 1.3, turb: 1.5, name: 'gold'   },  // gold — medium
    ];

    // Simple 3D noise (smooth pseudo-random field)
    // Uses layered sine waves to approximate gradient noise
    function noise3(x, y, z) {
      return (
        Math.sin(x * 1.2 + z * 0.7) * Math.cos(y * 0.9 + z * 1.1) * 0.5 +
        Math.sin(x * 2.5 + y * 1.8 + z * 0.5) * 0.25 +
        Math.sin(x * 0.6 - y * 2.1 + z * 1.6) * Math.cos(x * 1.7 + z * 0.9) * 0.25 +
        Math.sin(x * 3.7 + y * 0.4 - z * 2.3) * 0.15 +
        Math.cos(x * 0.8 + y * 3.2 + z * 1.4) * 0.15
      );
    }

    // Curl of noise field → divergence-free flow (no sinks/sources)
    function curlNoise(x, y, t) {
      const eps = 0.5;
      // ∂noise/∂y for x-component, -∂noise/∂x for y-component
      const dndy = (noise3(x, y + eps, t) - noise3(x, y - eps, t)) / (2 * eps);
      const dndx = (noise3(x + eps, y, t) - noise3(x - eps, y, t)) / (2 * eps);
      return { fx: dndy, fy: -dndx };
    }

    function getMedium(y) {
      // Smooth blend between mediums based on vertical position
      const band = (y / height) * MEDIUMS.length;
      const idx = Math.min(Math.floor(band), MEDIUMS.length - 1);
      const next = Math.min(idx + 1, MEDIUMS.length - 1);
      const frac = band - idx;
      const m1 = MEDIUMS[idx];
      const m2 = MEDIUMS[next];
      // Smooth interpolation
      const t = frac * frac * (3 - 2 * frac);  // smoothstep
      return {
        r: m1.color[0] + (m2.color[0] - m1.color[0]) * t,
        g: m1.color[1] + (m2.color[1] - m1.color[1]) * t,
        b: m1.color[2] + (m2.color[2] - m1.color[2]) * t,
        speed: m1.speed + (m2.speed - m1.speed) * t,
        turb:  m1.turb  + (m2.turb  - m1.turb)  * t,
      };
    }

    function resize() {
      width  = canvas.width  = window.innerWidth;
      height = canvas.height = window.innerHeight;

      // Scale particle count to viewport area
      const targetCount = Math.floor((width * height) / 3500);
      while (particles.length < targetCount) {
        particles.push(makeParticle(true));
      }
      while (particles.length > targetCount) {
        particles.pop();
      }
    }

    function makeParticle(randomAge) {
      return {
        x: Math.random() * width,
        y: Math.random() * height,
        trail: [],
        age: randomAge ? Math.random() * 400 : 0,
        maxAge: 300 + Math.random() * 300,
        size: 0.5 + Math.random() * 1.5,
        layer: Math.random()   // depth layer for parallax
      };
    }

    function draw() {
      ctx.clearRect(0, 0, width, height);

      time++;
      const t = time * TIME_SCALE;

      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];

        // Get flow field at particle position
        const nx = p.x * FIELD_SCALE;
        const ny = p.y * FIELD_SCALE;
        const med = getMedium(p.y);

        // Curl noise with medium-specific turbulence
        const flow = curlNoise(nx * med.turb, ny * med.turb, t);

        // Layer-based parallax: deeper particles move slower
        const layerSpeed = 0.6 + p.layer * 0.8;

        // Move particle
        const speed = med.speed * layerSpeed * 1.2;
        p.x += flow.fx * speed;
        p.y += flow.fy * speed;

        // Store trail point
        p.trail.push({ x: p.x, y: p.y });
        if (p.trail.length > TRAIL_LEN) p.trail.shift();

        p.age++;

        // Lifecycle fade — fade in and out
        let life;
        if (p.age < 30) {
          life = p.age / 30;
        } else if (p.age > p.maxAge - 40) {
          life = (p.maxAge - p.age) / 40;
        } else {
          life = 1;
        }
        life = Math.max(0, Math.min(1, life));

        // Respawn if dead or offscreen
        if (p.age >= p.maxAge || p.x < -20 || p.x > width + 20 || p.y < -20 || p.y > height + 20) {
          particles[i] = makeParticle(false);
          continue;
        }

        // Draw trail segments with fading opacity
        if (p.trail.length > 1) {
          for (let j = 1; j < p.trail.length; j++) {
            const seg = j / p.trail.length;  // 0=old, 1=new
            const segAlpha = life * seg * seg * (0.3 + p.layer * 0.5);
            const segMed = getMedium(p.trail[j].y);
            ctx.beginPath();
            ctx.moveTo(p.trail[j - 1].x, p.trail[j - 1].y);
            ctx.lineTo(p.trail[j].x, p.trail[j].y);
            ctx.strokeStyle = `rgba(${segMed.r | 0},${segMed.g | 0},${segMed.b | 0},${segAlpha})`;
            ctx.lineWidth = p.size * (0.3 + seg * 0.9) * (0.5 + p.layer * 0.8);
            ctx.stroke();
          }
        }

        // Draw glowing head
        const headAlpha = life * (0.5 + p.layer * 0.5);
        const headSize = p.size * (0.8 + p.layer * 0.6);

        // Glow
        ctx.beginPath();
        ctx.arc(p.x, p.y, headSize * 3, 0, 6.2832);
        ctx.fillStyle = `rgba(${med.r | 0},${med.g | 0},${med.b | 0},${headAlpha * 0.1})`;
        ctx.fill();

        // Core
        ctx.beginPath();
        ctx.arc(p.x, p.y, headSize, 0, 6.2832);
        ctx.fillStyle = `rgba(${med.r | 0},${med.g | 0},${med.b | 0},${headAlpha})`;
        ctx.fill();
      }

      requestAnimationFrame(draw);
    }

    resize();
    // Pre-fill canvas so trails don't start from blank
    for (let i = 0; i < 60; i++) {
      time++;
      const t = time * TIME_SCALE;
      for (const p of particles) {
        const nx = p.x * FIELD_SCALE;
        const ny = p.y * FIELD_SCALE;
        const med = getMedium(p.y);
        const flow = curlNoise(nx * med.turb, ny * med.turb, t);
        const layerSpeed = 0.6 + p.layer * 0.8;
        p.x += flow.fx * med.speed * layerSpeed * 1.2;
        p.y += flow.fy * med.speed * layerSpeed * 1.2;
        p.trail.push({ x: p.x, y: p.y });
        if (p.trail.length > TRAIL_LEN) p.trail.shift();
        p.age++;
      }
    }
    draw();

    let resizeTimer;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(resize, 200);
    });
  }

  // --- Smooth scroll for anchor links ---
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener('click', function (e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  }

  // --- Scroll Progress Bar ---
  function initScrollProgress() {
    const bar = document.getElementById('scroll-progress');
    if (!bar) return;

    function update() {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
      bar.style.width = progress + '%';
    }

    window.addEventListener('scroll', update, { passive: true });
    update();
  }

  // --- Hero Name Decode ---
  function initHeroDecode() {
    const el = document.querySelector('.hero-name');
    if (!el) return;
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$%&*!?/\\|<>';
    const text = el.textContent;

    // Start scrambled, decode after fadeUp animation finishes
    setTimeout(() => {
      let iteration = 0;
      const interval = setInterval(() => {
        el.textContent = text
          .split('')
          .map((char, i) => {
            if (char === ' ') return ' ';
            if (i < iteration) return text[i];
            return chars[Math.floor(Math.random() * chars.length)];
          })
          .join('');
        iteration += 0.6;
        if (iteration >= text.length) {
          el.textContent = text;
          clearInterval(interval);
        }
      }, 35);
    }, 1000);
  }

  // --- Card Spotlight + 3D Tilt ---
  function initCardEffects() {
    document.querySelectorAll('.project-card').forEach((card) => {
      // Inject spotlight overlay div
      const spot = document.createElement('div');
      spot.className = 'card-spotlight';
      card.style.position = 'relative';
      card.insertBefore(spot, card.firstChild);

      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const cx = rect.width / 2;
        const cy = rect.height / 2;

        // 3D tilt — max ±4 degrees
        const rotateY = ((x - cx) / cx) * 4;
        const rotateX = ((cy - y) / cy) * 4;
        card.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;

        // Radial spotlight following cursor
        spot.style.background = `radial-gradient(circle 200px at ${x}px ${y}px, rgba(232,168,53,0.08), transparent)`;
      });

      card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(800px) rotateX(0deg) rotateY(0deg)';
        spot.style.background = 'none';
      });
    });
  }

  // --- Terminal Decode on Section Labels ---
  function initTerminalDecode() {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$%&*!?/\\|<>';

    document.querySelectorAll('.section-title').forEach((title) => {
      const original = title.textContent;
      let hasDecoded = false;

      const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && !hasDecoded) {
            hasDecoded = true;
            observer.unobserve(title);
            decodeText(title, original);
          }
        });
      }, { threshold: 0.5 });

      observer.observe(title);
    });

    function decodeText(el, text) {
      let iteration = 0;
      const maxIterations = text.length;

      const interval = setInterval(() => {
        el.textContent = text
          .split('')
          .map((char, i) => {
            if (char === ' ') return ' ';
            if (i < iteration) return text[i];
            return chars[Math.floor(Math.random() * chars.length)];
          })
          .join('');

        iteration += 1 / 2;  // resolve ~2 chars per tick

        if (iteration >= maxIterations) {
          el.textContent = text;
          clearInterval(interval);
        }
      }, 30);
    }
  }

  // --- Magnetic Tags ---
  function initMagneticTags() {
    const tags = document.querySelectorAll('.tag, .skill-tag');
    const RADIUS = 60;    // detection radius in px
    const STRENGTH = 8;   // max repulsion in px

    document.addEventListener('mousemove', (e) => {
      for (const tag of tags) {
        const rect = tag.getBoundingClientRect();
        const tcx = rect.left + rect.width / 2;
        const tcy = rect.top + rect.height / 2;
        const dx = tcx - e.clientX;
        const dy = tcy - e.clientY;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < RADIUS) {
          const force = (1 - dist / RADIUS) * STRENGTH;
          const nx = (dx / dist) * force;
          const ny = (dy / dist) * force;
          tag.style.transform = `translate(${nx}px, ${ny}px)`;
        } else {
          tag.style.transform = '';
        }
      }
    }, { passive: true });
  }

  // --- Init ---
  document.addEventListener('DOMContentLoaded', () => {
    initReveal();
    initNav();
    // initBackground — handled by inline script
    initSmoothScroll();
    initScrollProgress();
    initHeroDecode();
    initCardEffects();
    initTerminalDecode();
    initMagneticTags();
  });
})();
