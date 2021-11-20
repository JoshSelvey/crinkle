import _ from 'lodash'

export const movementUtils = {
  createPoint(params) {
    const speed = _.random(params.speedMin, params.speedMax, true)
    const dir = _.random(2 * Math.PI, true)
    const point = {
      x: _.random(params.boundX),
      y: _.random(params.boundY),
      speed: speed,
      dir: dir,
      dx: speed * Math.cos(dir),
      dy: speed * Math.sin(dir),
      rx: Math.cos(.03),
      ry: Math.sin(.03),
      r: _.random(params.radiusMin, params.radiusMax)
    }
    return point
  },
  isOutOfBounds(pos, bound) {
    let padding = 10
    return pos >= bound - padding || pos <= padding
  },
  moveRandomly(point, params) {
    const defaults = {
      padding: 10,
      maxMovement: 20
    }
    let config = _.extend({}, defaults, params)
    point = _.clone(point)
    const updatePos = (pos, dir, bound) => {
      if (this.isOutOfBounds(pos + dir, bound, config.padding)) {
        dir = this.getNewDir(pos, bound, point.speed || config.maxMovement, config.padding)
      }
      return dir
    }
    point.dx = updatePos(point.x, point.dx, config.width)
    point.dy = updatePos(point.y, point.dy, config.height)
    point.x += point.dx
    point.y += point.dy
    return point
  },
  getNewDir(pos, bound, speed, padding) {
    let newDir = _.random(speed, true)
    let sign = pos + newDir > bound - padding ? -1 :
               pos - newDir < padding ? 1 :
               _.random() ? -1 : 1
    return newDir * sign
  }
}
