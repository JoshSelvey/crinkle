import { components } from 'react-select'

const MenuList = ({ children, ...props }) => {
  return (
      <components.MenuList {...props}>
          {Array.isArray(children)
              ? children.slice(0, 5) : children
          }
      </components.MenuList>
  )
}

export default MenuList
