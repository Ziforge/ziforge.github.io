# ziforge.github.io

Portfolio site for Ziforge — FPGA Audio Engineer, DSP Researcher, Instrument Designer.

## Structure

```
ziforge.github.io/
├── index.html      # Single-page site — all content here
├── style.css       # All styles — dark theme, responsive
├── main.js         # Scroll animations, nav, background canvas
├── images/         # Project screenshots & diagrams (add your own)
└── README.md       # This file
```

## Deployment

This site is designed for GitHub Pages deployment from the **root of the `main` branch**.

1. Create a repo named `ziforge.github.io` on GitHub
2. Push this directory to the repo
3. GitHub Pages will automatically serve `index.html` at `https://ziforge.github.io`

## Updating Content

### Projects
All project cards are in the `<!-- PROJECTS -->` section of `index.html`. Each project is an `<article class="project-card">` block. To add/edit:

- Copy an existing `<article class="project-card">` block
- Update title, status badge, description, and tags
- Status badge classes: `status-active`, `status-completed`, `status-dev`, `status-research`, `status-pro`

### Images
To add project images, replace the placeholder `<div>` with an `<img>`:

```html
<!-- Replace this: -->
<div class="project-image">screenshot / diagram placeholder</div>

<!-- With this: -->
<div class="project-image">
  <img src="images/your-image.jpg" alt="Description">
</div>
```

### Contact Links
Update the `href` values in the contact section:
- Email: `mailto:your@email.com`
- LinkedIn: `https://linkedin.com/in/yourprofile`
- GitHub: `https://github.com/ziforge`

### Publications
When publications are ready, uncomment and fill in the template in the publications section.

### Skills
Edit the skill tags in the `<!-- SKILLS -->` section. Each category is a `.skill-group` block.

## Design

- **Theme:** Dark (#0a0a0a background, warm amber #e8a835 accent)
- **Fonts:** JetBrains Mono (headings/code), Inter (body)
- **Background:** Subtle animated node network (patch-cable aesthetic)
- **Animations:** Fade-in on scroll, staggered children
- **No frameworks** — pure HTML/CSS/JS, fast loading
