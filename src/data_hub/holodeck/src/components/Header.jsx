import React from 'react';
import {MDCTopAppBar} from '@material/top-app-bar/index';
import {MDCDrawer} from "@material/drawer";
// import SortContainer from '../containers/SortContainer';

import tnrisGray from '../images/tnris_gray.png';
import tnrisWhite from '../images/tnris_white.png';
import tnrisFuego from '../images/tnris_fuego.png';

export default class Header extends React.Component {
  constructor(props) {
    super(props);
    this.handleOpenToolDrawer = this.handleOpenToolDrawer.bind(this);
    this.handleOpenOrderCartDialog = this.handleOpenOrderCartDialog.bind(this);
  }

  componentDidMount() {
    // this.menuDrawer = MDCDrawer.attachTo(document.querySelector('.menu-drawer'));
    this.toolDrawer = MDCDrawer.attachTo(document.querySelector('.tool-drawer'));

    this.topAppBarElement = document.querySelector('.mdc-top-app-bar');
    this.topAppBar = new MDCTopAppBar(this.topAppBarElement);

    // this.topAppBar.listen('MDCTopAppBar:nav', () => {
    //     this.menuDrawer.open = !this.menuDrawer.open;
    // });
  }

  handleOpenToolDrawer() {
    this.toolDrawer.open = !this.toolDrawer.open;
  }

  handleOpenOrderCartDialog() {
    this.props.openOrderCartDialog();
  }

  render() {
    let shoppingCartClass = "material-icons mdc-top-app-bar__navigation-icon";
    if (this.props.orders) {
      shoppingCartClass = Object.keys(this.props.orders).length !== 0 ? "material-icons mdc-top-app-bar__navigation-icon shopping-cart-full" : "material-icons mdc-top-app-bar__navigation-icon";
    }

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

    return (
      <header className="header-component mdc-top-app-bar mdc-top-app-bar--fixed">
        <div className="header-title mdc-top-app-bar__row">
          <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-start">
            <span className='header-title__tnris'>Texas Natural Resources Information System</span>
          </section>
          <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-end" role="toolbar">
            <a
              className='header-title__twdb' href="http://www.twdb.texas.gov/">
              A Division of the Texas Water Development Board
            </a>
          </section>
        </div>
        <div className="header-nav mdc-top-app-bar__row">
          <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-start">
            {/*<i className="material-icons mdc-top-app-bar__navigation-icon">menu</i>*/}
            <a href="https://tnris.org" className="mdc-top-app-bar__action-item tnris-logo-text">
              <img src={tnrisLogo} aria-label="TNRIS Logo" alt="TNRIS Logo" className="logo" />
              {/*TNRIS*/}
            </a>
            <span className="mdc-top-app-bar__title">Data Holodeck</span>
          </section>
          <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-end" role="toolbar">
            {/* <SortContainer /> */}
            <a onClick={this.handleOpenOrderCartDialog} className="mdc-top-app-bar__action-item">
              <i className={shoppingCartClass}>shopping_cart</i>
            </a>
            <a onClick={this.handleOpenToolDrawer} className="mdc-top-app-bar__action-item">
              <i className="material-icons mdc-top-app-bar__navigation-icon">search</i>
            </a>
          </section>
        </div>
      </header>
    );
  }
}
