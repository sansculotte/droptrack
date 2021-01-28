declare var API_URL: string
import 'whatwg-fetch'

import ApiData from 'interfaces/ApiData'

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE'

type CorsMethod = 'navigate' | 'same-origin' | 'no-cors' | 'cors' | undefined

const apiUrl = (path: string) => {
  const url = new URL(API_URL)
  url.pathname = path
  return url
}

async function request(
  url: URL,
  method: HttpMethod = 'GET',
  body?: any,
  headers?: Headers,
  mode: CorsMethod = 'cors',
) {
  headers = headers || new Headers({
    'Content-Type': 'application/json',
    'X-Authentication': window.localStorage.getItem('apiKey') || ''
  })
  const credentials = 'same-origin'
  const response = await fetch(url.toString(), { body, method, headers, mode, credentials })
  return response
}

async function get(path: string, params?:Array<[string, string]>) {
  const url = apiUrl(path)
  if (params) {
    url.search = new URLSearchParams(params).toString()
  }
  const response = await request(url, 'GET')
  return await response.json()
}

async function put(path: string, data: ApiData) {
  const response = await request(apiUrl(path), 'PUT', JSON.stringify(data))
  return await response.json()
}

async function post(path: string, data: ApiData) {
  const response = await request(apiUrl(path), 'POST', JSON.stringify(data))
  return await response.json()
}

async function upload(path: string, file: any, fieldname: string='file') {
  // do not set content-type header
  const headers = new Headers({
    'X-Authentication': window.localStorage.getItem('apiKey') || ''
  })
  const body = new FormData()
  body.append(fieldname, file)
  const response = await request(apiUrl(path), 'POST', body, headers)
  return await response.json()
}

async function poll(path: string) {
  const response = await request(apiUrl(path), 'GET')
  const data = await response.json()
  if (response.status === 202) {
    data.status = 'processing'
    data.url = response.headers.get('Location')
  }
  else if (response.status === 201) {
    data.status = 'done'
    data.url = response.headers.get('Location')
  }
  else if (response.status === 200) {
    data.status = 'done'
  }
  else {
    data.status = 'error'
  }
  return data
}

async function getBlob(path: string, params?:Array<[string, string]>) {
  const url = apiUrl(path)
  if (params) {
    url.search = new URLSearchParams(params).toString()
  }
  const response = await request(url, 'GET')
  return await response.blob()
}

export default {
  get,
  getBlob,
  put,
  poll,
  post,
  upload,
}
