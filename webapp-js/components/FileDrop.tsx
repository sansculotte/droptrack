import * as React from 'react'
import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'

import UploadSymbol from 'components/UploadSymbol'


interface Props {
  onDrop: (args: Array<any>) => void
}

const FileDrop = (props: Props) => {
  const onDrop = useCallback(props.onDrop, [])
  const {
    getRootProps,
    getInputProps,
    isDragActive
  } = useDropzone({onDrop, accept: 'audio/*'})

  return (
    <div {...getRootProps()}>
      <input {...getInputProps()} />
      {
        isDragActive
          ? <UploadSymbol />
          : <UploadSymbol />
      }
    </div>
  )
}

export default FileDrop
