import React from 'react';

import CatalogCardContainer from '../containers/CatalogCardContainer';
import CollectionDialogContainer from '../containers/CollectionDialogContainer';
import MapDialogContainer from '../containers/MapDialogContainer';
import Header from './Header';
import Footer from './Footer';

export default class Catalog extends React.Component {

  componentDidMount() {
    this.props.fetchCollections();
    this.props.fetchResources();
  }

  render() {
    console.log(this.props);
    const { error, loading } = this.props;
    const loadingMessage = <div className='loading-message'>Loading...</div>;

    if (error) {
      return <div>Error! {error.message}</div>;
    }

    if (loading) {
      return loadingMessage;
    }

    return (
      <div className="catalog-component">
        <Header />
        <div className='catalog'>
          <h1 className='mdc-typography--headline1'>Welcome to the holodeck!</h1>
          <button onClick={this.props.openMapDialog} style={{float: 'right'}}>show map</button>
          <CollectionDialogContainer />
          <MapDialogContainer />
            <div className='mdc-layout-grid'>
              <ul className='catalog-list mdc-layout-grid__inner'>
                {this.props.collections.result ? this.props.collections.result.map(collectionId =>
                  <li
                    className='mdc-layout-grid__cell mdc-layout-grid__cell--span-2'
                    key={collectionId}>
                    <CatalogCardContainer
                      collection={this.props.collections.entities.collectionsById[collectionId]}
                    />
                  </li>
                ) : loadingMessage}
              </ul>
          </div>
        </div>
        <Footer />
      </div>
    );
  }
}
