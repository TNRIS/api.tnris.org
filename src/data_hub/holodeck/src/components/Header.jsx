import React from 'react';
import {MDCTopAppBar} from '@material/top-app-bar/index';
import NotificationBadge from 'react-notification-badge';
import {Effect} from 'react-notification-badge';

// global sass breakpoint variables to be used in js
import breakpoints from '../sass/_breakpoints.scss';

import CollectionSearcherContainer from '../containers/CollectionSearcherContainer';

import tnrisLogo from '../images/tnris_logo.svg';

export default class Header extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      tnrisTitle: 'Texas Natural Resources Information System',
      twdbTitle: 'A Division of the Texas Water Development Board'
    }

    this.handleOrderCartView = this.handleOrderCartView.bind(this);
    this.handleCatalogView = this.handleCatalogView.bind(this);
    this.handleResize = this.handleResize.bind(this);
    this.handleKeyPress = this.handleKeyPress.bind(this);
  }

  componentDidMount() {
    this.topAppBarElement = document.querySelector('.mdc-top-app-bar');
    this.topAppBar = new MDCTopAppBar(this.topAppBarElement);

    if (this.props.location.pathname === "/cart/") {
      this.props.setViewOrderCart();
      this.props.clearPreviousUrl();
    }

    window.addEventListener("resize", this.handleResize);
    this.handleResize();
  }

  componentWillUnmount() {
    window.removeEventListener("resize", this.handleResize);
  }

  handleResize() {
    if (window.innerWidth < parseInt(breakpoints.phone, 10)) {
      this.setState({
        tnrisTitle: '',
        twdbTitle: 'A TWDB Division'
      })
    }
    else {
      this.setState({
        tnrisTitle: 'Texas Natural Resources Information System',
        twdbTitle: 'A Division of the Texas Water Development Board'
      })
    }
  }

  handleOrderCartView() {
    if (window.location.pathname !== '/cart/') {
      this.props.setViewOrderCart();
      this.props.setUrl('/cart/');
    }
  }

  handleCatalogView() {
    this.props.setViewCatalog();
    this.props.setUrl(this.props.catalogFilterUrl);
  }

  handleKeyPress (e, ref) {
    if (e.keyCode === 13 || e.keyCode === 32) {
      if (ref === 'cart') {
        this.handleOrderCartView();
      }
      else if (ref === 'toolDrawer') {
        this.props.handleToolDrawerDisplay();
      }
      else if (ref === 'catalog') {
        this.handleCatalogView();
      }
    }
  }

  render() {

    const tablet = parseInt(breakpoints.tablet, 10);

    let drawerStatusClass = 'closed-drawer';
    // if (this.props.view === 'catalog' &&
    //   this.props.toolDrawerVariant === 'dismissible' &&
    //   this.props.toolDrawerStatus === 'open') {
    //   drawerStatusClass = 'open-drawer';
    // }

    const shoppingCartCountBadge = Object.keys(this.props.orders).length > 0 ? (
      <NotificationBadge count={Object.keys(this.props.orders).length} effect={Effect.SCALE} frameLength={30}/>
    ) : '';

    const filters = ['filter', 'geo', 'sort', 'range'];
    const toolDrawerNotification = filters.map(x => this.props.location.pathname.includes(x) ?
      (<NotificationBadge key={x} label='!' count={1} frameLength={30}/>) : '');

    const appTitle = window.innerWidth >= tablet ? (
          <section id="app-title" className="mdc-top-app-bar__section mdc-top-app-bar__section--align-start" role="toolbar">
            <a
              className="custom-font mdc-typography mdc-typography--headline5"
              title="View Catalog"
              onClick={this.handleCatalogView}
              onKeyDown={(e) => this.handleKeyPress(e, 'catalog')}
              tabIndex="3">
                Data Catalog
            </a>
          </section>) : '';

    return (
        <header
          className={`header-component mdc-top-app-bar mdc-top-app-bar--fixed`}
          id="master-header">
          <div className="header-title mdc-top-app-bar__row">
            <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-start">
              <img className="tnris-logo" src={tnrisLogo} alt="" />
              <a className='header-title__tnris title-size' href="https://tnris.org/" tabIndex="0">
                {this.state.tnrisTitle}
              </a>
            </section>
            <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-end">
              <a className='header-title__twdb title-size' href="http://www.twdb.texas.gov/" tabIndex="0">
                {this.state.twdbTitle}
              </a>
            </section>
          </div>
          <div className={`header-nav mdc-top-app-bar__row ${drawerStatusClass}`}>
            {appTitle}
            <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-end" role="toolbar">
              <CollectionSearcherContainer />
              {this.props.orders && Object.keys(this.props.orders).length !== 0 ?
                 <div className="shopping-cart-icon nav-button">
                   {shoppingCartCountBadge}
                  <a
                    onClick={this.handleOrderCartView}
                    onKeyDown={(e) => this.handleKeyPress(e, 'cart')}
                    className="material-icons mdc-top-app-bar__navigation-icon"
                    title="View shopping cart"
                    tabIndex="3">
                    shopping_cart
                  </a>
                </div> : ''}
                {this.props.view === 'catalog' ?
                  <div className="tool-drawer-icon nav-button">
                    {toolDrawerNotification}
                    <a
                      onClick={this.props.handleToolDrawerDisplay}
                      onKeyDown={(e) => this.handleKeyPress(e, 'toolDrawer')}
                      className="material-icons mdc-top-app-bar__navigation-icon"
                      id="tools"
                      title={this.props.toolDrawerStatus === 'closed' ? 'Open tool drawer' : 'Close tool drawer'}
                      tabIndex="3">
                      {/*{this.props.toolDrawerVariant === 'dismissible' ?
                        this.props.toolDrawerStatus === 'closed' ? 'menu' : 'tune' : 'tune'}*/}
                        tune
                    </a>
                  </div> : ''}
            </section>
          </div>
        </header>
    );
  }
}
