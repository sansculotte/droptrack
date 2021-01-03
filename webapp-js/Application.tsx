import http from 'lib/http'
import * as React from 'react'

import ExpireMessage from 'components/ExpireMessage'
import FileDrop from 'components/FileDrop'

import ApiResponse from 'interfaces/ApiResponse' 

import * as style from './Application.scss'

interface Props {
}

interface State {
    files: Array<any>
    message?: string
    url: string
    dt_item: string
    dt_items: Array<any>
}

class Application extends React.Component<Props, State> {

  constructor(props: Props) {
      super(props)
      
    this.state = {
      files: [],
	url: '',
	dt_item: '',
	dt_items: [],
    }

  }

  public render() {
    return (
      <main className={style.app}>
        <h1>Droptrack</h1>
        {this.state.message &&
          <ExpireMessage delay={2000}>{this.state.message}</ExpireMessage>
        }
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
	    
      </main>
    )
  }

  handleDropFile(files: Array<any>) {
    const results = files.map(f => http.upload('/files', f, 'soundfile'))
    if (results.length > 0) {
      results[0].then((response: ApiResponse) => {
        const { message } = response
        this.setState({message})
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
      this.setState({message})
    }).catch(console.error)
  }
}

export default Application
