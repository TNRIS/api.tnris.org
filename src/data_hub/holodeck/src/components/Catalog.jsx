import React from 'react';
import { Redirect } from 'react-router';

import CatalogCardContainer from '../containers/CatalogCardContainer';
import CollectionDialogContainer from '../containers/CollectionDialogContainer';
// import Drawer from './Drawer';
import Footer from './Footer';
import CollectionFilterMapDialogContainer from '../containers/CollectionFilterMapDialogContainer';
import HeaderContainer from '../containers/HeaderContainer';
import OrderCartDialogContainer from '../containers/OrderCartDialogContainer';
import ToolDrawerContainer from '../containers/ToolDrawerContainer';
import loadingImage from '../images/loading.gif';
import noDataImage from '../images/no-data.png';

export default class Catalog extends React.Component {
  constructor(props) {
    super(props);

    window.innerWidth >= 1050 ? this.state = {toolDrawerView:'dismiss', toolDrawerStatus:'open', badUrlFlag: false} : this.state = {toolDrawerView:'modal', toolDrawerStatus:'closed', badUrlFlag: false};

    this.handleResize = this.handleResize.bind(this);
    this.handler = this.handler.bind(this);
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
    this.state.toolDrawerStatus === 'open' ? this.setState({toolDrawerStatus:'closed'}) : this.setState({toolDrawerStatus:'open'});

    if (this.state.toolDrawerView === 'modal') {
      const scrim = document.getElementById('scrim');
      scrim.onclick = () => {
        this.setState({toolDrawerStatus:'closed'});
      };
    }
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
        console.log(this.props.match.params.collectionId);
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

  render() {
    const { error, loading } = this.props;

    const loadingMessage = (
        <div className="catalog-component__loading">
          <img src={loadingImage} alt="Holodeck Loading..." className="holodeck-loading-image" />
        </div>
      );

    const noData = (
        <div className="no-data">
          <img src={noDataImage} className="no-data-image" alt="No Data Available" title="No data available with those search terms" />
        </div>
      );

    let dismissClass = 'closed-drawer';

    if (this.state.toolDrawerStatus === 'open' && this.state.toolDrawerView === 'dismiss') {
      dismissClass = 'open-drawer';
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

        <CollectionDialogContainer history={this.props.history} />
        <OrderCartDialogContainer />
        <CollectionFilterMapDialogContainer />

        <ToolDrawerContainer
          match={this.props.match}
          history={this.props.history}
          total={this.props.visibleCollections ? this.props.visibleCollections.length : 0}
          view={this.state.toolDrawerView}
          status={this.state.toolDrawerStatus}
        />

        <HeaderContainer
          view={this.state.toolDrawerView}
          status={this.state.toolDrawerStatus}
          handler={this.handler} />

        <div className={`catalog ${dismissClass}`}>
          {this.props.visibleCollections && this.props.visibleCollections.length < 1 ? noData : ''}

          <ul className='catalog-list mdc-image-list mdc-image-list--with-text-protection'>
            {this.props.visibleCollections ? this.props.visibleCollections.map(collectionId =>
              <CatalogCardContainer collection={this.props.collections[collectionId]} key={collectionId} match={this.props.match} history={this.props.history} />
            ) : loadingMessage}
          </ul>
        </div>

        <Footer
          view={this.state.toolDrawerView}
          status={this.state.toolDrawerStatus} />

      </div>
    );
  }
}
