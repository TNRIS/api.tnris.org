import React from 'react';
import {MDCTopAppBar} from '@material/top-app-bar/index';
import {MDCTabBar} from '@material/tab-bar';

import TnrisDownloadTemplateDetails from './TnrisDownloadTemplateDetails';

export default class TnrisDownloadTemplate extends React.Component {
  constructor(props) {
      super(props);
      console.log(this.props);
      this.state = {
        view:'details'
      };
      this.setTemplateView = this.setTemplateView.bind(this);
  }

  componentDidMount() {
    this.topAppBarElement = document.querySelector('.mdc-top-app-bar');
    this.topAppBar = new MDCTopAppBar(this.topAppBarElement);
    this.tabBar = new MDCTabBar(document.querySelector('.mdc-tab-bar'));
  }

  setTemplateView(view) {
    this.setState({view: view});
  }

  render() {
    let view;
    switch(this.state.view) {
      case 'details':
        view = <TnrisDownloadTemplateDetails collection={this.props.collection} />;
        break;
      case 'images':
        view = <div className='images'></div>
        break;
      case 'download':
        view = <div className='download'></div>
        break;
      default:
        view = <div className='default'></div>
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
                      <button className="mdc-tab" role="tab" aria-selected="false" tabIndex="-1"  onClick={() => this.setTemplateView("download")}>
                        <span className="mdc-tab__content">
                          <span className="mdc-tab__icon material-icons">save_alt</span>
                          <span className="mdc-tab__text-label">Download</span>
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
            </section>
          </div>
        </header>
        {view}
      </div>
    );
  }
}
