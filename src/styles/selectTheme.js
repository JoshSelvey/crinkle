const selectTheme = (theme) => ({
  ...theme,
  colors: {
    ...theme.colors,
    primary25: '#B3E3F9',
    primary: 'black',
    neutral10: 'black',
    neutral15: 'black',
    neutral20: 'black',
    neutral30: 'black',
    neutral40: 'black',
    neutral50: 'black',
  }
})

export default selectTheme
