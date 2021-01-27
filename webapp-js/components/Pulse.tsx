import * as React from 'react'

import * as styles from './Pulse.scss'


export default () =>
  <div className={styles.pulse}
    style={
      {
        width: '25px',
        height: '25px',
        borderRadius: '50%',
      }
    }
  />
