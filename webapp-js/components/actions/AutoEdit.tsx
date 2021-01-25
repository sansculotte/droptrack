import React, { useState } from 'react'

import http from 'lib/http'

import { MultiFileChooser } from '../MultiFileChooser'

import { AutoEditParameters } from 'interfaces/Action'
import ApiData from 'interfaces/ApiData'
import File from 'interfaces/File'
import Task from 'interfaces/Task'


interface Props {
  parameters: AutoEditParameters
  addTask: (task: Task) => void
}


const AutoEdit = (props: Props) => {

  const [ parameters, setParameters ] = useState(props.parameters)

  const handleDurationChange = (ev: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(ev.currentTarget.value, 10)
    if (!isNaN(value)) {
      parameters.duration = value
    }
    setParameters(parameters)
  }

  const handleAssemblyModeChange = (ev: React.ChangeEvent<HTMLSelectElement>) => {
    parameters.assembly_mode = ev.currentTarget.value as AutoEditParameters['assembly_mode']
    setParameters(parameters)
  }

  const handleNumsegsChange = (ev: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(ev.currentTarget.value, 10)
    if (!isNaN(value)) {
      parameters.numsegs = value
    }
    setParameters(parameters)
  }

  const setFiles = (files: Array<File>) => {
    parameters.files = files
    setParameters(parameters)
  }

  const handleSubmit = async (ev: React.FormEvent<HTMLFormElement>) => {
    ev.preventDefault()
    const url = '/api/autoedit' // '/actions/autoedit'
    console.log(parameters)
    const response = await http.post(url, parameters as ApiData)
    props.addTask(response.data)
  }

  return (
    <form onSubmit={handleSubmit}>
      <MultiFileChooser setFiles={setFiles} selected={parameters.files} />
      <input
        placeholder="duration: 0-99999"
        type="text"
        name="duration"
        value={parameters.duration}
        onChange={handleDurationChange}
      />
      <select
        placeholder="assemble mode"
        value={parameters.assembly_mode}
        onChange={handleAssemblyModeChange}
      >
        <option value="random">random</option>
        <option value="sequential">sequential</option>
      </select>
      <input
        placeholder="numsegs: 0-???"
        type="text"
        name="numsegs"
        value={parameters.numsegs}
        onChange={handleNumsegsChange}
      />
      <input type="submit" value="start" />
    </form>
  )
}

export { AutoEdit }
