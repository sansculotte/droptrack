import * as React from 'react'

import * as style from './ExpireMessage.scss'


interface Props {
  delay?: number
  children: React.ReactNode
}

interface State {
  visible: boolean
}


export default class ExpireMessage extends React.Component<Props, State> {

  timer: number | undefined

  constructor(props: Props) {
    super(props)
    this.timer = undefined
    this.state = {visible: true}
  }

  public componentDidUpdate(prevProps: Props) {
    if (this.props.children !== prevProps.children) {
      this.setTimer()
      this.setState({visible: true})
    }
  }

  public componentDidMount() {
    this.setTimer()
  }

  public componentWillUnmount() {
    clearTimeout(this.timer)
  }

  public render() {
    return this.state.visible
      ? <div className={style.message}>{this.props.children}</div>
      : null 
  }

  private setTimer() {
    // clear any existing timer
    if (this.timer !== undefined) {
      clearTimeout(this.timer)
    }

    // hide after `delay` milliseconds
    this.timer = setTimeout(() => {
        this.setState({visible: false})
        this.timer = undefined
      },
      this.props.delay
    )
  }
}
