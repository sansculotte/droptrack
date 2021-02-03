import http from 'lib/http'
import { getExtension } from 'lib/file'
import React, { useEffect, useState } from 'react'

import File from 'interfaces/File'

import * as styles from './FileChooser.scss'


interface Props {
  allowedExtensions?: Array<string>
  exclude: Array<File>
  onSelect: (file: File) => void
}

const FileChooser = (props: Props) => {

  const [ availableFiles, setAvailableFiles ] = useState<Array<File>>([])

  const fileAllowed = (file: File) => {
    return props.allowedExtensions === undefined
      || props.allowedExtensions.indexOf(getExtension(file)) > -1
  }

  const loadFileList = async () => {
    const response = await http.get('/files')
    if (response.status === 'ok') {
      const { files } = response.data as {files: Array<File>}
      setAvailableFiles(
        files
          .filter(fileAllowed)
          .filter(f => props.exclude.find(x => x.name === f.name) === undefined)
      )
    }
  }

  const select = (index: number) =>
    props.onSelect(availableFiles[index])

  useEffect(() => {
    loadFileList()
  }, [])

  return (
    <div className={styles.fileChooser}>
      <ul>
        {availableFiles.map((file, index) =>
          <li key={index} onClick={() => select(index)}>{file.name}</li>
        )}
      </ul>
    </div>
  )
}

export { FileChooser }
