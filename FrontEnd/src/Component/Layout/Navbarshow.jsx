import React, { useEffect, useState } from 'react'
import { useLocation } from 'react-router-dom'

const NavbarShow = ({children}) => {
    const Location  = useLocation();
    const [Show, setShow] = useState(false);
    useEffect(() => {
      if(Location.pathname==="/Login" || Location.pathname==="/login" || Location.pathname==="/register" || Location.pathname==="/Register" ){
        setShow(false);
      }else if(Location.pathname==="/" || Location.pathname==="/about" || Location.pathname==="/addpost" || Location.pathname==="/edit" || Location.pathname==="/chat" || Location.pathname==="/properties" || Location.pathname==="/profile-update" || Location.pathname==="/add-property" || Location.pathname==="/bookings"){
        setShow(true);
      }else if (Location.pathname.includes("/properties/")){
        setShow(true);
      }else{
        setShow(false);
      }

    }, [Location])
    
  return (
    <>{Show && children}</>
  )
}

export default NavbarShow;