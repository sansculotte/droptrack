import React, { useEffect, useState } from 'react'

import http from 'lib/http'

import { ErrorMessage } from '../ErrorMessage'
import { MultiFileChooser } from '../MultiFileChooser'
import Process from '../Process'

import { AutoActionTaskResult } from './AutoActionTaskResult'

import { AutoMasterParameters } from 'interfaces/Action'
import ApiData from 'interfaces/ApiData'
import File from 'interfaces/File'
import Task from 'interfaces/Task'


interface Props {
  parameters: AutoMasterParameters
  addTask: (task: Task) => void
  tasks: Map<string, Task>
}


const AutoMaster = (props: Props) => {

  const [ files, setFiles ] = useState(props.parameters.files)
  const [ bitdepth, setBitdepth ] = useState(`${props.parameters.bitdepth}`)
  // const [ duration, setDuration ] = useState(`${props.parameters.duration}`)
  // const [ numsegs, setNumsegs ] = useState(`${props.parameters.numsegs}`)
  // const [ assemblyMode, setAssemblyMode ] = useState(props.parameters.assembly_mode)
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

  // const handleDurationChange = (ev: React.ChangeEvent<HTMLInputElement>) => {
  //   const value = parseInt(ev.currentTarget.value, 10)
  //   if (!isNaN(value)) {
  //     setDuration(`${value}`)
  //   }
  //   setErrors([])
  // }

  // const handleAssemblyModeChange = (ev: React.ChangeEvent<HTMLSelectElement>) => {
  //   const assemblyMode = ev.currentTarget.value as AutoMasterParameters['assembly_mode']
  //   setAssemblyMode(assemblyMode)
  // }

  const handleBitdepthChange = (ev: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(ev.currentTarget.value, 10)
    if (!isNaN(value)) {
      setBitdepth(`${value}`)
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
    const url = '/api/automaster' // '/actions/automaster'
    const errors = []
    const parameters = {
      files,
      // duration: parseInt(duration, 10),
      bitdepth: parseInt(bitdepth, 10),
      // assembly_mode: assemblyMode
    }
    if (files.length === 0) {
      errors.push('Please Add an Input File')
    }
    if (parameters.bitdepth == 16 || parameters.bitdepth == 24) {
    }
    else {
      errors.push('Missing bitdepth set to default 16')
      parameters.bitdepth = 16
    }
    // if (parameters.duration < 0) {
    //   errors.push('Duration must be positive')
    // }
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
      <label>Processing bit depth</label>
      <input
        placeholder="bitdepth: 16/24"
        type="text"
        name="bitdepth"
        value={bitdepth}
        onChange={handleBitdepthChange}
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

export { AutoMaster }
