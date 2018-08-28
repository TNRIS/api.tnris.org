import React from 'react';
import {Link} from 'react-router-dom';

import CollectionList from './CollectionList';

export default class Catalog extends React.Component {

  componentDidMount() {
    this.props.fetchCollections();
    this.props.fetchResources();
  }

  render() {
    console.log(this.props);
    const { error, loading } = this.props;
    const loadingMessage = <div>Loading...</div>;

    if (error) {
      return <div>Error! {error.message}</div>;
    }

    if (loading) {
      return loadingMessage;
    }

    return (
      <div className='container catalog-component'>
        <div className='row'>
          <h1 className='col text-center'>Welcome to the holodeck!</h1>
        </div>
        <div className='row'>
          <h2 className='col text-center'>i'm the catalog</h2>
        </div>
        <div className='row'>
          {/*<img
            className='col'
            src='https://cdn-images-1.medium.com/max/800/1*z-jt1KCPbEFCaPBDOpSBrQ.gif'
            alt=''
          />*/}
          IMAGE
        </div>
        <div className='row'>
          <h4
            className='col text-center'
            style={{paddingTop: '10px'}}><Link to='/map'>Click Here</Link> to see the map!
          </h4>
        </div>
        <CollectionList className='row' collections={this.props.collections}/>
      </div>
    );
  }
}
