import React from 'react';
import { Redirect } from 'react-router';

import CatalogCardContainer from '../containers/CatalogCardContainer';
import Footer from './Footer';
import HistoricalAerialTemplate from './HistoricalAerialTemplate/HistoricalAerialTemplate';
import OutsideEntityTemplate from './TnrisOutsideEntityTemplate/TnrisOutsideEntityTemplate';
import TnrisDownloadTemplate from './TnrisDownloadTemplate/TnrisDownloadTemplate';
import TnrisOrderTemplate from './TnrisOrderTemplate/TnrisOrderTemplate';
import CollectionFilterMapDialogContainer from '../containers/CollectionFilterMapDialogContainer';
import HeaderContainer from '../containers/HeaderContainer';
import OrderCartDialogContainer from '../containers/OrderCartDialogContainer';
import ToolDrawerContainer from '../containers/ToolDrawerContainer';
import loadingImage from '../images/loading.gif';
import noDataImage from '../images/no-data.png';

export default class Catalog extends React.Component {
  constructor(props) {
    super(props);

    window.innerWidth >= 1050 ? this.state = {
      toolDrawerView:'dismiss',
      badUrlFlag: false
    } : this.state = {
      toolDrawerView:'modal',
      badUrlFlag: false
    };

    this.handleResize = this.handleResize.bind(this);
    this.handler = this.handler.bind(this);
    this.handleCloseCollectionView = this.handleCloseCollectionView.bind(this);
    this.handleShowCollectionView = this.handleShowCollectionView.bind(this);
  }

  componentDidMount() {
    this.props.fetchCollections();
    this.props.fetchStoredShoppingCart();
    window.addEventListener("resize", this.handleResize);
  }

  componentWillUnmount() {
    window.removeEventListener("resize", this.handleResize);
  }

  componentDidUpdate() {
    if (this.props.collections && Object.keys(this.props.match.params).includes('collectionId')) {
      if (!Object.keys(this.props.collections).includes(this.props.match.params.collectionId)) {
        // console.log(this.props.match.params.collectionId);
        this.setState({
          badUrlFlag: true
        });
      }
    }
  }

  componentWillReceiveProps(nextProps) {
    const themedClass = nextProps.theme + "-app-theme";
    const html = document.querySelector('html');
    html.className = themedClass;
  }

  handleResize() {
    if (window.innerWidth >= 1050) {
      this.setState({toolDrawerView:'dismiss'});
      this.setState({toolDrawerStatus: 'open'});
    }
    else {
      this.setState({toolDrawerView:'modal'});
      this.setState({toolDrawerStatus:'closed'});
      const scrim = document.getElementById('scrim');
      scrim.onclick = () => {
        this.setState({toolDrawerStatus:'closed'});
      };
    }
  }

  handler() {
    if (this.props.selectedCollection === null) {
      this.props.toolDrawerStatus === 'open' ? this.props.closeToolDrawer() : this.props.openToolDrawer();
    } else {
      this.handleCloseCollectionView();
      this.props.openToolDrawer();
    }
    if (this.state.toolDrawerView === 'modal') {
      const scrim = document.getElementById('scrim');
      scrim.onclick = () => {
        this.props.closeToolDrawer();
      };
    }
  }

  handleShowCollectionView() {
    if (this.props.showCollectionDialog) {
      let collection = this.props.collections[this.props.selectedCollection];
      switch(collection['template']) {
        case 'tnris-download':
          return (<TnrisDownloadTemplate collection={collection} />);
        case 'tnris-order':
          return (<TnrisOrderTemplate collection={collection} />);
        case 'historical-aerial':
          return (<HistoricalAerialTemplate collection={collection} />);
        case 'outside-entity':
          return (<OutsideEntityTemplate collection={collection} />);
        default:
          return (<TnrisDownloadTemplate collection={collection} />);
      }
    }
  }

  handleCloseCollectionView() {
    this.props.closeCollectionDialog();
    this.props.clearSelectedCollection();
    if (this.props.previousUrl.includes('/collection/')) {
      this.props.setUrl('/', this.props.history);
    }
    else {
      this.props.setUrl(this.props.previousUrl, this.props.history);
    }
  }

  render() {
    // console.log(this.props);
    const { error, loading } = this.props;
    let noDataDivClass = 'no-data no-data-closed';
    let dismissClass = 'closed-drawer';

    const loadingMessage = (
      <div className="catalog-component__loading">
        <img src={loadingImage} alt="Holodeck Loading..." className="holodeck-loading-image" />
      </div>
    );

    if (this.props.toolDrawerStatus === 'open' && this.state.toolDrawerView === 'dismiss') {
      dismissClass = 'open-drawer';
      noDataDivClass = 'no-data no-data-open';
    }

    if (error) {
      return <div>Error! {error.message}</div>;
    }

    if (loading) {
      return loadingMessage;
    }

    if (this.state.badUrlFlag) {
      return <Redirect to='/404' />;
    }

    return (
      <div className="catalog-component">

        <OrderCartDialogContainer />
        <CollectionFilterMapDialogContainer />

        <ToolDrawerContainer
          match={this.props.match}
          history={this.props.history}
          total={this.props.visibleCollections ? this.props.visibleCollections.length : 0}
          view={this.state.toolDrawerView}
          status={this.props.toolDrawerStatus}
        />

        <HeaderContainer
          view={this.state.toolDrawerView}
          status={this.props.toolDrawerStatus}
          handler={this.handler}
          match={this.props.match}
          history={this.props.history} />

        <div className={`catalog ${dismissClass} mdc-drawer-app-content`}>
          {this.props.visibleCollections && this.props.visibleCollections.length < 1 ?
            <div className={noDataDivClass}>
              <img
                src={noDataImage}
                className="no-data-image"
                alt="No Data Available"
                title="No data available with those search terms" />
            </div> : ''}

          {this.props.showCollectionDialog ? this.handleShowCollectionView() :
            <div className="mdc-layout-grid">
              <ul className="mdc-layout-grid__inner">
                {this.props.visibleCollections ? this.props.visibleCollections.map(collectionId =>
                  <li
                    className="mdc-layout-grid__cell mdc-layout-grid__cell--span-2"
                    key={collectionId}>
                    <CatalogCardContainer
                      collection={this.props.collections[collectionId]}
                      match={this.props.match}
                      history={this.props.history} />
                  </li>
                ) : loadingMessage}
              </ul>
            </div>
          }
        </div>

        <Footer
          view={this.state.toolDrawerView}
          status={this.props.toolDrawerStatus} />

      </div>
    );
  }
}
