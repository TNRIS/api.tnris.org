import React from 'react';
import { Redirect } from 'react-router';
import { Route, Switch } from 'react-router';
import { matchPath } from 'react-router-dom';

import Footer from './Footer';
import HistoricalAerialTemplate from './HistoricalAerialTemplate/HistoricalAerialTemplate';
import OutsideEntityTemplate from './TnrisOutsideEntityTemplate/TnrisOutsideEntityTemplate';
import TnrisOrderTemplate from './TnrisOrderTemplate/TnrisOrderTemplate';
import CollectionFilterMapView from './CollectionFilterMapView';
import NotFound from './NotFound';

import HeaderContainer from '../containers/HeaderContainer';
import ToolDrawerContainer from '../containers/ToolDrawerContainer';
import CatalogCardContainer from '../containers/CatalogCardContainer';
import TnrisDownloadTemplateContainer from '../containers/TnrisDownloadTemplateContainer';
import OrderCartViewContainer from '../containers/OrderCartViewContainer';

import loadingImage from '../images/loading.gif';
import noDataImage from '../images/no-data.png';

export default class Catalog extends React.Component {
  constructor(props) {
    super(props);

    window.innerWidth >= 1050 ? this.state = {
      toolDrawerView:'dismiss',
      showToolDrawerInCatalogView: true
    } : this.state = {
      toolDrawerView:'modal',
      showToolDrawerInCatalogView: true
    };

    this.handleResize = this.handleResize.bind(this);
    this.handleToolDrawerDisplayDesktop = this.handleToolDrawerDisplayDesktop.bind(this);
    this.handleShowCollectionView = this.handleShowCollectionView.bind(this);
    this.setCatalogView = this.setCatalogView.bind(this);
    this.loadingMessage = (
      <div className="catalog-component__loading">
        <img src={loadingImage} alt="Holodeck Loading..." className="holodeck-loading-image" />
      </div>
    );
  }

  componentDidMount() {
    this.props.fetchCollections();
    this.props.fetchStoredShoppingCart();
    window.addEventListener("resize", this.handleResize);
    window.onpopstate = (e) => {
      const theState = e.state.state;
      this.props.popBrowserStore(theState);
      if (this.props.view === 'catalog' &&
          this.state.showToolDrawerInCatalogView &&
          this.state.toolDrawerView === 'dismiss' &&
          this.props.toolDrawerStatus === 'closed') {
        this.props.openToolDrawer();
      }
    }
  }

  componentWillUnmount() {
    window.removeEventListener("resize", this.handleResize);
  }

  componentDidUpdate(prevProps, prevState) {
    if (this.props.view !== 'catalog' && this.props.view !== 'geoFilter') {
      if (!this.props.location.pathname.includes('/collection/') && !this.props.location.pathname.includes('/cart/')) {
        this.props.setViewCatalog();
      }
    }
    if (prevProps.theme !== this.props.theme) {
      const themedClass = this.props.theme + "-app-theme";
      const html = document.querySelector('html');
      html.className = themedClass;
    }
    if (this.props.view === 'orderCart' && this.props.toolDrawerStatus === 'open') {
      this.props.closeToolDrawer();
    }
  }

  handleResize() {
    if (window.innerWidth >= 1050) {
      this.setState({toolDrawerView:'dismiss'});
      if (this.state.showToolDrawerInCatalogView) {
        this.props.openToolDrawer();
      }
    }
    else {
      this.setState({toolDrawerView:'modal'});
      this.props.closeToolDrawer();
      const scrim = document.getElementById('scrim');
      scrim.onclick = () => {
        this.props.closeToolDrawer();
      };
    }
  }

  handleToolDrawerDisplayDesktop() {
    if (this.props.toolDrawerStatus === 'open') {
      this.props.closeToolDrawer();
      this.setState({showToolDrawerInCatalogView: false});
      return;
    }
    this.props.openToolDrawer();
    this.setState({showToolDrawerInCatalogView: true});
  }

