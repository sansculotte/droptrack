declare var API_URL: string
import 'whatwg-fetch'

interface ApiData {
  [key: string]: string | number | ApiData
}

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE'

type CorsMethod = 'navigate' | 'same-origin' | 'no-cors' | 'cors' | undefined

const apiUrl = (path: string) => {
  return API_URL + path
}

async function request(
  url: string,
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
  const response = await fetch(url, { body, method, headers, mode, credentials })
  if (response.ok) {
    const json = await response.json()
    return json
  }
  return await response.json()
}

async function get(path: string, params?:Array<[string, string]>) {
  const url = new URL(apiUrl(path))
  if (params) {
    url.search = new URLSearchParams(params).toString()
  }
  return request(url.toString(), 'GET')
}

async function put(path: string, data: ApiData) {
  return request(apiUrl(path), 'PUT', JSON.stringify(data))
}

async function post(path: string, data: ApiData) {
  return request(apiUrl(path), 'POST', JSON.stringify(data))
}

async function upload(path: string, file: any, fieldname: string='file') {
  // do not set content-type header
  const headers = new Headers({
    'X-Authentication': window.localStorage.getItem('apiKey') || ''
  })
  const body = new FormData()
  body.append(fieldname, file)
  return request(apiUrl(path), 'POST', body, headers)
}

export default {
  get,
  put,
  post,
  upload
}
