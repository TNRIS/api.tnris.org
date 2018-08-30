import React from 'react';

import Header from './Header';
import Footer from './Footer';
import CatalogContainer from '../containers/CatalogContainer';

export default class Main extends React.Component {

  render() {
    return (
      <div>
        <Header />
        <CatalogContainer />
        <Footer className='footer navbarFixedBottom' />
      </div>
    );
  }
}
