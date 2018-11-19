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
      toolDrawerView: 'dismiss'
    }

    window.innerWidth >= 1050 ? this.state = {toolDrawerView:'dismiss'} : this.state = {toolDrawerView:'modal'};

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
        if (drawer.classList.contains('open-drawer')) {
          drawer.classList.remove('open-drawer');
          console.log('removed');
        }
        else {
          drawer.classList.add('open-drawer');
          console.log('added');
        }
      };
    }
  }

  handleModal() {
    const tools = document.getElementById('tools');
    const scrim = document.getElementById('scrim');
    const aside = document.getElementById('aside-drawer');

    console.log('view :', this.state.toolDrawerView);

    if (this.state.toolDrawerView === 'modal') {
      tools.onclick = () => {
        console.log('you clicked the tools on modal view');
        // aside.classList.add('mdc-drawer--open')
        aside.classList.contains('mdc-drawer--open') ? aside.classList.remove('mdc-drawer--open') : aside.classList.remove('mdc-drawer--closing') && console.log('test') && aside.classList.add('mdc-drawer--opening');
        console.log('modal view tools function ran');
      };

      scrim.onclick = () => {
        console.log('you clicked the scrim to close');
        aside.classList.remove('mdc-drawer--open');
        // drawer.classList.add('op')
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

  render() {
    const { error, loading } = this.props;

    const loadingMessage = (
        <div className="catalog-component__loading">
          <img src={loadingImage} alt="Holodeck Loading..." className="holodeck-loading-image" />
        </div>
      );

    let dismissClass;

    if (this.state.toolDrawerView !== 'modal') {
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
        />

        <HeaderContainer view={this.state.toolDrawerView} />

        {/*<div className={dismissClass} id="dismiss-class">*/}
          <div className={`catalog ${dismissClass}`} id="dismiss-class">
            <ul className='catalog-list mdc-image-list mdc-image-list--with-text-protection'>
              {this.props.visibleCollections ? this.props.visibleCollections.map(collectionId =>
                <CatalogCardContainer collection={this.props.collections[collectionId]} key={collectionId} match={this.props.match} history={this.props.history} />
              ) : loadingMessage}
            </ul>
          </div>
          <Footer view={this.state.toolDrawerView} />
        {/*</div>*/}
      </div>
    );
  }
}
