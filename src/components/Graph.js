import { useEffect, useState } from 'react'
import * as d3 from 'd3'

const Graph = ({ team, player1, player2 }) => {
  const [message, SetMessage] = useState()

  useEffect(() => {
    const width = parseFloat(d3.select('.graph-div').style('width'))
    const height = parseFloat(d3.select('.graph-div').style('height'))
    const dominant_dim = width > height ? width : height

    const svg = d3.select('.svg-container')
      .html(null)
      .attr('width', width)
      .attr('height', height)
      .attr('viewBox', [-width/2, -height/2, width, height])

    const getLink = async () => {
      const response = await fetch(`/api/get_link_data/${team}/${player1.value}/${player2.value}`)
      var { nodes, links } = await response.json()



      const N = d3.map(nodes, d => d.id)
      const G = d3.map(nodes, d => d.group)
      const I = d3.map(nodes, d => `/images/${d.id}.jpg`)
      const T = d3.map(nodes, d => d.name)
      const LS = d3.map(links, ({source}) => source)
      const LT = d3.map(links, ({target}) => target)

      const n_groups = Math.max.apply(Math, G)

      switch(n_groups) {
        case -Infinity:
          SetMessage(<><b>No link found.</b></>)
          break
        case 1:
          SetMessage(<><b>{player1.label}</b> has played with themselves.</>)
          break
        case 2:
          SetMessage(<><b>{player1.label}</b> played with <b>{player2.label}</b></>)
          break
        default:
          SetMessage(
            <><b>{player1.label}</b> linked to <b>{player2.label}</b> with <b>{n_groups-1}</b> degrees of separation.</>
          )
      }

      const radius = dominant_dim / (8*Math.sqrt(nodes.length))
      const stroke = radius / 10
      const margin = 2 * radius
      const effective_dim = dominant_dim - (2 * margin)

      const color = d3.scaleOrdinal(d3.sort(G), d3.schemeTableau10)

      nodes = d3.map(nodes, (_, i) => ({id: N[i], group: G[i]}))
      links = d3.map(links, (_, i) => ({source: LS[i], target: LT[i]}))

      console.log(links)

      function isolate(force, filter) {
        var initialize = force.initialize
        force.initialize = function() { initialize.call(force, nodes.filter(filter))}
        return force
      }

      const simulation = d3.forceSimulation(nodes)
        .force('link', d3.forceLink(links).id(({index: i}) => N[i]).distance(effective_dim/((n_groups-1))))
        .force('collide', d3.forceCollide().radius(function(d) {return radius}))
        .force('center', d3.forceY(0))
        .on('tick', ticked)

      if (width > height) {
        simulation.force('center', d3.forceY(0))
        for (let i = 0; i < n_groups; i++) {
          simulation.force(`link${i}`, isolate(d3.forceX(-(effective_dim/2) + (effective_dim * i / (n_groups -1))), function(d) {return d.group === i+1}, i))
        }
      } else {
        simulation.force('center', d3.forceX(0))
        for (let i = 0; i < n_groups; i++) {
          simulation.force(`link${i}`, isolate(d3.forceY(-(effective_dim/2) + (effective_dim * i / (n_groups - 1))), function(d) {return d.group === i+1}, i))
        }
      }

      const link = svg.append('g')
        .attr('stroke', '#999')
        .attr('stroke-opacity', '0.6')
        .attr('stroke-width', stroke/2)
        .attr('stroke-linecap', 'round')
        .selectAll('line')
        .data(links)
        .join('line')

      svg.append('defs')
        .selectAll('pattern')
        .data(nodes)
        .join('pattern')
        .attr('height', 1)
        .attr('width', 1)
        .attr('id', ({index: i}) => N[i])
        .append('image')
        .attr('height', 2*radius)
        .attr('width', 2*radius)
        .attr('xlink:href', ({index: i}) => I[i]);

      const node = svg.append('g')
        .selectAll('circle')
        .data(nodes)
        .join('circle')
        .attr('stroke-width', stroke)
        .attr('stroke', ({index: i}) => color(G[i]))
        .attr('r', radius)
        .attr('fill', ({index: i}) => `url(#${N[i]})`)
        .call(drag(simulation))

      node.append('title').text(({index: i}) => T[i])

      function ticked() {
        link
          .attr('x1', d => d.source.x)
          .attr('y1', d => d.source.y)
          .attr('x2', d => d.target.x)
          .attr('y2', d => d.target.y)
        node
          .attr('cx', d => d.x)
          .attr('cy', d => d.y)
      }

      function drag(simulation) {
        const dragstarted = (event) => {
          if (!event.active) simulation.alphaTarget(0.3).restart()
          event.subject.fx = event.subject.x
          event.subject.fy = event.subject.y
        }
        const dragged = (event) => {
          event.subject.fx = event.x
          event.subject.fy = event.y
        }
        const dragended = (event) => {
          if (!event.active) simulation.alphaTarget(0);
          event.subject.fx = null;
          event.subject.fy = null;
        }
        return d3.drag()
          .on('start', dragstarted)
          .on('drag', dragged)
          .on('end', dragended)
      }
    }
    getLink()
  }, [team, player1, player2])

  return (
    <div>
      <div className='graph-info'>
        {message}
      </div>
      <div>
        <svg className='svg-container'/>
      </div>
    </div>
  )
}

export default Graph
