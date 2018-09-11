import React from 'react';
import SortContainer from '../containers/SortContainer';

import logo from '../images/tnris_logo_white.png'

export default class Header extends React.Component {

  render() {
    return (
      <div className='header-component'>
        <div className='header-title'>
          <span className='header-title__tnris'>Texas Natural Resources Information System</span>
          <a className='header-title__twdb' href="">A Division of the Texas Water Development Board</a>
        </div>
        <div className='header-nav'>
          <div className='logo-container'>
            <img src={logo} alt="TNRIS.org Logo" className="tnris-logo" />
          </div>
          <div className='buttons-container'>
            <SortContainer />
          </div>
        </div>
      </div>
    );
  }
}
