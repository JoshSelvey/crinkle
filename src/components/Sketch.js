import { useState, useEffect } from 'react'
import _ from 'lodash'
import { movementUtils } from './sketch_utils/movementUtils'
import { canvasUtils } from './sketch_utils/canvasUtils'

const INTERVAL_LENGTH = 10
const NUM_STREAMS = 20
const CANVAS_RGB = '132, 210, 246'
const BUBBLE_RGB = 'rgba(0, 71, 122, 0.6)'
const HEIGHT_PADDING = 106
const WIDTH_PADDING = 96

const SPEED_MIN = 1
const SPEED_MAX = 3
const RADIUS_MIN = 2
const RADIUS_MAX = 10

function Sketch() {

  const [height, setHeight] = useState(window.innerHeight - HEIGHT_PADDING)
  const [width, setWidth] = useState(window.innerWidth - WIDTH_PADDING)
  const [points, setPoints] = useState(_.times(NUM_STREAMS, () => null))
  const [canvas, setCanvas] = useState()

  const draw = () => {
    canvasUtils.fadeCanvas(0.6, canvas.getContext('2d'), CANVAS_RGB, {width: window.innerWidth - WIDTH_PADDING, height: window.innerHeight - HEIGHT_PADDING})
    _.times(NUM_STREAMS, idx => {drawPoint(idx)})
}

const drawPoint = (idx) => {
  let point = points[idx] || movementUtils.createPoint({
    speedMin: SPEED_MIN,
    speedMax: SPEED_MAX,
    boundX: width,
    boundY: height,
    radiusMin: RADIUS_MIN,
    radiusMax: RADIUS_MAX,
  })
  point = movementUtils.moveRandomly(point, {
    width: width,
    height: height
  })
  canvasUtils.drawDot(point, canvas.getContext('2d'), BUBBLE_RGB)
  points[idx] = point
  setPoints(points)
}

  useEffect(() => {
    if (!canvas) return
    canvasUtils.fadeCanvas(1, canvas.getContext('2d'), CANVAS_RGB, {width: window.innerWidth - WIDTH_PADDING, height: window.innerHeight - HEIGHT_PADDING})
    window.setInterval(draw, INTERVAL_LENGTH)
  }, [canvas])

  useEffect(() => {
    const checkSize = () => {
      setHeight(window.innerHeight - HEIGHT_PADDING)
      setWidth(window.innerWidth - WIDTH_PADDING)
    }
    window.addEventListener('resize', checkSize)
    return () => window.removeEventListener('resize', checkSize)
  }, [])

  return (
    <div className='canvas'>
      <canvas
        width={width}
        height={height}
        ref={cvs => setCanvas(cvs)}
      />
    </div>
  )
}

export default Sketch
