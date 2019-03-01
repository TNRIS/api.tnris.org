import React from 'react';
import {MDCTopAppBar} from '@material/top-app-bar/index';
import NotificationBadge from 'react-notification-badge';
import {Effect} from 'react-notification-badge';

import CollectionSearcherContainer from '../containers/CollectionSearcherContainer';

export default class Header extends React.Component {
  constructor(props) {
    super(props);
    // window.innerWidth > 1050 ? this.state = {
    //   tnrisTitle: 'Texas Natural Resources Information System',
    //   twdbTitle: 'A Division of the Texas Water Development Board'
    // } : this.state = {
    //   tnrisTitle: 'Texas Natural Resources Information System',
    //   twdbTitle: 'A TWDB Division'
    // };

    this.handleOrderCartView = this.handleOrderCartView.bind(this);
    this.handleCatalogView = this.handleCatalogView.bind(this);
    // this.handleResize = this.handleResize.bind(this);
  }

  componentDidMount() {
    this.topAppBarElement = document.querySelector('.mdc-top-app-bar');
    this.topAppBar = new MDCTopAppBar(this.topAppBarElement);

    if (this.props.location.pathname === "/cart/") {
      this.props.setViewOrderCart();
      this.props.clearPreviousUrl();
    }

    // window.addEventListener("resize", this.handleResize);
  }

  // componentWillUnmount() {
  //   window.removeEventListener("resize", this.handleResize);
  // }

  // handleResize() {
  //   if (window.innerWidth > 1050) {
  //     this.setState({
  //       tnrisTitle: 'Texas Natural Resources Information System',
  //       twdbTitle: 'A Division of the Texas Water Development Board'
  //     })
  //   }
  //   else {
  //     this.setState({
  //       twdbTitle: 'A TWDB Division'
  //     });
  //   }
  // }

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

    const twdbHeader = "A Division of the Texas Water Development Board";

    return (
        <header
          className={`header-component mdc-top-app-bar mdc-top-app-bar--fixed`}
          id="master-header">
          <div className="header-title mdc-top-app-bar__row">
            <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-start">
              {/*<img src="../images/tnris_logo_white.png" className="responsive-image" alt="" />*/}
              <a className='header-title__tnris' href="https://tnris.org/" tabIndex="0">
                {/*this.state.tnrisTitle*/}
                Texas Natural Resources Information System
              </a>
            </section>
            <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-end" role="toolbar">
              <a id="twdb-header-text" className='header-title__twdb' href="http://www.twdb.texas.gov/" tabIndex="0">
                {twdbHeader}
              </a>
            </section>
          </div>
          <div className={`header-nav mdc-top-app-bar__row ${drawerStatusClass}`}>
            <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-end" role="toolbar">

              <CollectionSearcherContainer />
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
