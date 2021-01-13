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
// import Transformation from 'interfaces/Transformation'


interface Props {
  flashMessage: (message: string) => void
}

interface State {
  activeWidget: 'drop' | 'files' | 'tasks'
  files: Array<File>
  lastUpdate: number
  message?: string
  tasks: Map<string, Task>
  // transformations: Array<Transformation>
}


class Workspace extends React.Component<Props, State> {

  constructor(props: Props) {
    super(props)
    this.state = {
      files: [],
      tasks: new Map(),
      lastUpdate: new Date().getTime(),
      // transformations: [],
      activeWidget: 'drop'
    }
  }

  public componentDidMount() {
    this.loadFileList()
  }

  render() {
    return (
      <div>
        <menu>
          <input type="button" onClick={this.hideAll.bind(this)} value="Drop" />
          <input type="button" onClick={this.showFileList.bind(this)} value="Files" />
          <input type="button" onClick={this.showTasks.bind(this)} value="Tasks" />
          <TaskPoll
            tasks={this.state.tasks}
            updateTasks={this.updateTasks.bind(this)}
            flashMessage={this.props.flashMessage}
          />
        </menu>
        {this.state.activeWidget === 'files'
          && <FileList files={this.state.files} />
        }
        {this.state.activeWidget === 'tasks'
          && <TaskList tasks={this.state.tasks} />
        }
        <form>
          <FileDrop accept="audio/*" onDrop={this.handleDropFile.bind(this)} />
          <FileUrl addTask={this.addTask.bind(this)} flashMessage={this.props.flashMessage} />
        </form>
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

  hideAll() {
    this.setState({activeWidget: 'drop'})
  }

  showFileList() {
    this.setState({activeWidget: 'files'}, () => this.loadFileList())
  }

  showTasks() {
    this.setState({activeWidget: 'tasks'})
  }

  addTask(task: Task) {
    const { tasks } = this.state
    tasks.set(task.uuid, task)
    this.setState({ tasks })
 }

  updateTasks(tasks: Map<string, Task>) {
    const lastUpdate = new Date().getTime()
    this.setState({tasks, lastUpdate})
  }

  async loadFileList() {
    const response = await http.get('/files')
    if (response.status === 'ok') {
      const { files } = response.data
      this.setState({ files })
    }
  }
}

export default Workspace
