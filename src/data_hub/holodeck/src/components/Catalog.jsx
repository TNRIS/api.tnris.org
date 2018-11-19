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

export default class Catalog extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      badUrlFlag: false,
      toolDrawerView: 'dismiss',
      toolDrawerStatus: 'open'
    }

    window.innerWidth >= 1050 ? this.state = {toolDrawerView:'dismiss', toolDrawerStatus: 'open'} : this.state = {toolDrawerView:'modal', toolDrawerStatus:'closed'};

    this.handleResize = this.handleResize.bind(this);
    this.handleDismissible = this.handleDismissible.bind(this);
    this.handleModal = this.handleModal.bind(this);
  }

  handleResize() {
    console.log(window.innerWidth);

    if (window.innerWidth >= 1050) {
      this.setState({toolDrawerView:'dismiss'});
      console.log('dismiss view');
      window.removeEventListener("click", this.handleModal);
      window.addEventListener("click", this.handleDismissible);
    }
    else if (window.innerWidth < 1050) {
      this.setState({toolDrawerView:'modal'});
      console.log('modal view');
      window.removeEventListener("click", this.handleDismissible);
      window.addEventListener("click", this.handleModal);
      console.log('log this to see if function ran');
    }
    else {
      console.log('error');
    }
  }

  handleDismissible() {
    const tools = document.getElementById('tools');
    const drawer = document.getElementById('dismiss-class');

    console.log('view :', this.state.toolDrawerView);

    if (this.state.toolDrawerView === 'dismiss') {
      tools.onclick = () => {
        console.log('you clicked the tools on dismiss view');
        // if (drawer.classList.contains('open-drawer')) {
        //   drawer.classList.remove('open-drawer');
        //   console.log('removed');
        // }
        // else {
        //   drawer.classList.add('open-drawer');
        //   console.log('added');
        // }
        this.state.toolDrawerStatus === 'open' ? this.setState({toolDrawerStatus:'closed'}) : this.setState({toolDrawerStatus:'open'});
      };
    }
  }

  handleModal() {
    const tools = document.getElementById('tools');
    const scrim = document.getElementById('scrim');
    // const aside = document.getElementById('aside-drawer');

    console.log('view :', this.state.toolDrawerView);

    if (this.state.toolDrawerView === 'modal') {
      tools.onclick = () => {
        console.log('you clicked the tools on modal view');
        // aside.classList.add('mdc-drawer--open')
        this.state.toolDrawerStatus === 'open' ? this.setState({toolDrawerStatus:'closed'}) : this.setState({toolDrawerStatus:'open'});
        // this.setState({toolDrawerStatus: !this.state.toolDrawerStatus})
        // aside.classList.contains('mdc-drawer--open') ? aside.classList.remove('mdc-drawer--open') : aside.classList.remove('mdc-drawer--closing') && console.log('test') && aside.classList.add('mdc-drawer--opening');
        console.log('modal view tools function ran');
      };

      scrim.onclick = () => {
        console.log('you clicked the scrim to close');
        this.setState({toolDrawerStatus:'closed'});
      };
    }
  }

  componentDidMount() {
    this.props.fetchCollections();
    this.props.fetchStoredShoppingCart();
    window.addEventListener("resize", this.handleResize);
    this.state.toolDrawerView === 'dismiss' ? window.addEventListener("click", this.handleDismissible) : window.addEventListener("click", this.handleModal);
  }

  componentWillUnmount() {
    window.removeEventListener("resize", this.handleResize);
    window.removeEventListener("click", this.handleDismissible);
    window.removeEventListener("click", this.handleModal);
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
          status={this.state.toolDrawerStaus} />

          <div className={`catalog ${dismissClass}`} id="dismiss-class">
            <ul className='catalog-list mdc-image-list mdc-image-list--with-text-protection'>
              {this.props.visibleCollections ? this.props.visibleCollections.map(collectionId =>
                <CatalogCardContainer collection={this.props.collections[collectionId]} key={collectionId} match={this.props.match} history={this.props.history} />
              ) : loadingMessage}
            </ul>
          </div>

        <Footer view={this.state.toolDrawerView} />

      </div>
    );
  }
}
