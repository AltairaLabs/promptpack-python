// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightThemeGalaxy from 'starlight-theme-galaxy';

// Declared once: `site`/`base` below need them, and so does every absolute URL
// in the link-preview tags, which a scraper fetches with no page to resolve
// against. The base path is part of that URL — without it the image 404s.
const SITE = 'https://altairalabs.github.io';
const BASE = '/promptpack-python';
const OG_IMAGE = `${SITE}${BASE}/og-image.png`;
const OG_ALT = 'PromptPack Python — parse and use PromptPacks in your Python applications';

export default defineConfig({
  site: SITE,
  base: BASE,
  integrations: [
    starlight({
      title: 'PromptPack Python',
      logo: {
        src: './public/logo.svg',
        alt: 'PromptPack Logo',
      },
      plugins: [starlightThemeGalaxy()],
      customCss: ['./src/styles/custom.css'],
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/AltairaLabs/promptpack-python' },
      ],
      sidebar: [
        { label: 'Getting Started', autogenerate: { directory: 'getting-started' } },
        { label: 'Packages', autogenerate: { directory: 'packages' } },
        { label: 'Examples', autogenerate: { directory: 'examples' } },
        { label: 'API Reference', autogenerate: { directory: 'api' } },
        { label: 'Contributors', autogenerate: { directory: 'contributors' } },
      ],
      head: [
        {
          tag: 'script',
          attrs: {
            type: 'module',
            src: '/mermaid-init.js',
          },
        },
        // The link-preview card. Starlight already emits og:title,
        // og:description and twitter:card per page; what it has no opinion
        // about is the IMAGE, and a summary_large_image card with no image is
        // what Slack renders as a bare line of text.
        //
        // A PNG, not SVG: Slack, LinkedIn and X all decline to rasterise SVG.
        // Absolute, because a scraper resolves this URL with no page to be
        // relative to.
        //
        // Regenerate from src/assets/og-card.svg:
        //   rsvg-convert -w 1200 -h 630 -o public/og-image.png src/assets/og-card.svg
        { tag: 'meta', attrs: { property: 'og:image', content: OG_IMAGE } },
        { tag: 'meta', attrs: { property: 'og:image:width', content: '1200' } },
        { tag: 'meta', attrs: { property: 'og:image:height', content: '630' } },
        { tag: 'meta', attrs: { property: 'og:image:alt', content: OG_ALT } },
        { tag: 'meta', attrs: { name: 'twitter:image', content: OG_IMAGE } },
      ],
    }),
  ],
});
