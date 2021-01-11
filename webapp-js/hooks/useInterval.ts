import { useEffect, useRef } from 'react'


const useInterval = (callback: () => void, delay: number) => {
  const persistentCallback = useRef<Function>(callback)

  useEffect(() => {
    const tick = () => {
      if (persistentCallback.current) { 
        persistentCallback.current()
      }
    }
    if (delay > 0) {
      const id = setInterval(tick, delay)
      return () => clearInterval(id)
    }
  }, [callback, delay])
}

export { useInterval }
