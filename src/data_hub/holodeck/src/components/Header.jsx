import React from 'react';
import {MDCTopAppBar} from '@material/top-app-bar/index';
import {MDCDrawer} from "@material/drawer";
import NotificationBadge from 'react-notification-badge';
import {Effect} from 'react-notification-badge';

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

    else if (Object.keys(this.props.match.params).includes('collectionId')) {
      const collectionUuid = this.props.match.params['collectionId'];
      this.props.closeToolDrawer();
      this.props.setViewCollection();
      this.props.selectCollection(collectionUuid);
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
    if (this.props.toolDrawerView === 'dismiss' && this.props.showToolDrawerInCatalogView) {
      this.props.openToolDrawer();
    }
    this.props.clearSelectedCollection();
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

    const shoppingCartCountBadge = Object.keys(this.props.orders).length > 0 ? (
      <NotificationBadge count={Object.keys(this.props.orders).length} effect={Effect.SCALE} frameLength={30}/>
    ) : '';

    const filters = ['filter', 'geo', 'sort', 'range'];
    const toolDrawerNotification = this.props.toolDrawerStatus === 'closed' && filters.map(x => this.props.match.url.includes(x) ? (
      <NotificationBadge key={x} label='!' count={1} frameLength={30}/>
    ) : '');

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

    return (
        <header
          className={`header-component mdc-top-app-bar mdc-top-app-bar--fixed`}
          id="master-header">
          <div className="header-title mdc-top-app-bar__row">
            <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-start">
              <a className='header-title__tnris' href="https://tnris.org/" tabIndex="0">
                Texas Natural Resources Information System
              </a>
            </section>
            <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-end" role="toolbar">
              <a
                className='header-title__twdb' href="http://www.twdb.texas.gov/" tabIndex="0">
                A Division of the Texas Water Development Board
              </a>
            </section>
          </div>
          <div className={`header-nav mdc-top-app-bar__row ${dismissClass}`}>
            <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-start" role="toolbar">
              {/*<a href="https://tnris.org" className="mdc-top-app-bar__action-item tnris-logo-text">
                <img src={tnrisLogo} aria-label="TNRIS Logo" alt="TNRIS Logo" className="logo" />
              </a>
              <span className="mdc-top-app-bar__title">Data Holodeck</span>*/}
              {/*{this.props.view === 'orderCart' ?
                <a
                  onClick={this.handleBack}
                  className="mdc-top-app-bar__action-item"
                  title="Back"
                  >
                  <i className="material-icons mdc-top-app-bar__navigation-icon">arrow_back</i>
                </a> : ''}*/}
              <a
                onClick={this.handleCatalogView}
                className="material-icons mdc-top-app-bar__navigation-icon"
                id="tools"
                title="Catalog">
                view_comfy
              </a>
               <CollectionSearcherContainer match={this.props.match} history={this.props.history} />
               {this.props.orders && Object.keys(this.props.orders).length !== 0 ?
                  <a
                    onClick={this.handleOrderCartView}
                    className="mdc-top-app-bar__action-item"
                    title="View shopping cart">
                    <div>
                      {shoppingCartCountBadge}
                      <i className={shoppingCartClass}>shopping_cart</i>
                    </div>
                  </a> : ''}
                {this.props.view === 'catalog' ?
                  <a
                    onClick={this.props.toggleToolDrawerDisplay}
                    className="material-icons mdc-top-app-bar__navigation-icon"
                    id="tools"
                    title={this.props.toolDrawerStatus === 'closed' ? 'Open tool drawer' : 'Close tool drawer'}>
                    {this.props.toolDrawerView === 'dismiss' ?
                      this.props.toolDrawerStatus === 'closed' ?
                        'tune' : 'keyboard_arrow_right' : 'tune'}
                  </a> : null}
            </section>
          </div>
        </header>
    );
  }
}
