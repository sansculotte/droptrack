import '@babel/polyfill'
import * as React from 'react'
import * as ReactDOM from 'react-dom'
import Application from './Application'

const container = document.getElementById('application-root')

if (container instanceof Element) {
  ReactDOM.render(<Application />, container)
}
