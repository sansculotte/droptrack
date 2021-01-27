import File from './File'

export default interface Task {
  uuid: string
  name: string
  url: string
  result_files: Array<File>
  status: 'done' | 'processing'
}
