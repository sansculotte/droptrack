import http from 'lib/http'
import * as React from 'react'
import { useState } from 'react'

import ApiResponse from 'interfaces/ApiResponse' 

interface Props {
  flashMessage: (message: string) => void 
}

export default (props: Props) => {
  const [ url, setUrl ] = useState('')

  const handleChangeUrl = (ev: React.FormEvent<HTMLInputElement>) => {
    const url = ev.currentTarget.value
    setUrl(url)
  }

  const handleDropUrl = (ev: React.MouseEvent) => {
    ev.preventDefault()
    http.post('/url', {url}).then((response: ApiResponse) => {
      console.log(response)
      props.flashMessage(response.message)
    }).catch(console.error)
  }

  return (
    <>
      <input
        name="url"
        type="url"
        placeholder="soundfile url"
        onChange={handleChangeUrl}
        value={url}
      />
      <input type="button" onClick={handleDropUrl} value="Drop" />
    </>
  )
}
