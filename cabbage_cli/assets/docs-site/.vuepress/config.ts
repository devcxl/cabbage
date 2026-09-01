import { defineUserConfig } from 'vuepress'
import { viteBundler } from '@vuepress/bundler-vite'
import { defaultTheme } from '@vuepress/theme-default'
import { markdownChartPlugin } from '@vuepress/plugin-markdown-chart'

const base = (process.env.BASE_URL || (process.env.GITHUB_REPOSITORY ? `/${process.env.GITHUB_REPOSITORY.split('/')[1]}/` : '/')) as `/${string}/` | '/'

export default defineUserConfig({
  base,
  lang: 'zh-CN',
  title: 'Project Documentation',
  description: 'Project documentation managed by Cabbage',
  bundler: viteBundler(),
  theme: defaultTheme({
    navbar: [
      { text: '首页', link: '/' },
      { text: '产品需求', link: '/01-product/' },
      { text: '系统架构', link: '/03-architecture/' },
      { text: 'API 接口', link: '/05-api/' },
      { text: '测试计划', link: '/08-testing/' },
    ],
    sidebar: 'heading',
  }),
  plugins: [markdownChartPlugin({ mermaid: true })],
})
