import { defineUserConfig } from 'vuepress'
import { viteBundler } from '@vuepress/bundler-vite'
import { defaultTheme } from '@vuepress/theme-default'
import { markdownChartPlugin } from '@vuepress/plugin-markdown-chart'

const base = (process.env.BASE_URL || (process.env.GITHUB_REPOSITORY ? `/${process.env.GITHUB_REPOSITORY.split('/')[1]}/` : '/')) as `/${string}/` | '/'

export default defineUserConfig({
  base,
  lang: 'zh-CN',
  title: 'Cabbage Documentation',
  description: 'Project documentation managed by Cabbage',
  bundler: viteBundler(),
  theme: defaultTheme({
    navbar: [
      { text: '首页', link: '/' },
      { text: '概览', link: '/00-overview/' },
      { text: '产品', link: '/01-product/' },
      { text: '架构', link: '/03-architecture/' },
      { text: '测试', link: '/08-testing/' },
      { text: 'CI/CD', link: '/11-ci-cd/' },
      { text: '发布', link: '/12-release/' },
    ],
    sidebar: 'heading',
  }),
  plugins: [markdownChartPlugin({ mermaid: true })],
})
