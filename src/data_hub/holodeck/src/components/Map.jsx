import React from 'react';
import {Link} from 'react-router-dom';

export default class Map extends React.Component {

  render() {

    return (
      <div className='map-selector'>
        <h1 className='mdc-typography--headline1'>map</h1>
        <div className=''>
          <img
            className='col'
            style={{height: '500px'}}
            src='https://i.kym-cdn.com/photos/images/original/000/895/634/08a.gif'
            alt=''
          />
        </div>
      </div>
    );
  }
}
