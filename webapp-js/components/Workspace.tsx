import * as React from 'react'

import http from 'lib/http'
import FileDrop from './FileDrop'
import FileList from './FileList'
import FileUrl from './FileUrl'

import ApiResponse from 'interfaces/ApiResponse'
import File from 'interfaces/File'
import Task from 'interfaces/Task'


interface Props {
  flashMessage: (message: string) => void
}

interface State {
  files: Array<File>
  tasks: Array<Task>
  message?: string
  showFileList: boolean
}


class Workspace extends React.Component<Props, State> {

  constructor(props: Props) {
    super(props)
    this.state = {
      files: [],
      tasks: [],
      showFileList: false,
    }
  }

  public componentDidMount() {
    this.loadFileList()
  }

  render() {
    return (
      <div>

        <form>
          <FileUrl flashMessage={this.props.flashMessage} />
          <FileDrop accept="audio/*" onDrop={this.handleDropFile.bind(this)} />
        </form>
        {this.state.showFileList
          ? <>
              <input type="button" onClick={this.hideFileList.bind(this)} value="Hide Files" />
              <FileList files={this.state.files} />
            </>
          : <input type="button" onClick={this.showFileList.bind(this)} value="Show Files"/>
        }
      </div>
    )
  }

  handleDropFile(files: Array<any>) {
    const results = files.map(f => http.upload('/files', f, 'soundfile'))
    if (results.length > 0) {
      results[0].then((response: ApiResponse) => {
        const { message } = response
        this.props.flashMessage(message)
      }).catch((error: ApiResponse) => console.error(error))
    }
    else {
        console.error('no files')
    }
  }

  showFileList() {
    this.setState({showFileList: true}, () => this.loadFileList())
  }

  hideFileList() {
    this.setState({showFileList: false})
  }

  async loadFileList() {
    const response = await http.get('/files')
    if (response.status === 'ok') {
      const { files } = response
      this.setState({files})
    }
  }
}

export default Workspace
