import React from 'react';
import {MDCTopAppBar} from '@material/top-app-bar/index';
import NotificationBadge from 'react-notification-badge';
import {Effect} from 'react-notification-badge';

// global sass breakpoint variables to be used in js
import breakpoints from '../sass/_breakpoints.scss';

import CollectionSearcherContainer from '../containers/CollectionSearcherContainer';

export default class Header extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      tnrisTitle: 'Texas Natural Resources Information System',
      twdbTitle: 'A Division of the Texas Water Development Board',
      collapse: false
    }

    this.handleOrderCartView = this.handleOrderCartView.bind(this);
    this.handleCatalogView = this.handleCatalogView.bind(this);
    this.handleResize = this.handleResize.bind(this);
  }

  componentDidMount() {
    this.topAppBarElement = document.querySelector('.mdc-top-app-bar');
    this.topAppBar = new MDCTopAppBar(this.topAppBarElement);

    if (this.props.location.pathname === "/cart/") {
      this.props.setViewOrderCart();
      this.props.clearPreviousUrl();
    }
    window.addEventListener("resize", this.handleResize);
  }

  componentWillUnmount() {
    window.removeEventListener("resize", this.handleResize);
  }

  handleResize() {
    if (window.innerWidth < parseInt(breakpoints.phone, 10)) {
      this.setState({
        tnrisTitle: 'TNRIS',
        twdbTitle: 'A TWDB Division',
        collapse: true
      })
    }
    else {
      this.setState({
        tnrisTitle: 'Texas Natural Resources Information System',
        twdbTitle: 'A Division of the Texas Water Development Board',
        collapse: false
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

  render() {
    console.log(window.innerWidth);

    const phone = parseInt(breakpoints.phone, 10);
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
            <div className="mdc-typography mdc-typography--headline5 no-style"
              onClick={this.handleCatalogView}
              title="Data Catalog">
              Data Catalog
            </div>
          </section>) : '';

    const alignEndSearch = window.innerWidth >= tablet ? (
      <CollectionSearcherContainer />) : '';

    const alignStartSearch = window.innerWidth >= phone && window.innerWidth < tablet ? (
      <div className="search-container">
        <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-start" role="toolbar">
          <CollectionSearcherContainer />
        </section>
      </div>) : '';

    const clickToSearch = () => {
      console.log('you clicked');
      const showHide = document.getElementById("click-to-search");
      const searchIcon = document.getElementById("search-icon");
      searchIcon ? searchIcon.parentNode.removeChild(searchIcon) : '';
      showHide.classList.contains("hidden") ? showHide.className = "show" : showHide.className = "hidden";
    };

    const collapseSearch = this.state.collapse === true ? (
      <div className="search-container">
        <section id="collapsed-search" className="mdc-top-app-bar__section mdc-top-app-bar__section--align-start" role="toolbar">
          <button className="collapse-button mdc-icon-button material-icons" onClick={clickToSearch} title="Search">
            search
          </button>
          <div id="click-to-search" className="hidden search-function">
            <CollectionSearcherContainer />
          </div>
        </section>
      </div>) : '';

    return (
        <header
          className={`header-component mdc-top-app-bar mdc-top-app-bar--fixed`}
          id="master-header">
          <div className="header-title mdc-top-app-bar__row">
            <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-start">
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
            {alignStartSearch}
            {collapseSearch}
            <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-end" role="toolbar">
              {alignEndSearch}
              {this.props.orders && Object.keys(this.props.orders).length !== 0 ?
                 <div className="shopping-cart-icon nav-button">
                   {shoppingCartCountBadge}
                  <a
                    onClick={this.handleOrderCartView}
                    className="material-icons mdc-top-app-bar__navigation-icon"
                    title="View shopping cart">
                    shopping_cart
                  </a>
                </div> : ''}
                {this.props.view === 'catalog' ?
                  <div className="tool-drawer-icon nav-button">
                    {toolDrawerNotification}
                    <a
                      onClick={this.props.handleToolDrawerDisplay}
                      className="material-icons mdc-top-app-bar__navigation-icon"
                      id="tools"
                      title={this.props.toolDrawerStatus === 'closed' ? 'Open tool drawer' : 'Close tool drawer'}>
                      {/*{this.props.toolDrawerVariant === 'dismissible' ?
                        this.props.toolDrawerStatus === 'closed' ? 'menu' : 'tune' : 'tune'}*/}
                        tune
                    </a>
                  </div> :
                  <div className="catalog-icon nav-button">
                    <a
                      onClick={this.handleCatalogView}
                      className="material-icons mdc-top-app-bar__navigation-icon"
                      id="tools"
                      title="View Catalog">
                      view_comfy
                    </a>
                  </div>}
            </section>
          </div>
        </header>
    );
  }
}
