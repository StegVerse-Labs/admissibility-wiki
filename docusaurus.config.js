// @ts-check

const config = {
  title: 'Admissibility Wiki',
  tagline: 'Transition governance, commit-time authority, and receipt-bound execution.',
  favicon: 'img/favicon.svg',

  url: 'https://stegverse-labs.github.io',
  baseUrl: '/admissibility-wiki/',

  organizationName: 'StegVerse-Labs',
  projectName: 'admissibility-wiki',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.js',
          routeBasePath: '/',
          editUrl: 'https://github.com/StegVerse-Labs/admissibility-wiki/edit/main/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      },
    ],
  ],

  themeConfig: {
    navbar: {
      title: 'Admissibility Wiki',
      items: [
        {to: '/', label: 'Start', position: 'left'},
        {to: '/glossary/admissibility', label: 'Glossary', position: 'left'},
        {to: '/proof-path/minimal-public-proof-path', label: 'Proof Path', position: 'left'},
        {to: '/governance/governed-llm-activation-map', label: 'Governed LLM', position: 'left'},
        {
          href: 'https://github.com/StegVerse-Labs/admissibility-wiki',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Core',
          items: [
            {label: 'Admissibility', to: '/glossary/admissibility'},
            {label: 'Transition Table', to: '/stegverse/transition-table'},
            {label: 'Minimal Public Proof Path', to: '/proof-path/minimal-public-proof-path'},
            {label: 'Governed LLM', to: '/governance/governed-llm-activation-map'},
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} StegVerse-Labs.`,
    },
  },
};

export default config;
