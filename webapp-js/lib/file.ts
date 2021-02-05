import File from 'interfaces/File'

const getExtension = (file: File): string => {
  const parts = file.name.split('.')
  if (parts.length > 1) {
    return parts[parts.length - 1].toLowerCase()
  }
  return ''
}

const sortCompare = (field: string = 'name') => (a: File, b: File) => {
  if (a[field] < b[field]) {
    return -1
  }
  if (a[field] > b[field]) {
    return 1
  }
  return 0
}

export { getExtension, sortCompare }
