import './styles/App.css'
import { useState, useEffect } from 'react'
import Select from 'react-select'
import Button from './components/Button'
import selectStyles from './styles/selectStyle'
import selectTheme from './styles/selectTheme'

function App() {

  const [team_dropdown, setTeamDropdown] = useState()
  const [player_dropdown, setPlayerDropdown] = useState()
  const [player_options, setPlayerOptions] = useState()
  const [team, setTeam] = useState()
  const [player1, setPlayer1] = useState()
  const [player2, setPlayer2] = useState()
  const [graph, setGraph] = useState()

  return (
    <div className='App'>
      <div className='sketch'></div>
    <div className='content'>
      <div className='select-row-1'>
        <Select
          styles={selectStyles}
          theme={selectTheme}
        />
      </div>
      <div className='select-row-2'>
        <div className='col-select col-left'>
          <Select
            styles={selectStyles}
            theme={selectTheme}
          />
        </div>
        <Button text='Link!'/>
        <div className='col-select col-right'>
          <Select
            styles={selectStyles}
            theme={selectTheme}
          />
        </div>
      </div>
      <div className='graph-div'></div>
    </div>
    </div>
  );
}

export default App
