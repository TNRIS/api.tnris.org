import React from 'react';
import { Redirect } from 'react-router';

import CatalogCardContainer from '../containers/CatalogCardContainer';
import CollectionDialogContainer from '../containers/CollectionDialogContainer';
// import Drawer from './Drawer';
import Footer from './Footer';
import CollectionFilterMapDialogContainer from '../containers/CollectionFilterMapDialogContainer';
import HeaderContainer from '../containers/HeaderContainer';
import OrderCartDialogContainer from '../containers/OrderCartDialogContainer';
import ToolDrawer from './ToolDrawer';
// import { MDCDrawer } from "@material/drawer";
import loadingImage from '../images/loading.gif';

export default class Catalog extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      badUrlFlag: false,
      toolDrawerView: 'dismiss'
    }

    window.innerWidth >= 1052 ? this.state = {toolDrawerView:'dismiss'} : this.state = {toolDrawerView: 'modal'};
    this.handleResize = this.handleResize.bind(this);
  }

  handleResize() {
    window.innerWidth >= 1052 ? this.setState({toolDrawerView:'dismiss'}) : this.setState({toolDrawerView:'modal'});
  }

  componentDidMount() {
    this.props.fetchCollections();
    // this.props.fetchResources();
    this.props.fetchStoredShoppingCart();
    window.addEventListener("resize", this.handleResize);
    // this.toolDrawer = MDCDrawer.attachTo(document.querySelector('.catalog-component'));
  }

  componentWillUnmount() {
    window.removeEventListener("resize", this.handleResize);
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
    const mainContent = (
      <div className='main'>
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

    if (error) {
      return <div>Error! {error.message}</div>;
    }

    if (loading) {
      return loadingMessage;
    }

    if (this.state.badUrlFlag) {
      return <Redirect to='/404' />;
    }

    return (
      <div className="catalog-component">

        <ToolDrawer match={this.props.match}
          history={this.props.history}
          total={this.props.visibleCollections ? this.props.visibleCollections.length : 0}
          view={this.state.toolDrawerView}
        />

        {this.state.toolDrawerView === 'dismiss' ? <div className="mdc-drawer-app-content">{mainContent}</div> : mainContent}

      {/*this.state.toolDrawerView === 'dismiss' ?
        <div className="mdc-drawer-app-content">
          <main className='main-content' id='main-content'>{mainContent}</main>
        </div>
        : mainContent*/}

      </div>
    );
  }
}
