import * as React from 'react'
import { useEffect, useState } from 'react'
import http from 'lib/http'

import * as styles from './DownloadButton.scss'


interface Props {
  url: string
  name: string
  title?: string
}

const fetchBlob = async (url: string) => {
  const blob = await http.getBlob(url)
//    const file = new File([blob], name, {type: blob.type, lastModified: Date.now()});
  return URL.createObjectURL(blob)
}

export default (props: Props) => {
  
  const [ fileUrl, setFileUrl ] = useState<string>()

  const startDownload = async (url: string) => {
    try {
        const fileUrl = await fetchBlob(url)
        setFileUrl(fileUrl)
    }
    catch(e) {
        console.log(e)
    }
  }

  useEffect(() => {
    if (fileUrl) {
      let link = document.createElement('a')
      link.download = props.name
      link.href = fileUrl
      link.click()
    }
    return () => {
      if (fileUrl) {
        URL.revokeObjectURL(fileUrl)
      }
    }
  }, [fileUrl])

  return (
    <button
      onClick={() => startDownload(props.url)}
      title={props.title}
      className={styles.downloadButton}
    >⬇</button> 
  )
}
