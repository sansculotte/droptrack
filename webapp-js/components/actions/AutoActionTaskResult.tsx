import React, { useEffect, useState } from 'react'

import http from 'lib/http'

import DownloadButton from '../DownloadButton'

import Task from 'interfaces/Task'


interface ResultFile {
  format: string
  filename: string
}


const AutoActionTaskResult = (props: {url: Task['url']}) => {

  const [ resultFiles, setResultFiles ] = useState<Array<ResultFile>>([])
    
  useEffect(
    () => {
      http.get(props.url).then(
        data => setResultFiles(data.data.output_files)
    )},
    []
  )

  return (
    <ul>
    {
      resultFiles.map(f =>
        <li key={f.filename}>
          <dt>{f.filename}</dt>
          <dd>
            <DownloadButton
              url={`/files/${f.filename}`}
              name={f.format}
              title={f.filename}
            />
          </dd>
        </li>
      )
    }
    </ul>
  )
}

export { AutoActionTaskResult }
