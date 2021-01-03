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

const API_URL = 'http://127.0.0.1:5000'

class Application extends React.Component<Props, State> {

  constructor(props: Props) {
      super(props)
      
    this.state = {
      files: [],
	url: '',
	dt_item: '',
	dt_items: [],
    }

      // fetch data
      this.fetchData();
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
	    
	<div>
	    <h1>droptrack items</h1>
	    <h2>fetch a list from the API and display it</h2>

	    { /* file browser, fetch data and list */ }
	
	    <div>
                <button className="fetch-button" onClick={this.fetchData}>
                Fetch Data
                </button>
	    </div>

	    <div>
	        {this.state.dt_item && <h3>dt_item {this.state.dt_item}</h3>}
	        {Object.keys(this.state.dt_items).length>0 && <p>dt_items length {Object.keys(this.state.dt_items).length}</p>}
	        {
		    Object.keys(this.state.dt_items).length>0 &&
			this.state.dt_items.map(item => (
			    <p>{item.dt_item} {item.dt_item_path}</p>
			))
		}
	    </div>

	</div>
      </main>
    )
  }

    fetchData = async () => {
	console.log('fetching ' + API_URL)
    	fetch(API_URL + '/item?dt_item=zniz')
    	    .then(res => res.json())
    	    .then(
    		(result) => {
    		    this.setState({
    		    	// isLoaded: true,
			dt_item: result.dt_item,
    		    	dt_items: result.dt_item_content,
    		    });
		    console.log('result.dt_item ' + result.dt_item)
		    console.log('state.dt_item ' + this.state.dt_item)
		    // console.log(result.dt_item_content)
    		},
    		// Note: it's important to handle errors here
    		// instead of a catch() block so that we don't swallow
    		// exceptions from actual bugs in components.
    		(error) => {
		    console.error(error)
    		    // this.setState({
    		    // 	isLoaded: true,
    		    // 	error
    		    // });
    		}
    	    )
    }
    
    // fetchData = async () => {
    //     // const response = await axios.get(API_URL)

    // 	fetch(this.API_URL)
    // 	    .then(res => res.json())
    // 	    .then(
    // 		(result) => {
    // 		    this.setState({
    // 			isLoaded: true,
    // 			items: result.items
    // 		    });
    // 		},
    // 		// Note: it's important to handle errors here
    // 		// instead of a catch() block so that we don't swallow
    // 		// exceptions from actual bugs in components.
    // 		(error) => {
    // 		    this.setState({
    // 			isLoaded: true,
    // 			error
    // 		    });
    // 		}
    // 	    )
    // 	// setBooks(response.data) 

    // }

    handleDropFile(files: Array<any>) {
    const results = files.map(f => http.upload('/upload', f, 'soundfile'))
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
