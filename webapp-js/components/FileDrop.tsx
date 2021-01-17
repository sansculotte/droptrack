import * as React from 'react'
import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'

import UploadSymbol from 'components/UploadSymbol'

import * as styles from './FileDrop.scss'


interface Props {
  onDrop: (args: Array<any>) => void
  accept: string
}

export default (props: Props) => {
  const onDrop = useCallback(props.onDrop, [])
  const {
    getRootProps,
    getInputProps,
    isDragActive
  } = useDropzone({onDrop, accept: props.accept})

  return (
    <div className={styles.fileDrop} {...getRootProps()}>
      <input {...getInputProps()} />
      {
        isDragActive
          ? <UploadSymbol />
          : <UploadSymbol />
      }
    </div>
  )
}
