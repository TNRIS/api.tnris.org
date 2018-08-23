import React from 'react';
import {Link} from 'react-router-dom';

import CollectionList from './CollectionList';

export default class Catalog extends React.Component {
  render() {
    return (
      <div>
        <h1>Welcome to the holodeck!</h1>
        <h2>i'm the catalog</h2>
        <img
          src='https://cdn-images-1.medium.com/max/800/1*z-jt1KCPbEFCaPBDOpSBrQ.gif'
          alt=''
        />
        <p>
          <Link to='/map'>Click Here</Link> to see the map!
        </p>
        <CollectionList />
      </div>
    );
  }
}
