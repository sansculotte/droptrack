export default interface Task {
  uuid: string
  name: string
  url: string
  status: 'done' | 'processing'
}
