import './styles/App.css'
import { useState, useEffect } from 'react'
import Select from 'react-select'
import Button from './components/Button'
import MenuList from './components/menuList'
import Graph from './components/Graph'
import Sketch from './components/Sketch'
import selectStyles from './styles/selectStyle'
import selectTheme from './styles/selectTheme'

function App() {

  const [team_dropdown, setTeamDropdown] = useState()
  const [player_dropdown, setPlayerDropdown] = useState([])
  const [player_options, setPlayerOptions] = useState()
  const [team, setTeam] = useState({label:'', value: ''})
  const [player1, setPlayer1] = useState()
  const [player2, setPlayer2] = useState()
  const [graph, setGraph] = useState()

  const changeTeam = (e) => {
    setTeam(e)
    if (e.value === 'World') return
    setPlayer1(null)
    setPlayer2(null)
  }

  const updateGraph = () => {
    if (!team || !player1 || !player2) return
    setGraph(
      <Graph
        team={team.value}
        player1={player1}
        player2={player2}
      />
    )
  }

  useEffect(() => {
    fetch('api/get_team_dropdown').then(res => res.json()).then(data => {setTeamDropdown(data.data)})
    fetch('api/get_player_dropdown').then(res => res.json()).then(data => {setPlayerDropdown(data.data)})
  }, [])

  useEffect(() => {
    setPlayerOptions(player_dropdown.filter(players => players.team === team.value))
  }, [team, player_dropdown])

  return (
    <div className='App'>
      <div className='sketch'>
        <Sketch/>
      </div>
    <div className='content'>
      <div className='select-row-1'>
        <Select
          options={team_dropdown}
          onChange={changeTeam}
          styles={selectStyles}
          theme={selectTheme}
        />
      </div>
      <div className='select-row-2'>
        <div className='col-select col-left'>
          <Select
            components={{MenuList}}
            value={player1}
            options={player_options}
            onChange={(e) => {setPlayer1(e)}}
            styles={selectStyles}
            theme={selectTheme}
          />
        </div>
        <Button text='Link!' onClick={updateGraph}/>
        <div className='col-select col-right'>
          <Select
            components={{MenuList}}
            value={player2}
            options={player_options}
            onChange={(e) => {setPlayer2(e)}}
            styles={selectStyles}
            theme={selectTheme}
          />
        </div>
      </div>
      <div className='graph-div'>
        {graph}
      </div>
    </div>
    </div>
  );
}

export default App
