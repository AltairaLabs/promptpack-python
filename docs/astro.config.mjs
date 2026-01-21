// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightThemeGalaxy from 'starlight-theme-galaxy';

export default defineConfig({
  site: 'https://altairalabs.github.io',
  base: '/promptpack-python',
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
      ],
    }),
  ],
});
