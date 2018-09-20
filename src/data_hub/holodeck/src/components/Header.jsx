import React from 'react';

import { MDCTopAppBar } from '@material/top-app-bar/index';

import SortContainer from '../containers/SortContainer';
import CollectionFilterContainer from '../containers/CollectionFilterContainer';

import tnrisLogo from '../images/tnris.png'
import twdbLogo from '../images/twdb_splash.png'

export default class Header extends React.Component {

  componentDidMount() {
    this.topAppBarElement = document.querySelector('.mdc-top-app-bar');
    this.topAppBar = new MDCTopAppBar(this.topAppBarElement);
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
              <SortContainer />
              <CollectionFilterContainer />
            </div>
          </section>
          <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-end" role="toolbar">

            <a href="http://www.twdb.texas.gov/" className="mdc-top-app-bar__action-item">
              <img src={twdbLogo} aria-label="TWDB Logo" alt="TWDB Logo" className="logo" />
            </a>
          </section>
        </div>
      </header>
    );
  }
}
