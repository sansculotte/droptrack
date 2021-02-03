import File from 'interfaces/File'

const getExtension = (file: File): string => {
  const parts = file.name.split('.')
  if (parts.length > 1) {
    return parts[parts.length - 1].toLowerCase()
  }
  return ''
}

export { getExtension }
