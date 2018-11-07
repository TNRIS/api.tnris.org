import React from 'react';
import {MDCTopAppBar} from '@material/top-app-bar/index';
import {MDCTabBar} from '@material/tab-bar';
import { MDCMenu } from '@material/menu';

import HistoricalAerialTemplateDetails from './HistoricalAerialTemplateDetails';
import OrderTnrisDataFormContainer from '../../containers/OrderTnrisDataFormContainer';

export default class HistoricalAerialTemplate extends React.Component {
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
      // case 'explore':
      //   tabIndex = 1;
      //   break;
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
        showComponent = <HistoricalAerialTemplateDetails collection={this.props.collection} />;
        break;
      // case 'explore':
      //   showComponent = (<div>Explore Map loaded with LS4 WMS Services</div>);
      //   break;
      case 'order':
        showComponent = (
          <div className='historical-aerial-template-details'>
            <div className="template-content-div">
              <div className='mdc-typography--headline5 template-content-div-header'>
                Order
              </div>
              <div>
                <OrderTnrisDataFormContainer />
              </div>
            </div>
          </div>
          );
        break;
      default:
        showComponent = <HistoricalAerialTemplateDetails collection={this.props.collection} />;
    }

    const collectionYear = this.props.collection.acquisition_date ? this.props.collection.acquisition_date.substring(0, 4) + ' ' : '';

    // const exploreTab = this.props.collection.index_service_url || this.props.collection.mosaic_service_url || this.props.collection.frames_service_url ? (
    //   <button className="mdc-tab" role="tab" aria-selected="false" tabIndex="-1"  onClick={() => this.setTemplateView("explore")}>
    //     <span className="mdc-tab__content">
    //       <span className="mdc-tab__icon material-icons">map</span>
    //       <span className="mdc-tab__text-label">Explore</span>
    //     </span>
    //     <span className="mdc-tab-indicator">
    //       <span className="mdc-tab-indicator__content mdc-tab-indicator__content--underline"></span>
    //     </span>
    //     <span className="mdc-tab__ripple"></span>
    //   </button>
    // ) : '';
    const exploreTab = '';
    // const exploreListItem = this.props.collection.index_service_url || this.props.collection.mosaic_service_url || this.props.collection.frames_service_url ? (
    //   <a className={this.state.view === 'explore' ? 'mdc-list-item  mdc-list-item--activated' : 'mdc-list-item'}
    //      onClick={() => this.setTemplateView("explore")}>
    //      <i className="mdc-tab__icon material-icons">map</i> Explore
    //   </a>
    // ) : '';
    const exploreListItem = '';

    return (
      <div className='historical-aerial-template' tabIndex='1'>
        <header className="mdc-top-app-bar">
          <div className="mdc-top-app-bar__row">

            <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-start">
              <span className="mdc-top-app-bar__title">{collectionYear}{this.props.collection.name}</span>
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

                      {exploreTab}

                      <button className="mdc-tab" role="tab" aria-selected="false" tabIndex="-1"  onClick={() => this.setTemplateView("order")} title="Order">
                        <span className="mdc-tab__content">
                          <span className="mdc-tab__icon material-icons">create</span>
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

                    {exploreListItem}

                    <a className={this.state.view === 'order' ? 'mdc-list-item  mdc-list-item--activated' : 'mdc-list-item'}
                       onClick={() => this.setTemplateView("order")}>
                       <i className="mdc-tab__icon material-icons">create</i> Order
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
