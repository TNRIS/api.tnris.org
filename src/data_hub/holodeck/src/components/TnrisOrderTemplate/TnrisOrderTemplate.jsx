import React from 'react';
import {MDCTopAppBar} from '@material/top-app-bar/index';
import {MDCTabBar} from '@material/tab-bar';
import { MDCMenu } from '@material/menu';

import TnrisOrderTemplateDetails from './TnrisOrderTemplateDetails';
import TnrisOrderTemplateImages from './TnrisOrderTemplateImages';
import TnrisOrderTemplateOrder from './TnrisOrderTemplateOrder';
// import TnrisOrderTemplateOrderContainer from '../../containers/TnrisOrderTemplateOrderContainer';

export default class TnrisOrderTemplate extends React.Component {
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
      case 'images':
        tabIndex = 1;
        break;
      case 'order':
        tabIndex = 2;
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
    switch(this.state.view) {
      case 'details':
        showComponent = <TnrisOrderTemplateDetails collection={this.props.collection} />;
        break;
      case 'images':
        showComponent = (<TnrisOrderTemplateImages
          images={this.props.collection.images}
          thumbnail={this.props.collection.thumbnail_image} />);
        break;
      case 'order':
        showComponent = <TnrisOrderTemplateOrder />;
        break;
      default:
        showComponent = <TnrisOrderTemplateDetails collection={this.props.collection} />;
    }

    return (
      <div className='tnris-download-template' tabIndex='1'>
        <header className="mdc-top-app-bar">
          <div className="mdc-top-app-bar__row">
            <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-start">
              <span className="mdc-top-app-bar__title">{this.props.collection.name}</span>
            </section>
            <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-end" role="toolbar">
              <div className="mdc-tab-bar" role="tablist">
                <div className="mdc-tab-scroller">
                  <div className="mdc-tab-scroller__scroll-area">
                    <div className="mdc-tab-scroller__scroll-content">
                      <button className="mdc-tab mdc-tab--active" role="tab" aria-selected="true" tabIndex="0" onClick={() => this.setTemplateView("details")}>
                        <span className="mdc-tab__content">
                          <span className="mdc-tab__icon material-icons">details</span>
                          <span className="mdc-tab__text-label">Details</span>
                        </span>
                        <span className="mdc-tab-indicator mdc-tab-indicator--active">
                          <span className="mdc-tab-indicator__content mdc-tab-indicator__content--underline"></span>
                        </span>
                        <span className="mdc-tab__ripple"></span>
                      </button>
                      <button className="mdc-tab" role="tab" aria-selected="false" tabIndex="-1"  onClick={() => this.setTemplateView("images")}>
                        <span className="mdc-tab__content">
                          <span className="mdc-tab__icon material-icons">collections</span>
                          <span className="mdc-tab__text-label">Images</span>
                        </span>
                        <span className="mdc-tab-indicator">
                          <span className="mdc-tab-indicator__content mdc-tab-indicator__content--underline"></span>
                        </span>
                        <span className="mdc-tab__ripple"></span>
                      </button>
                      <button className="mdc-tab" role="tab" aria-selected="false" tabIndex="-1"  onClick={() => this.setTemplateView("order")}>
                        <span className="mdc-tab__content">
                          <span className="mdc-tab__icon material-icons">save_alt</span>
                          <span className="mdc-tab__text-label">Order</span>
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
                    <a className={this.state.view === 'images' ? 'mdc-list-item  mdc-list-item--activated' : 'mdc-list-item'}
                       onClick={() => this.setTemplateView("images")}>
                       <i className="mdc-tab__icon material-icons">collections</i> Images
                    </a>
                    <a className={this.state.view === 'download' ? 'mdc-list-item  mdc-list-item--activated' : 'mdc-list-item'}
                       onClick={() => this.setTemplateView("download")}>
                       <i className="mdc-tab__icon material-icons">save_alt</i> Download
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
