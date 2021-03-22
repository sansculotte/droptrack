import File from 'interfaces/File'

interface ActionBase {
  name: string
  url: string
}

type AssemblyMode = 'random' | 'sequential'

interface AutoEditParameters {
  duration: number
  numsegs: number
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
  output_format: Array<string> 
  [key: string]: string | string[] | number | Array<File>
}

interface AutoCover extends ActionBase {
  parameters: AutoCoverParameters 
}

interface AutoMasterParameters {
  files: Array<File>
  bitdepth: number
  [key: string]: number | Array<File>
}

interface AutoMaster extends ActionBase {
  parameters: AutoMasterParameters
}

type Action = AutoEdit | AutoCover | AutoMaster

export default Action
export { AutoEdit, AutoCover, AutoMaster, AutoEditParameters, AutoCoverParameters, AutoMasterParameters }
