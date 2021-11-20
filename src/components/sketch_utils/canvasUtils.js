import _ from 'lodash'

export const canvasUtils = {
  fadeCanvas(pct, canvas, rgb, params) {
    canvas.fillStyle = `rgba(${rgb}, ${pct})`
    canvas.fillRect(0, 0, params.width, params.height)
  },
  createPathMethod(points, canvas) {
    canvas.beginPath()
    points.map((point, idx) => {
      let method = point.type
      canvas[method](...point.args)
    })
  },
  drawDot(point, canvas, color) {
    canvas['fillStyle'] = color
    this.createPathMethod([
      {
        type: 'arc',
        args: [point.x, point.y, point.r || 2, 0, Math.PI * 2, false]
      }
    ], canvas)
    canvas['fill']()
  }
}
