import http from 'lib/http'
import React, { useEffect, useState } from 'react'

import File from 'interfaces/File'

import * as styles from './FileChooser.scss'


interface Props {
  exclude: Array<File>
  onSelect: (file: File) => void
}

const FileChooser = (props: Props) => {

  const [ availableFiles, setAvailableFiles ] = useState<Array<File>>([])

  const loadFileList = async () => {
    const response = await http.get('/files')
    if (response.status === 'ok') {
      const { files } = response.data
      setAvailableFiles(
        files.filter(f => props.exclude.find(x => x.name === f.name) === undefined)
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
