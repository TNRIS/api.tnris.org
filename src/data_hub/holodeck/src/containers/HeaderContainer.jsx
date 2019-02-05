import { connect } from 'react-redux';

import { catalogActions,
         collectionActions,
         toolDrawerActions,
         urlTrackerActions } from '../actions';
import {
  getAllCollections
} from '../selectors/collectionSelectors';
import Header from '../components/Header';

const mapStateToProps = state => ({
  collections: getAllCollections(state),
  orders: state.orderCart.orders,
  previousUrl: state.urlTracker.previousUrl,
  catalogFilterUrl: state.urlTracker.catalogFilterUrl,
  selectedCollection: state.collections.selectedCollection,
  theme: state.colorTheme.theme,
  view: state.catalog.view,
  toolDrawerStatus: state.toolDrawer.toolDrawerStatus
});

const mapDispatchToProps = dispatch => ({
  clearSelectedCollection: () => {
    dispatch(collectionActions.clearSelectedCollection());
  },
  selectCollection: (collectionId) => {
    dispatch(collectionActions.selectCollection(collectionId));
  },
  openToolDrawer: () => {
    dispatch(toolDrawerActions.openToolDrawer());
  },
  closeToolDrawer: () => {
    dispatch(toolDrawerActions.closeToolDrawer());
  },
  setUrl: (newUrl, history) => {
    dispatch(urlTrackerActions.setUrl(newUrl, history));
  },
  clearPreviousUrl: () => {
    dispatch(urlTrackerActions.clearPreviousUrl());
  },
  setViewCatalog: () => {
    dispatch(catalogActions.setViewCatalog());
  },
  setViewOrderCart: () => {
    dispatch(catalogActions.setViewOrderCart());
  },
  setViewCollection: () => {
    dispatch(catalogActions.setViewCollection());
  }
})

const HeaderContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(Header);

export default HeaderContainer;
