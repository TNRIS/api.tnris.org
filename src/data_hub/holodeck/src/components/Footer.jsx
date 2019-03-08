import React from 'react';
import { MDCMenu } from '@material/menu';

export default class Footer extends React.Component {
  constructor(props) {
      super(props);
      this.showLinkMenu = this.showLinkMenu.bind(this);
  }

  showLinkMenu(menuRef) {
    this.menu = new MDCMenu(this.refs[menuRef]);
    this.menu.open = true;
  }

  render() {
    let drawerStatusClass = 'closed-drawer';
    if (this.props.view === 'catalog' &&
      this.props.toolDrawerVariant === 'dismissible' &&
      this.props.toolDrawerStatus === 'open') {
      drawerStatusClass = 'open-drawer';
    }

    return (
      <div className={`footer-component ${drawerStatusClass}`} id='master-footer'>
          <ul className="link-container">

            <li className="link-container-menu-list">
              <div className="mdc-menu-surface--anchor" onClick={() => this.showLinkMenu('legal_link_menu')} tabIndex="0">
                <div className="link-menu-control">
                  <i className="material-icons" alt="Legal Links" title="Legal Links">gavel</i>
                </div>
                <div ref="legal_link_menu" className="mdc-menu mdc-menu-surface">
                  <ul className="mdc-list inner-menu-link-list" role="menu" aria-hidden="true">
                    <li className="mdc-list-item" role="menuitem" tabIndex="0">
                      <a href="https://tnris.org/site-policies#privacy-and-security-policy" target="_blank" rel="noopener noreferrer" tabIndex="0">
                        Privacy/Security Policy
                      </a>
                    </li>
                    <li className="mdc-list-item" role="menuitem" tabIndex="0">
                      <a href="https://tnris.org/site-policies#accessibility-policy" target="_blank" rel="noopener noreferrer" tabIndex="0">
                        Accessibility
                      </a>
                    </li>
                    <li className="mdc-list-item" role="menuitem" tabIndex="0">
                      <a href="http://www.twdb.texas.gov/home/open_records.asp" target="_blank" rel="noopener noreferrer" tabIndex="0">
                        Open Records Request
                      </a>
                    </li>
                    <li className="mdc-list-item" role="menuitem" tabIndex="0">
                      <a href="http://www.twdb.texas.gov/home/compact_texan.asp" target="_blank" rel="noopener noreferrer" tabIndex="0">
                        Compact with Texans
                      </a>
                    </li>
                    <li className="mdc-list-item" role="menuitem" tabIndex="0">
                      <a href="http://www.twdb.texas.gov/home/fraud.asp" target="_blank" rel="noopener noreferrer" tabIndex="0">
                        Fraud &amp; Waste
                      </a>
                    </li>
                    <li className="mdc-list-item" role="menuitem" tabIndex="0">
                      <a href="https://www.tsl.texas.gov/trail/index.html" target="_blank" rel="noopener noreferrer" tabIndex="0">TRAIL</a>
                    </li>
                    <li className="mdc-list-item" role="menuitem" tabIndex="0">
                      <a href="http://www.texas.gov" target="_blank" rel="noopener noreferrer" tabIndex="0">Texas.gov</a>
                    </li>
                    <li className="mdc-list-item" role="menuitem" tabIndex="0">
                      <a href="http://www.twdb.texas.gov" target="_blank" rel="noopener noreferrer" tabIndex="0">
                        <abbr title="Texas Water Development Board">TWDB</abbr>
                      </a>
                    </li>
                  </ul>
                </div>
              </div>
            </li>

            <li className="link-container-menu-list">
              <div className="mdc-menu-surface--anchor" onClick={() => this.showLinkMenu('copyright_menu')} tabIndex="0">
                <div className="link-menu-control">
                  <i className="material-icons" alt="Copyright" title="Copyright">copyright</i>
                </div>
                <div ref="copyright_menu" className="mdc-menu mdc-menu-surface">
                  <ul className="mdc-list inner-menu-link-list" role="menu" aria-hidden="true">
                    <p className="nested-item">
                      Content of this site © Texas Natural Resources Information System and Texas Water Development Board unless otherwise noted.
                    </p>
                  </ul>
                </div>
              </div>
            </li>

            <li className="link-container-menu-list">
              <div className="mdc-menu-surface--anchor" onClick={() => this.showLinkMenu('contact_menu')} tabIndex="0">
                <div className="link-menu-control">
                  <i className="material-icons" alt="Contact Information" title="Contact Information">phone</i>
                </div>
                <div ref="contact_menu" className="mdc-menu mdc-menu-surface">
                  <ul className="mdc-list inner-menu-link-list" role="menu" aria-hidden="true">
                    <div className="nested-item location-item">
                      <span><strong>Location</strong></span>
                      <address>
                        1700 N. Congress<br />
                        Room B-40<br />
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
                        <strong>RDC Office Hours:</strong><br />
                        Monday-Friday, 8am-4pm<br />
                        By Appointment Only
                      </p>
                    </div>
                  </ul>
                </div>
              </div>
            </li>

            <li className="link-container-menu-list">
              <div className="mdc-menu-surface--anchor" onClick={() => this.showLinkMenu('tnris_link_menu')} tabIndex="0">
                <div className="link-menu-control">
                  <i className="material-icons" alt="TNRIS Links" title="TNRIS Links">web</i>
                </div>
                <div ref="tnris_link_menu" className="mdc-menu mdc-menu-surface">
                  <ul className="mdc-list inner-menu-link-list" role="menu" aria-hidden="true">
                    <li className="mdc-list-item" role="menuitem" tabIndex="0">
                      <a href="https://tnris.org/maps-and-data/applications-and-utilities" target="_blank" rel="noopener noreferrer" tabIndex="0">
                        Applications and Utilities
                      </a>
                    </li>
                    <li className="mdc-list-item" role="menuitem" tabIndex="0">
                      <a href="https://tnris.org/research-distribution-center" target="_blank" rel="noopener noreferrer" tabIndex="0">
                        Research &amp; Distribution
                      </a>
                    </li>
                    <li className="mdc-list-item" role="menuitem" tabIndex="0">
                      <a href="https://tnris.org/stratmap" target="_blank" rel="noopener noreferrer" tabIndex="0">
                        StratMap Program
                      </a>
                    </li>
                    <li className="mdc-list-item" role="menuitem" tabIndex="0">
                      <a href="https://tnris.org/training" target="_blank" rel="noopener noreferrer" tabIndex="0">
                        Education &amp; Training
                      </a>
                    </li>
                    <li className="mdc-list-item" role="menuitem" tabIndex="0">
                      <a href="https://tnris.org/about" target="_blank" rel="noopener noreferrer" tabIndex="0">
                        About Us
                      </a>
                    </li>
                    <li className="mdc-list-item" role="menuitem" tabIndex="0">
                      <a href="https://tnris.org/contact" target="_blank" rel="noopener noreferrer" tabIndex="0">
                        General Contact
                      </a>
                    </li>
                  </ul>
                </div>
              </div>
            </li>

          </ul>
      </div>
    );
  }
}
