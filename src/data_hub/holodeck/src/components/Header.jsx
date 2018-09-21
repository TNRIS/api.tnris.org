import React from 'react';
import {MDCTopAppBar} from '@material/top-app-bar/index';
import {MDCDrawer} from "@material/drawer";
import SortContainer from '../containers/SortContainer';
import CollectionFilterContainer from '../containers/CollectionFilterContainer';

import tnrisLogo from '../images/tnris.png';

export default class Header extends React.Component {

  componentDidMount() {
    this.menuDrawer = MDCDrawer.attachTo(document.querySelector('.menu-drawer'));
    this.toolDrawer = MDCDrawer.attachTo(document.querySelector('.tool-drawer'));

    this.topAppBarElement = document.querySelector('.mdc-top-app-bar');
    this.topAppBar = new MDCTopAppBar(this.topAppBarElement);

    this.topAppBar.listen('MDCTopAppBar:nav', () => {
        this.menuDrawer.open = !this.menuDrawer.open;
        this.toolDrawer.open = !this.toolDrawer.open;
    });
  }

  render() {
    return (
      <header className="header-component mdc-top-app-bar">
        <div className="header-title mdc-top-app-bar__row">
          <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-start">
            <span className='header-title__tnris'>Texas Natural Resources Information System</span>
          </section>
          <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-end" role="toolbar">
            <a className='header-title__twdb' href="http://www.twdb.texas.gov/">A Division of the Texas Water Development Board</a>
          </section>
        </div>
        <div className="header-nav mdc-top-app-bar__row">
          <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-start">
            <i className="material-icons mdc-top-app-bar__navigation-icon">menu</i>
            <a href="https://tnris.org" className="mdc-top-app-bar__action-item">
              <img src={tnrisLogo} aria-label="TNRIS Logo" alt="TNRIS Logo" className="logo" />
            </a>
            <span className="mdc-top-app-bar__title">Data Holodeck</span>
            <div className='header-nav__buttons'>
              <CollectionFilterContainer />
            </div>
          </section>
          <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-end" role="toolbar">
            <SortContainer />
            <i className="material-icons mdc-top-app-bar__navigation-icon">menu</i>
          </section>
        </div>
      </header>
    );
  }
}
