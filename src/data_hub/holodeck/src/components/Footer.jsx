import React from 'react';

export default class Footer extends React.Component {

  render() {
    return (
      <div className="footer-component">
        <div className="footer-component__legal">
          <ul className="legal-links">
            <li>
              <a href="https://tnris.org/site-policies#privacy-and-security-policy">Privacy/Security Policy</a>
            </li>
            <li>
              <a href="https://tnris.org/site-policies#accessibility-policy">Accessibility</a>
            </li>
            <li>
              <a href="http://www.twdb.texas.gov/home/open_records.asp">Open Records Request</a>
            </li>
            <li>
              <a href="http://www.twdb.texas.gov/home/compact_texan.asp">Compact with Texans</a>
            </li>
            <li>
              <a href="http://www.twdb.texas.gov/home/fraud.asp">Fraud &amp; Waste</a>
            </li>
            <li>
              <a href="https://www.tsl.texas.gov/trail/index.html">TRAIL</a>
            </li>
            <li>
              <a href="http://www.texas.gov">Texas.gov</a>
            </li>
            <li>
              <a href="http://www.twdb.texas.gov"><abbr title="Texas Water Development Board">TWDB</abbr></a>
            </li>
          </ul>
        </div>
        <div className="mdc-layout-grid">
          <div className="mdc-layout-grid__inner">
            <div className="mdc-layout-grid__cell--span-3-desktop mdc-layout-grid__cell--span-4-tablet  mdc-layout-grid__cell--span-2-phone">
              <h4>
                <a href="https://tnris.org/maps-and-data">Maps &amp; Data</a>
              </h4>
              <ul>
                <li><a href="https://data.tnris.org">Data</a></li>
                <li><a href="https://tnris.org/maps-and-data/applications-and-utilities">Applications and Utilities</a></li>
                <li><a href="https://tnris.org/research-distribution-center">Research &amp; Distribution (RDC)</a>
                  <ul className="footer-sub-menu">
                    <li><a href="https://tnris.org/research-distribution-center/historical-imagery-archive">Historical Imagery Archive</a></li>
                    <li><a href="https://tnris.org/research-distribution-center/custom-maps">Custom Maps</a></li>
                  </ul>
                </li>
              </ul>
            </div>
            <div className="mdc-layout-grid__cell--span-3-desktop mdc-layout-grid__cell--span-4-tablet  mdc-layout-grid__cell--span-2-phone">
              <h4>Programs</h4>
              <ul>
                <li><a href="https://tnris.org/stratmap">StratMap</a>
                  <ul className="footer-sub-menu">
                    <li><a href="https://tnris.org/stratmap/stratmap-contracts">StratMap Contracts</a></li>
                    <li><a href="https://tnris.org/stratmap/elevation-lidar">Elevation - Lidar </a></li>
                    <li><a href="https://tnris.org/stratmap/orthoimagery">Orthoimagery</a></li>
                  </ul>
                </li>
                <li><a href="https://tnris.org/training">Education &amp; Training</a>
                  <ul className="footer-sub-menu">
                    <li><a href="https://tnris.org/education/gis-mentorship">GIS Mentorships</a></li>
                    <li><a href="https://tnris.org/education/purchasers">Purchaser Resources</a></li>
                  </ul>
                </li>
                <li><a href="texas-imagery-service">Texas Imagery Service</a></li>
              </ul>
            </div>
            <div className="mdc-layout-grid__cell--span-3-desktop mdc-layout-grid__cell--span-4-tablet  mdc-layout-grid__cell--span-2-phone">
              <h4>Site</h4>
              <ul>
                <li><a href="https://tnris.org/about">About Us</a></li>
                <li><a href="https://tnris.org/contact">Contact Us</a></li>
                <li><a href="https://tnris.org/order-data">Order Data</a></li>
              </ul>
            </div>
            <div className="mdc-layout-grid__cell--span-3-desktop mdc-layout-grid__cell--span-4-tablet  mdc-layout-grid__cell--span-2-phone">
              <h4>Location</h4>
              <address>
                1700 N. Congress, Room B-40<br />
                Austin, Texas, 78701
              </address>
              <small>
                <a href="https://goo.gl/maps/RE5BC" target="_blank" rel="noopener noreferrer">
                  <i className="material-icons">open_in_new</i>View Map
                </a>
              </small>
              <p>
                <a href="tel:5124638337">
                  <i className="material-icons">phone</i>512-463-8337
                </a>
              </p>
            </div>
          </div>
        </div>
        <div className="footer-component__copyright">
          Content of this site © Texas Natural Resources Information System and Texas Water Development Board unless otherwise noted.
        </div>
      </div>
    );
  }
}
