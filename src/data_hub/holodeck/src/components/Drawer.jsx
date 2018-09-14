import React from 'react';

import tnrisLogo from '../images/tnris.png';
import twdbLogo from '../images/twdb_splash.png';

export default class Drawer extends React.Component {

  render() {
    return (
      <div className="drawer-component">
        <aside className="mdc-drawer mdc-drawer--modal">
          <div className="mdc-drawer__header">
            <h3 className="mdc-drawer__title">Links</h3>
            <h6 className="mdc-drawer__subtitle">to tnris.org</h6>
          </div>
          <div className="mdc-drawer__content">
            <nav className="mdc-list">
              <a className="mdc-list-item" href="https://tnris.org/maps-and-data" aria-hidden="true">
                <i className="material-icons mdc-list-item__graphic" aria-hidden="true">inbox</i>Maps &amp; Data
              </a>
              <a className="mdc-list-item" href="https://tnris.org/geographic-information-office">
                <i className="material-icons mdc-list-item__graphic" aria-hidden="true">send</i>Geographic Information Office
              </a>

              <h3 className="mdc-drawer__title">Programs</h3>
              <a href="https://tnris.org/stratmap">
                <h6 className="mdc-list-group__subheader">Strategic Mapping Program</h6>
                <h6 className="mdc-list-group__subheader">StratMap</h6>
              </a>
              <a className="mdc-list-item" href="https://tnris.org/stratmap/stratmap-contracts">
                <i className="material-icons mdc-list-item__graphic" aria-hidden="true">send</i>StratMap Contracts
              </a>
              <a className="mdc-list-item" href="https://tnris.org/stratmap/elevation-lidar">
                <i className="material-icons mdc-list-item__graphic" aria-hidden="true">send</i>Elevation- Lidar
              </a>
              <a className="mdc-list-item" href="https://tnris.org/stratmap/orthoimagery">
                <i className="material-icons mdc-list-item__graphic" aria-hidden="true">send</i>Orthoimagery
              </a>

              <a href="https://tnris.org/research-distribution-center">
                <h6 className="mdc-list-group__subheader">Research and Distribution Center (RDC)</h6>
              </a>
              <a className="mdc-list-item" href="https://tnris.org/research-distribution-center/historical-imagery-archive">
                <i className="material-icons mdc-list-item__graphic" aria-hidden="true">send</i>Historical Imagery Archive
              </a>
              <a className="mdc-list-item" href="https://tnris.org/research-distribution-center/custom-maps">
                <i className="material-icons mdc-list-item__graphic" aria-hidden="true">send</i>Custom Maps
              </a>

              <a href="https://tnris.org/education">
                <h6 className="mdc-list-group__subheader">Education and Training</h6>
              </a>
              <a className="mdc-list-item" href="https://tnris.org/education/gis-mentorship">
                <i className="material-icons mdc-list-item__graphic" aria-hidden="true">send</i>GIS Mentorships
              </a>
              <a className="mdc-list-item" href="https://tnris.org/education/purchasers">
                <i className="material-icons mdc-list-item__graphic" aria-hidden="true">send</i>Purchaser Resources
              </a>

              <a href="https://tnris.org/texas-imagery-service">
                <h6 className="mdc-list-group__subheader">Texas Imagery Service</h6>
              </a>


              <hr className="mdc-list-divider" />

              <a className="mdc-list-item" href="https://tnris.org/about">
                <i className="material-icons mdc-list-item__graphic" aria-hidden="true">drafts</i>About
              </a>
              <a className="mdc-list-item" href="https://tnris.org/contact">
                <i className="material-icons mdc-list-item__graphic" aria-hidden="true">drafts</i>Contact Us
              </a>
              <a className="mdc-list-item" href="https://tnris.org">
                <img src={tnrisLogo} className="mdc-list-item__graphic" aria-hidden="true" />tnris.org
              </a>
              <a className="mdc-list-item" href="http://www.twdb.texas.gov/">
                <img src={twdbLogo} className="mdc-list-item__graphic" aria-hidden="true" />twdb.texas.gov
              </a>

            </nav>
          </div>
        </aside>
        <div className="mdc-drawer-scrim"></div>
      </div>
    );
  }
}
