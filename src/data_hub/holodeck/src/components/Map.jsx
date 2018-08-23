import React from 'react';
import {Link} from 'react-router-dom';

import ResourceList from './ResourceList';

export default class Map extends React.Component {
  render() {
    return (
      <div className='container'>
        <div className='row'>
          <h1 className='col text-center'>Welcome to the holodeck!</h1>
        </div>
        <div className='row'>
          <h2 className='col text-center'>i'm the map</h2>
        </div>
        <div className='row'>
          <img
            className='col'
            style={{height: '500px'}}
            src='https://i.kym-cdn.com/photos/images/original/000/895/634/08a.gif'
            alt=''
          />
        </div>
        <div className='row'>
          <h4
            className='col text-center'
            style={{paddingTop: '10px'}}><Link to='/'>Click Here</Link> to see the catalog!
          </h4>
        </div>
        <ResourceList className='row' />
      </div>
    );
  }
}
