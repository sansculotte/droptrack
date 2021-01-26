import File from './File'

interface ApiData {
  [key: string]: string | number | Array<string> | ApiData | Array<File>
}

export default ApiData
