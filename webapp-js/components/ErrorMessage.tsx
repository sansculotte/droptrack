import React from 'react'

import * as styles from './ErrorMessage.scss'

interface Props {
  errors: Array<string>
}

const ErrorMessage = (props: Props) =>
  <div className={styles.error}>
    {props.errors.map((error, index) =>
      <div key={`${index}`}>{ error }</div>
    )}
  </div>

export { ErrorMessage }
