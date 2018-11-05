import React from 'react';

import CatalogCardContainer from '../containers/CatalogCardContainer';
import CollectionDialogContainer from '../containers/CollectionDialogContainer';
import Drawer from './Drawer';
import Footer from './Footer';
import HeaderContainer from '../containers/HeaderContainer';
// import MapDialogContainer from '../containers/MapDialogContainer';
import OrderCartDialogContainer from '../containers/OrderCartDialogContainer';
import ToolDrawer from './ToolDrawer';
import loadingImage from '../images/loading.gif';

export default class Catalog extends React.Component {

  componentDidMount() {
    this.props.fetchCollections();
    this.props.fetchResources();
    this.props.fetchStoredShoppingCart();
  }

  render() {
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
        <Drawer />
        <ToolDrawer match={this.props.match} history={this.props.history} />
        <HeaderContainer />
        <div className='catalog'>
          {/* <button onClick={this.props.openMapDialog}>show map</button> */}
          <CollectionDialogContainer history={this.props.history} />
          <OrderCartDialogContainer />
          {/* <MapDialogContainer /> */}
          <ul className='catalog-list mdc-image-list mdc-image-list--with-text-protection'>
            {this.props.visibleCollections ? this.props.visibleCollections.map(collectionId =>
              <CatalogCardContainer collection={this.props.collections[collectionId]} key={collectionId} match={this.props.match} history={this.props.history} />
            ) : loadingMessage}
          </ul>
        </div>
        <Footer />
      </div>
    );
  }
}
