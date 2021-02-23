import * as React from 'react'

import http from 'lib/http'
import './FileDrop.css'
import Dropzone from 'react-dropzone-uploader'

import UploadSymbol from 'components/UploadSymbol'

interface Props {
  accept: string
  onUploadFinished: (message: string) => void
}

type Status = 'done' | 'uploading' | 'error_upload' | 'headers_received' | 'aborted'

export default (props: Props) => {

  const handleChangeStatus = ({ meta }: any, status: Status) => {
    if (status === 'done') {
      props.onUploadFinished(`${meta.name} uploaded`)
    }
  }
    
  return (
    <Dropzone
      getUploadParams={() => http.uploadParams('/files')}
      onChangeStatus={handleChangeStatus}
      accept={props.accept}
      inputContent={UploadSymbol}
      submitButtonContent={null}
      styles={{
        dropzone: {
          minHeight: 500,
          overflow: 'auto'
        }
      }}
    />
  )
}
