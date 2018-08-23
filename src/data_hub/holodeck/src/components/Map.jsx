import React from 'react';
import {Link} from 'react-router-dom';

import ResourceList from './ResourceList';

export default class Map extends React.Component {
  render() {
    return (
      <div>
        <h1>Welcome to the holodeck!</h1>
        <h2>i'm the map</h2>
        <img
          style={{width: '75%'}}
          src='https://i.kym-cdn.com/photos/images/original/000/895/634/08a.gif'
          alt=''
        />
        <p>
          <Link to='/'>Click Here</Link> to see the catalog!
        </p>
        <ResourceList />
      </div>
    );
  }
}
