import React, { useState } from 'react'

import http from 'lib/http'

import { MultiFileChooser } from '../MultiFileChooser'

import { AutoEditParameters } from 'interfaces/Action'
import ApiData from 'interfaces/ApiData'
import Task from 'interfaces/Task'


interface Props {
  parameters: AutoEditParameters
  addTask: (task: Task) => void
}


const AutoEdit = (props: Props) => {

  const [ files, setFiles ] = useState(props.parameters.files)
  const [ duration, setDuration ] = useState(`${props.parameters.duration}`)
  const [ numsegs, setNumsegs ] = useState(`${props.parameters.numsegs}`)
  const [ assemblyMode, setAssemblyMode ] = useState(props.parameters.assembly_mode)

  const handleDurationChange = (ev: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(ev.currentTarget.value, 10)
    if (!isNaN(value)) {
      setDuration(`${value}`)
    }
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
  }

  const handleSubmit = async (ev: React.FormEvent<HTMLFormElement>) => {
    ev.preventDefault()
    const url = '/api/autoedit' // '/actions/autoedit'
    const parameters = { files, duration, numsegs, assembly_mode: assemblyMode }
    const response = await http.post(url, parameters as ApiData)
    props.addTask(response.data)
  }

  return (
    <form onSubmit={handleSubmit}>
      <MultiFileChooser setFiles={setFiles} selected={files} />
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
      <input type="submit" value="start" />
    </form>
  )
}

export { AutoEdit }
