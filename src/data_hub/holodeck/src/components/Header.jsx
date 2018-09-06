import React from 'react';

export default class Header extends React.Component {

  render() {
    return (
      <div className='header-component'>
        <div className='header-title'>
          <span className='header-title__tnris'>Texas Natural Resources Information System</span>
          <a className='header-title__twdb' href="">A Division of the Texas Water Development Board</a>
        </div>
        <div className='header-nav'>
          Look at this nav!
        </div>
      </div>
    );
  }
}
