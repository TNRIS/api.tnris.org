import React from 'react';
import {MDCTopAppBar} from '@material/top-app-bar/index';
import {MDCTabBar} from '@material/tab-bar';
import { MDCMenu } from '@material/menu';

import TnrisDownloadTemplateDetails from './TnrisDownloadTemplateDetails';

import TnrisDownloadTemplateDownloadContainer from '../../containers/TnrisDownloadTemplateDownloadContainer';
import ContactContainer from '../../containers/ContactContainer';
import OrderTnrisDataFormContainer from '../../containers/OrderTnrisDataFormContainer';

export default class TnrisDownloadTemplate extends React.Component {
  constructor(props) {
      super(props);
      this.state = {
        view:'details'
      };
      this.setTemplateView = this.setTemplateView.bind(this);
      this.showTabMenu = this.showTabMenu.bind(this);
  }

  componentDidMount() {
    this.topAppBarElement = document.querySelector('.mdc-top-app-bar');
    this.topAppBar = new MDCTopAppBar(this.topAppBarElement);
    this.tabBar = new MDCTabBar(document.querySelector('.mdc-tab-bar'));
  }

  setTemplateView(viewString) {
    this.setState({view: viewString});
    let tabIndex;
    switch(viewString) {
      case 'details':
        tabIndex = 0;
        break;
      case 'download':
        tabIndex = 1;
        break;
      case 'order':
        tabIndex = 2
        break;
      case 'contact':
        tabIndex = 3;
        break;
      default:
        tabIndex = 0;
    }
    this.tabBar.activateTab(tabIndex);
  }

  showTabMenu() {
    this.menu = new MDCMenu(this.refs.tab_menu);
    this.menu.open = true;
  }

  render() {
    let showComponent;
    let templateClass;
    switch(this.state.view) {
      case 'details':
        showComponent = <TnrisDownloadTemplateDetails collection={this.props.collection} />;
        templateClass = 'tnris-download-template';
        break;
      case 'download':
        showComponent = <TnrisDownloadTemplateDownloadContainer />;
        templateClass = 'tnris-download-template dark-theme';
        break;
      case 'contact':
        showComponent = (
          <div className='tnris-download-template-details'>
            <div className="template-content-div">
              <div className='mdc-typography--headline5 template-content-div-header'>
                Contact
              </div>
              <div>
                <ContactContainer collection={this.props.collection}/>
              </div>
            </div>
          </div>
        )
        templateClass = 'tnris-download-template';
        break;
      case 'order':
        showComponent = (
          <div className='tnris-download-template-details'>
            <div className="template-content-div">
              <div className='mdc-typography--headline5 template-content-div-header'>
                Order
              </div>
              <div>
                <OrderTnrisDataFormContainer />
              </div>
            </div>
          </div>
        )
        templateClass = 'tnris-download-template';
        break;
      default:
        showComponent = <TnrisDownloadTemplateDetails collection={this.props.collection} />;
        templateClass = 'tnris-download-template';
    }

    return (
      <div className={templateClass} tabIndex='1'>
        <header className="mdc-top-app-bar">
          <div className="mdc-top-app-bar__row">

            <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-start">
              <span className="mdc-top-app-bar__title">{this.props.collection.name}</span>
            </section>

            <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-end" role="toolbar">

              <div className="mdc-tab-bar" role="tablist">

                <div className="mdc-tab-scroller mdc-tab-scroller--align-end">
                  <div className="mdc-tab-scroller__scroll-area">
                    <div className="mdc-tab-scroller__scroll-content">

                      <button className="mdc-tab mdc-tab--active" role="tab" aria-selected="true" tabIndex="0" onClick={() => this.setTemplateView("details")} title="Details">
                        <span className="mdc-tab__content">
                          <span className="mdc-tab__icon material-icons">details</span>
                        </span>
                        <span className="mdc-tab-indicator mdc-tab-indicator--active">
                          <span className="mdc-tab-indicator__content mdc-tab-indicator__content--underline"></span>
                        </span>
                        <span className="mdc-tab__ripple"></span>
                      </button>

                      <button className="mdc-tab" role="tab" aria-selected="false" tabIndex="-1"  onClick={() => this.setTemplateView("download")} title="Download">
                        <span className="mdc-tab__content">
                          <span className="mdc-tab__icon material-icons">save_alt</span>
                        </span>
                        <span className="mdc-tab-indicator">
                          <span className="mdc-tab-indicator__content mdc-tab-indicator__content--underline"></span>
                        </span>
                        <span className="mdc-tab__ripple"></span>
                      </button>

                      <button className="mdc-tab" role="tab" aria-selected="false" tabIndex="-1"  onClick={() => this.setTemplateView("order")} title="Order">
                        <span className="mdc-tab__content">
                          <span className="mdc-tab__icon material-icons">shopping_basket</span>
                        </span>
                        <span className="mdc-tab-indicator">
                          <span className="mdc-tab-indicator__content mdc-tab-indicator__content--underline"></span>
                        </span>
                        <span className="mdc-tab__ripple"></span>
                      </button>

                      <button className="mdc-tab" role="tab" aria-selected="false" tabIndex="-1"  onClick={() => this.setTemplateView("contact")} title="Contact">
                        <span className="mdc-tab__content">
                          <span className="mdc-tab__icon material-icons">contact_support</span>
                        </span>
                        <span className="mdc-tab-indicator">
                          <span className="mdc-tab-indicator__content mdc-tab-indicator__content--underline"></span>
                        </span>
                        <span className="mdc-tab__ripple"></span>
                      </button>

                    </div>
                  </div>
                </div>

              </div>

              <div className="mdc-menu-surface--anchor">
                <a onClick={this.showTabMenu} className="mdc-top-app-bar__action-item">
                  <i className="material-icons mdc-top-app-bar__navigation-icon">more_vert</i>
                </a>
                <div ref="tab_menu" className="mdc-menu mdc-menu-surface">
                  <nav className="mdc-list">
                    <a className={this.state.view === 'details' ? 'mdc-list-item  mdc-list-item--activated' : 'mdc-list-item'}
                       onClick={() => this.setTemplateView("details")}>
                       <i className="mdc-tab__icon material-icons">details</i> Details
                    </a>
                    <a className={this.state.view === 'download' ? 'mdc-list-item  mdc-list-item--activated' : 'mdc-list-item'}
                       onClick={() => this.setTemplateView("download")}>
                       <i className="mdc-tab__icon material-icons">save_alt</i> Download
                    </a>
                    <a className={this.state.view === 'download' ? 'mdc-list-item  mdc-list-item--activated' : 'mdc-list-item'}
                       onClick={() => this.setTemplateView("order")}>
                       <i className="mdc-tab__icon material-icons">shopping_basket</i> Order
                    </a>
                    <a className={this.state.view === 'contact' ? 'mdc-list-item  mdc-list-item--activated' : 'mdc-list-item'}
                       onClick={() => this.setTemplateView("contact")}>
                       <i className="mdc-tab__icon material-icons">contact_support</i> Contact
                    </a>
                  </nav>
                </div>
              </div>

            </section>
          </div>
        </header>

        {showComponent}

      </div>
    );
  }
}
