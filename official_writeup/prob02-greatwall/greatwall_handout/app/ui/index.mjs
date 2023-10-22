// @ts-check
import { fileURLToPath } from 'node:url'
import fastify from 'fastify'
import fastifyHttpProxy from '@fastify/http-proxy'
import fastifyStatic from '@fastify/static'
import puppeteer from 'puppeteer-core'
import { setTimeout } from 'node:timers/promises'
import { readFileSync, writeFileSync } from 'node:fs'

const flag = readFileSync('/flag_easy', 'utf8')
writeFileSync('/flag_easy', 'flag{no_flag_here}')

const server = fastify({ logger: true })
server.register(fastifyHttpProxy, {
  prefix: '/websockify',
  websocket: true,
  upstream: 'http://localhost:8080'
})
server.register(fastifyStatic, {
  root: fileURLToPath(new URL('./static', import.meta.url))
})
server.register(fastifyStatic, {
  root: '/usr/share/novnc',
  prefix: '/novnc',
  decorateReply: false
})

/**
 * @param {string} url
 */
async function checkUrl(url, test = false) {
  const u = new URL(url)
  if (!['http:', 'https:'].includes(u.protocol)) {
    throw new Error('Invalid URL')
  }
  if (test) {
    await fetch(url)
  }
  return url
}

async function getCfw() {
  const browser = await puppeteer.connect({
    browserURL: 'http://localhost:9229'
  })
  return browser
}

server.get('/api/visit', async (req, rep) => {
  // @ts-ignore
  const url = req.query.url
  await checkUrl(url)
  if (!new URL(url).hostname.endsWith('.pku.edu.cn')) {
    throw new Error('Only PKU website is allowed!')
  }
  console.log(`Visit ${url}`)

  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/google-chrome-stable',
    args: ['--proxy-server=socks://127.0.0.1:7890', '--no-sandbox']
  })
  const ctx = await browser.createIncognitoBrowserContext()
  const page = await ctx.newPage()
  await page.goto(url.toString())
  if (new URL(url).hostname === 'ys.pku.edu.cn') {
    // Genshin School of Peking University uses Primogem to pay tuition
    await page.type('#primogem_code[type=password]', flag)
  }
  await setTimeout(5000)
  const screenshot = await page.screenshot({ encoding: 'base64' })
  await browser.close()
  return screenshot
})

server.get('/api/general', async (req, rep) => {
  const browser = await getCfw()
  const [page] = await browser.pages()
  await page.click('#app > div > main > div.left-side > div > div.menu-light > li:nth-child(1)')
  browser.disconnect()
  return 0
})

server.get('/api/proxies', async (req, rep) => {
  const browser = await getCfw()
  const [page] = await browser.pages()
  await page.click('#app > div > main > div.left-side > div > div.menu-light > li:nth-child(2)')
  browser.disconnect()
  return 0
})

server.get('/api/profiles', async (req, rep) => {
  const browser = await getCfw()
  const [page] = await browser.pages()
  await page.click('#app > div > main > div.left-side > div > div.menu-light > li:nth-child(3)')
  browser.disconnect()
  return 0
})

server.get('/api/import', async (req, rep) => {
  // @ts-ignore
  const url = req.query.url
  await checkUrl(url)
  console.log(`Import ${url}`)

  const browser = await getCfw()
  const [page] = await browser.pages()
  await page.click('#app > div > main > div.left-side > div > div.menu-light > li:nth-child(3)')
  const input = await page.$(
    '#main-server-view > div > div.card-light.remote-view > div.input-container > input[type=text]'
  )
  await input?.click({ clickCount: 3 })
  await input?.type(url)
  await page.click(
    '#main-server-view > div > div.card-light.remote-view > div.btns-container > div.confirm.confirm-left'
  )
  browser.disconnect()
  return 0
})

server.listen({
  host: '0.0.0.0',
  port: 3030
})
