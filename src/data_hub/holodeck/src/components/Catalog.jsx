import React from 'react';

import CatalogCardContainer from '../containers/CatalogCardContainer';
import CollectionDialogContainer from '../containers/CollectionDialogContainer';
import MapDialogContainer from '../containers/MapDialogContainer';
import CollectionFilterContainer from '../containers/CollectionFilterContainer';
import Header from './Header';
import Footer from './Footer';

import loadingImage from '../images/loading.jpg';

export default class Catalog extends React.Component {
  constructor(props) {
    super(props);
  }

  componentDidMount() {
    this.props.fetchCollections();
    this.props.fetchResources();
  }

  componentWillReceiveProps(nextProps) {
    console.log(nextProps);
  }

  render() {
    console.log(this.props.visibleCollections);
    const { error, loading } = this.props;
    const loadingMessage = (
        <div className="catalog-component__loading">
          <img src={loadingImage} alt="Holodeck Loading..." className="holodeck-loading-image" />
        </div>
      );

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
          <CollectionFilterContainer />
          <button onClick={this.props.openMapDialog} style={{float: 'right'}}>show map</button>
          <CollectionDialogContainer />
          <MapDialogContainer />
            <div className='mdc-layout-grid'>
              <ul className='catalog-list mdc-layout-grid__inner'>
                {this.props.collections ? this.props.visibleCollections.map(collectionId =>
                  <li
                    className='mdc-layout-grid__cell mdc-layout-grid__cell--span-2'
                    key={collectionId}>
                    <CatalogCardContainer
                      collection={this.props.collections[collectionId]}
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
