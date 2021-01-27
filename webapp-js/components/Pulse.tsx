import * as React from 'react'

import * as styles from './Pulse.scss'


export default (props: {size?: number}) => {

  const size = props.size || 20

  return (
    <div className={styles.pulse}
      style={
        {
          width: `${size}px`,
          height: `${size}px`,
          borderRadius: '50%',
        }
      }
    />
  )
}
