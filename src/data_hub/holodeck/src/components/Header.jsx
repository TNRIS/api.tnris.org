import React from 'react';
import {MDCTopAppBar} from '@material/top-app-bar/index';
import {MDCDrawer} from "@material/drawer";

import tnrisGray from '../images/tnris_gray.png';
import tnrisWhite from '../images/tnris_white.png';
import tnrisFuego from '../images/tnris_fuego.png';

export default class Header extends React.Component {
  constructor(props) {
    super(props);

    this.handleCloseView = this.handleCloseView.bind(this);
    this.handleOpenOrderCartDialog = this.handleOpenOrderCartDialog.bind(this);
  }

  componentDidMount() {
    this.toolDrawer = MDCDrawer.attachTo(document.querySelector('.tool-drawer'));
    this.topAppBarElement = document.querySelector('.mdc-top-app-bar');
    this.topAppBar = new MDCTopAppBar(this.topAppBarElement);
  }

  handleOpenOrderCartDialog() {
    this.props.openOrderCartDialog();
  }

  handleCloseView() {
    this.props.closeCollectionDialog();
    this.props.clearSelectedCollection();
    this.props.closeOrderCartDialog();
    if (this.props.previousUrl.includes('/collection/')) {
      this.props.setUrl('/', this.props.history);
    }
    else {
      this.props.setUrl(this.props.previousUrl, this.props.history);
    }
  }

  render() {
    let shoppingCartClass = "material-icons mdc-top-app-bar__navigation-icon";

    if (this.props.orders) {
      shoppingCartClass = Object.keys(this.props.orders).length !== 0 ?
      "material-icons mdc-top-app-bar__navigation-icon shopping-cart-full" :
      "material-icons mdc-top-app-bar__navigation-icon";
    }

    let dismissClass = 'closed-drawer';

    if (this.props.status === 'open' && this.props.view === 'dismiss') {
      dismissClass = 'open-drawer';
    }

    const closedTitle = 'Open Tool Drawer';
    const openTitle = 'Close Tool Drawer';

    let tnrisLogo;
    switch(this.props.theme) {
      case 'light':
        tnrisLogo = tnrisGray;
        break;
      case 'dark':
        tnrisLogo = tnrisGray;
        break;
      case 'earth':
        tnrisLogo = tnrisWhite;
        break;
      case 'fuego':
        tnrisLogo = tnrisFuego;
        break;
      case 'vaporwave':
        tnrisLogo = tnrisWhite;
        break;
      case 'america':
        tnrisLogo = tnrisWhite;
        break;
      case 'hulk':
        tnrisLogo = tnrisWhite;
        break;
      case 'relax':
        tnrisLogo = tnrisWhite;
        break;
      default:
      tnrisLogo = tnrisGray;
    }
    // console.log(this.props);
    return (
        <header
          className={`header-component mdc-top-app-bar mdc-top-app-bar--fixed ${dismissClass}`}
          id="master-header">
          <div className="header-title mdc-top-app-bar__row">
            <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-start">
              <span className='header-title__tnris'>Texas Natural Resources Information System</span>
            </section>
            <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-end" role="toolbar">
              <a
                className='header-title__twdb' href="http://www.twdb.texas.gov/" tabIndex="0">
                A Division of the Texas Water Development Board
              </a>
            </section>
          </div>
          <div className="header-nav mdc-top-app-bar__row">
            <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-start">
              <a href="https://tnris.org" className="mdc-top-app-bar__action-item tnris-logo-text" tabIndex="0">
                <img src={tnrisLogo} aria-label="TNRIS Logo" alt="TNRIS Logo" className="logo" />
              </a>
              <span className="mdc-top-app-bar__title">Data Holodeck</span>
            </section>
            <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-end" role="toolbar">
              {this.props.selectedCollection !== null || this.props.showOrderCartDialog ?
                <div onClick={this.handleCloseView} className="mdc-top-app-bar__action-item" tabIndex="0">
                  <i className="material-icons mdc-top-app-bar__navigation-icon">home</i>
                </div> : ''}
              <div onClick={this.handleOpenOrderCartDialog} className="mdc-top-app-bar__action-item" tabIndex="0">
                <i className={shoppingCartClass}>shopping_cart</i>
              </div>
              <div
                onClick={this.props.handler}
                className="mdc-top-app-bar__action-item"
                id="tools" title={this.props.status === 'closed' ? closedTitle : openTitle}
                tabIndex="0">
                <i
                  className="material-icons mdc-top-app-bar__navigation-icon">
                  {this.props.status === 'closed' ? 'search' : 'keyboard_arrow_right'}
                </i>
              </div>
            </section>
          </div>
        </header>
    );
  }
}
