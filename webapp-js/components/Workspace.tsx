import * as React from 'react'

import http from 'lib/http'
import FileDrop from './FileDrop'
import FileList from './FileList'
import FileUrl from './FileUrl'
import TaskList from './TaskList'
import TaskPoll from './TaskPoll'

import ApiResponse from 'interfaces/ApiResponse'
import File from 'interfaces/File'
import Task from 'interfaces/Task'

import * as styles from '../Application.scss'


interface Props {
  flashMessage: (message: string) => void
}

interface State {
  activeWidget: 'drop' | 'files' | 'tasks'
  files: Array<File>
  lastUpdate: number
  message?: string
  tasks: Map<string, Task>
}


class Workspace extends React.Component<Props, State> {

  constructor(props: Props) {
    super(props)
    this.state = {
      files: [],
      tasks: new Map(),
      lastUpdate: new Date().getTime(),
      activeWidget: 'drop'
    }
  }

  public componentDidMount() {
    this.loadFileList()
  }

  public render() {
    return (
      <div>
        <menu>
          <input type="button" onClick={this.hideAll.bind(this)} value="Drop" />
          <input type="button" onClick={this.showFileList.bind(this)} value="Files" />
          <a className={styles.button} onClick={this.showTasks.bind(this)}>
              <span>Tasks</span>
              <TaskPoll
                tasks={this.state.tasks}
                updateTasks={this.updateTasks.bind(this)}
                flashMessage={this.props.flashMessage}
              />
          </a>
        </menu>
        {this.state.activeWidget === 'drop'
          && (
            <form>
              <FileDrop accept="audio/*" onDrop={this.handleDropFile.bind(this)} />
              <FileUrl addTask={this.addTask.bind(this)} flashMessage={this.props.flashMessage} />
            </form>
          )
        }
        {this.state.activeWidget === 'files'
          && <FileList files={this.state.files} />
        }
        {this.state.activeWidget === 'tasks'
          && <TaskList tasks={this.state.tasks} />
        }
     </div>
    )
  }

  private handleDropFile(files: Array<any>) {
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

  private hideAll() {
    this.setState({activeWidget: 'drop'})
  }

  private showFileList() {
    this.setState({activeWidget: 'files'}, () => this.loadFileList())
  }

  private showTasks() {
    this.setState({activeWidget: 'tasks'})
  }

  private addTask(task: Task) {
    const { tasks } = this.state
    tasks.set(task.uuid, task)
    this.setState({ tasks })
 }

  private updateTasks(tasks: Map<string, Task>) {
    const lastUpdate = new Date().getTime()
    this.setState({tasks, lastUpdate})
  }

  private async loadFileList() {
    const response = await http.get('/files')
    if (response.status === 'ok') {
      const { files } = response.data
      this.setState({ files })
    }
  }
}

export default Workspace