  handleShowCollectionView() {
    if (this.props.selectedCollection) {
      let collection = this.props.collections[this.props.selectedCollection];
      switch(collection['template']) {
        case 'tnris-download':
          return (<TnrisDownloadTemplateContainer collection={collection} />);
        case 'tnris-order':
          return (<TnrisOrderTemplate collection={collection} />);
        case 'historical-aerial':
          return (<HistoricalAerialTemplate collection={collection} />);
        case 'outside-entity':
          return (<OutsideEntityTemplate collection={collection} />);
        default:
          return (<TnrisDownloadTemplateContainer collection={collection} />);
      }
    }
    else {
      const match = matchPath(
        this.props.history.location.pathname,
        { path: '/collection/:collectionId' }
      );
      if (this.props.collections && Object.keys(match.params).includes('collectionId')) {
        if (!Object.keys(this.props.collections).includes(match.params.collectionId)) {
          return <Redirect to='/404' />;
        }
      }
    }

  }

  setCatalogView() {
    const noDataDivClass = this.props.toolDrawerStatus === 'open' && this.state.showToolDrawerInCatalogView ?
      'no-data no-data-open' : 'no-data no-data-closed';
    if (this.props.view === 'geoFilter') {
      return <CollectionFilterMapView />
    }
    else {
      const catalogCards = this.props.visibleCollections && this.props.visibleCollections.length < 1 ?
        <div className={noDataDivClass}>
          <img
            src={noDataImage}
            className="no-data-image"
            alt="No Data Available"
            title="No data available with those search terms" />
        </div> : <div className="catalog-grid mdc-layout-grid">
            <ul className="mdc-layout-grid__inner">
              {this.props.visibleCollections ? this.props.visibleCollections.map(collectionId =>
                <li
                  className="mdc-layout-grid__cell mdc-layout-grid__cell--span-3-desktop"
                  key={collectionId}>
                  <CatalogCardContainer
                    collection={this.props.collections[collectionId]} />
                </li>
              ) : this.loadingMessage}
            </ul>
          </div>;
      return catalogCards;
    }
  }

  render() {
    const { error, loading } = this.props;

    let dismissClass = 'closed-drawer';
    if (this.props.toolDrawerStatus === 'open' && this.state.toolDrawerView === 'dismiss') {
      dismissClass = 'open-drawer';
    }

    if (error) {
      return <div>Error! {error.message}</div>;
    }

    if (loading) {
      return this.loadingMessage;
    }

    return (
      <div className="catalog-component">
        <ToolDrawerContainer
          total={this.props.visibleCollections ? this.props.visibleCollections.length : 0}
          showToolDrawerInCatalogView={this.state.showToolDrawerInCatalogView}
          view={this.state.toolDrawerView} />

        <HeaderContainer
          toolDrawerView={this.state.toolDrawerView}
          toggleToolDrawerDisplay={this.toggleToolDrawerDisplay}
          showToolDrawerInCatalogView={this.state.showToolDrawerInCatalogView} />

        <div className={`catalog ${dismissClass} mdc-drawer-app-content`}>
          <div>
            <Switch>
              <Route path='/collection/:collectionId' exact render={(props) => this.handleShowCollectionView()} />
              <Route path='/catalog/:filters' exact render={(props) => this.setCatalogView()} />
              <Route path='/cart/' exact render={(props) => <OrderCartViewContainer toolDrawerView={this.state.toolDrawerView} showToolDrawerInCatalogView={this.state.showToolDrawerInCatalogView}/>} />
              <Route path='/' exact render={(props) => this.setCatalogView()} />
              <Route path='*' render={(props) => <NotFound status={this.props.toolDrawerStatus} />} />
            </Switch>
          </div>
        </div>

        <Footer
          view={this.state.toolDrawerView}
          status={this.props.toolDrawerStatus}
          showToolDrawerInCatalogView={this.state.showToolDrawerInCatalogView} />

      </div>
    );
  }
}
