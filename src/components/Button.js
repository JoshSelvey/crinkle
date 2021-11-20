const Button = ({ text, onClick }) => {
  return (
    <div className='btn-div'>
      <button onClick={onClick} className='btn'>
        {text}
      </button>
    </div>
  )
}

export default Button
