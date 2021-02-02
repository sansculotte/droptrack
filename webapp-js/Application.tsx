import * as React from 'react'

import AuthModal from 'components/AuthModal'
import Workspace from 'components/Workspace'
import ExpireMessage from 'components/ExpireMessage'

import * as style from './Application.scss'


interface Props {
}

interface State {
  authenticate: boolean
  message?: string
}


class Application extends React.Component<Props, State> {

  constructor(props: Props) {
    super(props)
    this.state = {
      message: undefined,
      authenticate: false,
    }
  }

  public componentDidMount() {
    const apiKey = window.localStorage.getItem('apiKey')
    if (apiKey === null) {
      this.setState({authenticate: true})
    }
  }

  public render() {
    return (
      <main className={style.app}>
        <h1>Droptrack</h1>
        {this.state.message &&
          <ExpireMessage
            delay={3500}
            timeStamp={new Date().getTime()}
          >{this.state.message}</ExpireMessage>
        }
        {this.state.authenticate
          ? <AuthModal setKey={this.setKey.bind(this)} />
          : <Workspace flashMessage={this.flashMessage.bind(this)} />
        }
      </main>
    )
  }

  private setKey(key: string) {
    window.localStorage.setItem('apiKey', key)
    this.setState({ authenticate: false })
  }

  private flashMessage(message: string) {
    this.setState({ message })
  }
}

export default Application
