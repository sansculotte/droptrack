import React from 'react'

import Pulse from './Pulse'

export default () =>
  <div style={{display: 'flex'}}>
    <Pulse size={16}/>
    <div style={{marginLeft: '20px'}}>Processing...</div>
  </div>
