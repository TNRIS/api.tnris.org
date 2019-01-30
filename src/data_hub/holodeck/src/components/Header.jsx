import React from 'react';
import {MDCTopAppBar} from '@material/top-app-bar/index';
import {MDCDrawer} from "@material/drawer";

import CollectionSearcherContainer from '../containers/CollectionSearcherContainer';
// import tnrisGray from '../images/tnris_gray.png';
// import tnrisWhite from '../images/tnris_white.png';
// import tnrisFuego from '../images/tnris_fuego.png';

export default class Header extends React.Component {
  constructor(props) {
    super(props);

    this.handleBack = this.handleBack.bind(this);
    this.handleOrderCartView = this.handleOrderCartView.bind(this);
    this.handleCatalogView = this.handleCatalogView.bind(this);
  }

  componentDidMount() {
    this.toolDrawer = MDCDrawer.attachTo(document.querySelector('.tool-drawer'));
    this.topAppBarElement = document.querySelector('.mdc-top-app-bar');
    this.topAppBar = new MDCTopAppBar(this.topAppBarElement);

    if (this.props.match.path === "/cart/") {
      this.props.closeToolDrawer();
      this.props.setViewOrderCart();
      this.props.clearPreviousUrl();
    }
  }

  handleBack() {
    if (this.props.previousUrl.includes('/catalog/')) {
      this.props.setViewCatalog();
      this.props.openToolDrawer();
      this.props.setUrl(this.props.previousUrl, this.props.history);
    }
    else if (this.props.previousUrl.includes('/collection/')) {
      const collectionUuid = this.props.previousUrl.replace('/collection/', '');
      this.props.setViewCollection();
      this.props.selectCollection(collectionUuid);
      if (this.props.collections[collectionUuid].template === 'tnris-download') {
        this.props.fetchCollectionResources(collectionUuid);
      }
      this.props.setUrl(this.props.previousUrl, this.props.history);
    }
    else {
      this.props.setViewCatalog();
      this.props.openToolDrawer();
      this.props.setUrl(this.props.previousUrl, this.props.history);
    }
  }

  handleOrderCartView() {
    if (window.location.pathname !== '/cart/') {
      this.props.clearSelectedCollection();
      this.props.closeToolDrawer();
      this.props.setViewOrderCart();
      this.props.setUrl('/cart/', this.props.history);
    }
  }

  handleCatalogView() {
    this.props.clearSelectedCollection();
    this.props.openToolDrawer();
    this.props.setViewCatalog();
    this.props.setUrl(this.props.catalogFilterUrl, this.props.history);
  }

  render() {
    let shoppingCartClass = "material-icons mdc-top-app-bar__navigation-icon";

    if (this.props.orders) {
      shoppingCartClass = Object.keys(this.props.orders).length !== 0 ?
      "material-icons mdc-top-app-bar__navigation-icon shopping-cart-full" :
      "material-icons mdc-top-app-bar__navigation-icon shopping-cart-empty";
    }

    let dismissClass = 'closed-drawer';

    if (this.props.toolDrawerStatus === 'open' && this.props.toolDrawerView === 'dismiss') {
      dismissClass = 'open-drawer';
    }

    const closedTitle = 'Open tool drawer';
    const openTitle = 'Close tool drawer';

    // let tnrisLogo;
    // switch(this.props.theme) {
    //   case 'light':
    //     tnrisLogo = tnrisGray;
    //     break;
    //   case 'dark':
    //     tnrisLogo = tnrisGray;
    //     break;
    //   case 'earth':
    //     tnrisLogo = tnrisWhite;
    //     break;
    //   case 'fuego':
    //     tnrisLogo = tnrisFuego;
    //     break;
    //   case 'vaporwave':
    //     tnrisLogo = tnrisWhite;
    //     break;
    //   case 'america':
    //     tnrisLogo = tnrisWhite;
    //     break;
    //   case 'hulk':
    //     tnrisLogo = tnrisWhite;
    //     break;
    //   case 'relax':
    //     tnrisLogo = tnrisWhite;
    //     break;
    //   default:
    //   tnrisLogo = tnrisGray;
    // }
    console.log(this.props);
    return (
        <header
          className={`header-component mdc-top-app-bar mdc-top-app-bar--fixed ${dismissClass}`}
          id="master-header">
          <div className="header-title mdc-top-app-bar__row">
            <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-start">
              <a className='header-title__tnris' href="https://tnris.org/" tabIndex="0" rel="noopener noreferrer" target="_blank">
                Texas Natural Resources Information System
              </a>
            </section>
            <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-end" role="toolbar">
              <a
                className='header-title__twdb' href="http://www.twdb.texas.gov/" tabIndex="0" rel="noopener noreferrer" target="_blank">
                A Division of the Texas Water Development Board
              </a>
            </section>
          </div>
          <div className={`header-nav mdc-top-app-bar__row`}>
            <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-start" role="toolbar">
              {this.props.view === 'orderCart' ?
                <a href="javascript:undefined" // eslint-disable-line
                  onClick={this.handleBack}
                  className="mdc-top-app-bar__action-item"
                  title="Back"
                  tabIndex="3"
                  >
                  <i className="material-icons mdc-top-app-bar__navigation-icon">arrow_back</i>
                </a> : ''}
               <CollectionSearcherContainer match={this.props.match} history={this.props.history} />
               {this.props.orders && Object.keys(this.props.orders).length !== 0 ?
                  <a href="javascript:undefined" // eslint-disable-line
                    onClick={this.handleOrderCartView}
                    className="mdc-top-app-bar__action-item"
                    title="View shopping cart"
                    tabIndex="3">
                    <i className={shoppingCartClass}>shopping_cart</i>
                  </a> : ''}
                {this.props.view === 'catalog' ?
                  <a href="javascript:undefined" // eslint-disable-line
                    onClick={this.props.toggleToolDrawerDisplay}
                    className="mdc-top-app-bar__action-item"
                    id="tools"
                    title={this.props.toolDrawerStatus === 'closed' ? closedTitle : openTitle}
                    tabIndex="3">
                    <i
                      className="material-icons mdc-top-app-bar__navigation-icon">
                      {this.props.toolDrawerStatus === 'closed' ? 'tune' : 'keyboard_arrow_right'}
                    </i>
                  </a> :
                  <a href="javascript:undefined" // eslint-disable-line
                    onClick={this.handleCatalogView}
                    className="mdc-top-app-bar__action-item"
                    id="tools"
                    title="Catalog"
                    tabIndex="3">
                    <i className="material-icons mdc-top-app-bar__navigation-icon">view_list</i>
                  </a>}
            </section>
          </div>
        </header>
    );
  }
}
