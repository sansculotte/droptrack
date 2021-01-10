import * as React from 'react'

import http from 'lib/http'
import FileDrop from './FileDrop'
import FileList from './FileList'

import ApiResponse from 'interfaces/ApiResponse' 
import File from 'interfaces/File'


interface Props {
  flashMessage: (message: string) => void
}

interface State {
  files: Array<File>
  message?: string
  url: string
  showFileList: boolean
}


class Dashboard extends React.Component<Props, State> {

  constructor(props: Props) {
    super(props)
    this.state = {
      files: [],
      url: '',
      showFileList: false,
    }
  }

  public componentDidMount() {
    this.loadFileList()
  }

  render() {
    return (
      <>
      <form>
        <input
          name="url"
          type="url"
          placeholder="soundfile url"
          onChange={this.handleChangeUrl.bind(this)}
          value={this.state.url}
        />
        <input type="button" onClick={this.handleDropUrl.bind(this)} value="Drop" />
        <FileDrop accept="audio/*" onDrop={this.handleDropFile.bind(this)} />
      </form>
      {this.state.showFileList
        ? <>
            <input type="button" onClick={this.hideFileList.bind(this)} value="Hide Files" />
            <FileList files={this.state.files} />
          </>
        : <input type="button" onClick={this.showFileList.bind(this)} value="Show Files"/>
      }
      </>
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

  handleChangeUrl(ev: React.FormEvent<HTMLInputElement>) {
    const url = ev.currentTarget.value
    this.setState({url})
  }

  handleDropUrl(ev: React.MouseEvent) {
    ev.preventDefault()
    http.post('/url', {url: this.state.url}).then((response: ApiResponse) => {
      const { message } = response
      this.props.flashMessage(message)
    }).catch(console.error)
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

export default Dashboard
