import React, { useEffect, useState } from 'react'
import DeleteButton from './DeleteButton'
import { FileChooser } from './FileChooser'

import File from 'interfaces/File'

import * as styles from './MultiFileChooser.scss'


interface Props {
  selected?: Array<File>
  setFiles: (files: Array<File>) => void
}


const MultiFileChooser = (props: Props) => {

  const [ selectedFiles, setSelectedFiles ] = useState(props.selected || [])
  const [ showFileChooser, setShowFileChooser ] = useState(false)

  const addFile = (file: File) => {
    setSelectedFiles(selectedFiles.concat(file))
    setShowFileChooser(false)
  }

  const removeFile = (file: File) =>
    setSelectedFiles(selectedFiles.filter(f => f !== file))

  const toogleFileChooser = () => setShowFileChooser(!showFileChooser)

  useEffect(() => props.setFiles(selectedFiles), [selectedFiles])

  return (
    <div className={styles.multiFileChooser}>
      <ul>
        {selectedFiles.map(f =>
          <li key={f.name}>
            <dt>{f.name}</dt>
            <dd><DeleteButton onClick={() => removeFile(f)} /></dd>
          </li>
        )}
        </ul>
      {showFileChooser
        ? <FileChooser exclude={selectedFiles} onSelect={addFile} />
        : <button onClick={toogleFileChooser}>Add File</button>
      }
    </div>
  )
}

export { MultiFileChooser }