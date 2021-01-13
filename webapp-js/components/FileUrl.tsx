import http from 'lib/http'
import * as React from 'react'
import { useState } from 'react'

import ApiResponse from 'interfaces/ApiResponse' 
import Task from 'interfaces/Task'

interface Props {
  flashMessage: (message: string) => void 
  addTask: (task: Task) => void
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
      const { message, task } = response.data
      props.addTask(task)
      props.flashMessage(message)
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
