import File from 'interfaces/File'

interface ActionBase {
  name: string
  url: string
}

type AssemblyMode = 'random' | 'sequential'

interface AutoEditParameters {
  duration: number
  files: Array<File>
  assembly_mode: AssemblyMode
  [key: string]: AssemblyMode | number | Array<File>
}

interface AutoEdit extends ActionBase {
  parameters: AutoEditParameters
}

interface AutoCoverParameters {
  duration: number
  files: Array<File>
  [key: string]: string | number | Array<File>
}

interface AutoCover extends ActionBase {
  parameters: AutoCoverParameters 
}

type Action = AutoEdit | AutoCover

export default Action
export { AutoEdit, AutoCover, AutoEditParameters, AutoCoverParameters }
