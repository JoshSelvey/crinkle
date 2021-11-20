const selectTheme = (theme) => ({
  ...theme,
  colors: {
    ...theme.colors,
    primary25: '#B3E3F9',
    primary: '#b9314f',
    neutral20: 'black',
    neutral30: 'black',
  }
})

export default selectTheme
