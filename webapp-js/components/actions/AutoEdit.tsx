import React, { useEffect, useState } from 'react'

import http from 'lib/http'

import { ErrorMessage } from '../ErrorMessage'
import { MultiFileChooser } from '../MultiFileChooser'
import Process from '../Process'

import { TaskResult } from './TaskResult'

import { AutoEditParameters } from 'interfaces/Action'
import ApiData from 'interfaces/ApiData'
import File from 'interfaces/File'
import Task from 'interfaces/Task'


interface Props {
  parameters: AutoEditParameters
  addTask: (task: Task) => void
  tasks: Map<string, Task>
}


const AutoEdit = (props: Props) => {

  const [ files, setFiles ] = useState(props.parameters.files)
  const [ duration, setDuration ] = useState(`${props.parameters.duration}`)
  const [ numsegs, setNumsegs ] = useState(`${props.parameters.numsegs}`)
  const [ assemblyMode, setAssemblyMode ] = useState(props.parameters.assembly_mode)
  const [ errors, setErrors ] = useState<Array<string>>([])
  const [ taskId, setTaskId ] = useState<string|null>(null)
  const [ task, setTask ] = useState<Task|undefined>()

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

  const handleDurationChange = (ev: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(ev.currentTarget.value, 10)
    if (!isNaN(value)) {
      setDuration(`${value}`)
    }
    setErrors([])
  }

  const handleAssemblyModeChange = (ev: React.ChangeEvent<HTMLSelectElement>) => {
    const assemblyMode = ev.currentTarget.value as AutoEditParameters['assembly_mode']
    setAssemblyMode(assemblyMode)
  }

  const handleNumsegsChange = (ev: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(ev.currentTarget.value, 10)
    if (!isNaN(value)) {
      setNumsegs(`${value}`)
    }
    setErrors([])
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
    const url = '/api/autoedit' // '/actions/autoedit'
    const errors = []
    const parameters = {
      files,
      duration: parseInt(duration, 10),
      numsegs: parseInt(numsegs, 10),
      assembly_mode: assemblyMode
    }
    if (files.length === 0) {
      errors.push('Please Add an Input File')
    }
    if (parameters.duration > 500) {
      errors.push('Please keep duration under 500')
    }
    if (parameters.duration < 0) {
      errors.push('Duration must be positive')
    }
    if (errors.length > 0) {
      setErrors(errors)
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
      <label>Duration</label>
      <input
        placeholder="duration: 0-99"
        type="text"
        name="duration"
        value={duration}
        onChange={handleDurationChange}
      />
      <label>Assembly Mode</label>
      <select
        placeholder="assemble mode"
        value={assemblyMode}
        onChange={handleAssemblyModeChange}
      >
        <option value="random">random</option>
        <option value="sequential">sequential</option>
      </select>
      <label>Number of Segements</label>
      <input
        placeholder="numsegs: 0-???"
        type="text"
        name="numsegs"
        value={numsegs}
        onChange={handleNumsegsChange}
      />
      {!task
        ? <input type="submit" value="start" />
        : task.status === 'done'
          ? <><TaskResult url={task.url} /><a onClick={restart}>Restart</a></>
          : <Process />
      }
    </form>
  )
}

export { AutoEdit }
