import React, { useEffect, useState } from 'react'

import http from 'lib/http'

import { AutoActionTaskResult } from './AutoActionTaskResult'
import { ErrorMessage } from '../ErrorMessage'
import { MultiFileChooser } from '../MultiFileChooser'
import Process from '../Process'

import { AutoCover } from 'interfaces/Action'
import ApiData from 'interfaces/ApiData'
import File from 'interfaces/File'
import Task from 'interfaces/Task'


interface Props {
  parameters: AutoCover['parameters']
  addTask: (task: Task) => void
  tasks: Map<string, Task>
}


const AutoCover = (props: Props) => {

  const [ files, setFiles ] = useState(props.parameters.files)
  const [ errors, setErrors ] = useState<Array<string>>([])
  const [ task, setTask ] = useState<Task|undefined>()
  const [ taskId, setTaskId ] = useState<string|null>(null)

  useEffect(
    () => {
      setTask(taskId ? props.tasks.get(taskId) : undefined)
    },
    [taskId]
  )

  useEffect(
    () => {
      if (taskId && task) {
        const t = props.tasks.get(taskId)
        if (t && t.status !== task.status) {
          setTask(t)
        }
      }
    }
  )

  const restart = () => {
    setTask(undefined)
    setTaskId(null)
  }

  const handleFilesChange = (files: Array<File>) => {
    setFiles(files)
    setErrors([])
  }

  const handleSubmit = async (ev: React.FormEvent<HTMLFormElement>) => {
    if (task && task.status === 'done') {
      return
    }

    ev.preventDefault()
    const url = '/api/autocover' // '/actions/autocover'
    const errors = []

    const parameters = { files }

    if (files.length === 0) {
      errors.push('Please Add an Input File')
    }
    else {
      const response = await http.post(url, parameters as ApiData)
      const t = response.data
      setTaskId(t.uuid)
      props.addTask(t)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {errors.length > 0 && <ErrorMessage errors={errors} />}
      <MultiFileChooser
        setFiles={handleFilesChange}
        selected={files}
        allowedExtensions={['wav', 'mp3', 'ogg', 'flac']}
      />
      {!task
        ? <input type="submit" value="start" />
        : task.status === 'done'
          ? <>
            <AutoActionTaskResult url={task.url} />
            <a onClick={restart}>Restart</a>
            </>
          : <Process />
      }
    </form> 
  )
}

export { AutoCover }
