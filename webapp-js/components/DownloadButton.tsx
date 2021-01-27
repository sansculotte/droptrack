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
  return URL.createObjectURL(blob)
}

export default (props: Props) => {
  
  const [ fileUrl, setFileUrl ] = useState<string>()

  const startDownload = async (ev: React.MouseEvent, url: string) => {
    ev.preventDefault()
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
      style={{width: '30px', height: '30px'}}
      onClick={(ev) => startDownload(ev, props.url)}
      title={props.title}
      className={styles.downloadButton}
    >⬇</button> 
  )
}
