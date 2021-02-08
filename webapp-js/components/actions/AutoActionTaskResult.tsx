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

  // ellipsis in the middle think
  const limitChars = (str: string, length=30) => {
    const head = 7
    if (str.length > length) {
      return str.substr(0, length - head) + '…' + str.substr(-head)
    }
    return str
  }

  return (
    <ul>
    {
      resultFiles.map(f =>
        <li key={f.filename}>
          <dt title={f.filename}>{limitChars(f.filename)}</dt>
          <dd>
            <DownloadButton
              url={`/files/${f.filename}`}
              name={f.filename}
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
