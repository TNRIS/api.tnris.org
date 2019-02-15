import React from 'react';

export default class Footer extends React.Component {

  render() {
    console.log(this.props);
    let drawerStatusClass = 'closed-drawer';
    if (this.props.view === 'catalog' &&
      this.props.toolDrawerVariant === 'dismissible' &&
      this.props.toolDrawerStatus === 'open') {
      drawerStatusClass = 'open-drawer';
    }

    return (
      <div className={`footer-component ${drawerStatusClass}`} id='master-footer'>
        <div className="footer-component__legal">
          <ul className="legal-links">
            <li>
              <a href="https://tnris.org/site-policies#privacy-and-security-policy" tabIndex="0">
                Privacy/Security Policy
              </a>
            </li>
            <li>
              <a href="https://tnris.org/site-policies#accessibility-policy" tabIndex="0">
                Accessibility
              </a>
            </li>
            <li>
              <a href="http://www.twdb.texas.gov/home/open_records.asp" tabIndex="0">
                Open Records Request
              </a>
            </li>
            <li>
              <a href="http://www.twdb.texas.gov/home/compact_texan.asp" tabIndex="0">
                Compact with Texans
              </a>
            </li>
            <li>
              <a href="http://www.twdb.texas.gov/home/fraud.asp" tabIndex="0">
                Fraud &amp; Waste
              </a>
            </li>
            <li>
              <a href="https://www.tsl.texas.gov/trail/index.html" tabIndex="0">TRAIL</a>
            </li>
            <li>
              <a href="http://www.texas.gov" tabIndex="0">Texas.gov</a>
            </li>
            <li>
              <a href="http://www.twdb.texas.gov" tabIndex="0">
                <abbr title="Texas Water Development Board">TWDB</abbr>
              </a>
            </li>
          </ul>
        </div>
        <div className="mdc-layout-grid">
          <div className="mdc-layout-grid__inner">
            <div className={`mdc-layout-grid__cell--span-3-desktop
              mdc-layout-grid__cell--span-4-tablet  mdc-layout-grid__cell--span-2-phone`}>
              <h4>
                <a href="https://tnris.org/maps-and-data" tabIndex="0">Maps &amp; Data</a>
              </h4>
              <ul>
                <li><a href="https://data.tnris.org" tabIndex="0">Data</a></li>
                <li>
                  <a href="https://tnris.org/maps-and-data/applications-and-utilities" tabIndex="0">
                    Applications and Utilities
                  </a>
                </li>
                <li>
                  <a href="https://tnris.org/research-distribution-center" tabIndex="0">
                    Research &amp; Distribution (RDC)
                  </a>
                  <ul className="footer-sub-menu">
                    <li>
                      <a
                        href="https://tnris.org/research-distribution-center/historical-imagery-archive"
                        tabIndex="0">
                        Historical Imagery Archive
                      </a>
                    </li>
                    <li>
                      <a href="https://tnris.org/research-distribution-center/custom-maps" tabIndex="0">
                        Custom Maps
                      </a>
                    </li>
                  </ul>
                </li>
              </ul>
            </div>
            <div className={`mdc-layout-grid__cell--span-3-desktop
              mdc-layout-grid__cell--span-4-tablet  mdc-layout-grid__cell--span-2-phone`}>
              <h4>Programs</h4>
              <ul>
                <li><a href="https://tnris.org/stratmap" tabIndex="0">StratMap</a>
                  <ul className="footer-sub-menu">
                    <li>
                      <a href="https://tnris.org/stratmap/stratmap-contracts" tabIndex="0">
                        StratMap Contracts
                      </a>
                    </li>
                    <li>
                      <a href="https://tnris.org/stratmap/elevation-lidar" tabIndex="0">
                        Elevation - Lidar
                      </a>
                    </li>
                    <li>
                      <a href="https://tnris.org/stratmap/orthoimagery" tabIndex="0">
                        Orthoimagery
                      </a>
                    </li>
                  </ul>
                </li>
                <li><a href="https://tnris.org/training" tabIndex="0">Education &amp; Training</a>
                  <ul className="footer-sub-menu">
                    <li>
                      <a href="https://tnris.org/education/gis-mentorship" tabIndex="0">
                        GIS Mentorships
                      </a>
                    </li>
                    <li>
                      <a href="https://tnris.org/education/purchasers" tabIndex="0">
                        Purchaser Resources
                      </a>
                    </li>
                  </ul>
                </li>
                <li><a href="texas-imagery-service" tabIndex="0">Texas Imagery Service</a></li>
              </ul>
            </div>
            <div className={`mdc-layout-grid__cell--span-3-desktop
              mdc-layout-grid__cell--span-4-tablet  mdc-layout-grid__cell--span-2-phone`}>
              <h4>Site</h4>
              <ul>
                <li><a href="https://tnris.org/about" tabIndex="0">About Us</a></li>
                <li><a href="https://tnris.org/contact" tabIndex="0">Contact Us</a></li>
                <li><a href="https://tnris.org/order-data" tabIndex="0">Order Data</a></li>
              </ul>
            </div>
            <div className={`mdc-layout-grid__cell--span-3-desktop
              mdc-layout-grid__cell--span-4-tablet  mdc-layout-grid__cell--span-2-phone`}>
              <h4>Location</h4>
              <address>
                1700 N. Congress, Room B-40<br />
                Austin, Texas, 78701
              </address>
              <small>
                <a href="https://goo.gl/maps/RE5BC" target="_blank" rel="noopener noreferrer" tabIndex="0">
                  <i className="material-icons">open_in_new</i>View Map
                </a>
              </small>
              <p>
                <a href="tel:5124638337" tabIndex="0">
                  <i className="material-icons">phone</i>512-463-8337
                </a>
                <br />
                RDC Office Hours:<br />
                Monday-Friday, 8am-4pm<br />
                By Appointment Only
              </p>
            </div>
          </div>
        </div>
        <div className="footer-component__copyright">
          {`Content of this site © Texas Natural Resources Information
            System and Texas Water Development Board unless otherwise noted.`}
        </div>
      </div>
    );
  }
}
