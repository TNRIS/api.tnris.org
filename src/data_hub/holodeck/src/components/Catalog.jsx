import React from 'react';
import { Redirect } from 'react-router';

import CatalogCardContainer from '../containers/CatalogCardContainer';
import CollectionDialogContainer from '../containers/CollectionDialogContainer';
// import Drawer from './Drawer';
import Footer from './Footer';
import CollectionFilterMapDialogContainer from '../containers/CollectionFilterMapDialogContainer';
import HeaderContainer from '../containers/HeaderContainer';
import OrderCartDialogContainer from '../containers/OrderCartDialogContainer';
import ToolDrawerContainer from '../containers/ToolDrawerContainer';
import loadingImage from '../images/loading.gif';

export default class Catalog extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      badUrlFlag: false
    }
  }

  componentDidMount() {
    this.props.fetchCollections();
    // this.props.fetchResources();
    this.props.fetchStoredShoppingCart();
  }

  componentDidUpdate() {
    if (this.props.collections && Object.keys(this.props.match.params).includes('collectionId')) {
      if (!Object.keys(this.props.collections).includes(this.props.match.params.collectionId)) {
        console.log(this.props.match.params.collectionId);
        this.setState({
          badUrlFlag: true
        });
      }
    }
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

    if (this.state.badUrlFlag) {
      return <Redirect to='/404' />;
    }

    const themedClass = "catalog-component " + this.props.theme + "-app-theme";

    return (
      <div className={themedClass}>
        {/*<Drawer />*/}
        <ToolDrawerContainer match={this.props.match} history={this.props.history} total={this.props.visibleCollections ? this.props.visibleCollections.length : 0} />
        <HeaderContainer />
        <div className='catalog'>
          <CollectionDialogContainer history={this.props.history} />
          <OrderCartDialogContainer />
          <CollectionFilterMapDialogContainer />
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
