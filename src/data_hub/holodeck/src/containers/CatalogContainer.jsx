import { connect } from 'react-redux';

import Catalog from '../components/Catalog';
import {
  catalogActions,
  collectionActions,
  orderCartActions,
  resourceActions,
  toolDrawerActions,
  urlTrackerActions } from '../actions';
import {
  getAllCollections,
  getSortedCollections
} from '../selectors/collectionSelectors';

const mapStateToProps = (state) => ({
  collections: getAllCollections(state),
  error: state.collections.error,
  loading: state.collections.loading,
  resources: state.resources.items,
  selectedCollection: state.collections.selectedCollection,
  sortOrder: state.collectionSorter.sortOrder,
  visibleCollections: getSortedCollections(state),
  theme: state.colorTheme.theme,
  previousUrl: state.urlTracker.previousUrl,
  toolDrawerStatus: state.toolDrawer.toolDrawerStatus,
  view: state.catalog.view
});

const mapDispatchToProps = dispatch => ({
  clearSelectedCollection: () => {
    dispatch(collectionActions.clearSelectedCollection());
  },
  closeToolDrawer: () => {
    dispatch(toolDrawerActions.closeToolDrawer());
  },
  fetchCollections: () => {
    dispatch(collectionActions.fetchCollections());
  },
  fetchResources: () => {
    dispatch(resourceActions.fetchResources());
  },
  fetchStoredShoppingCart: () => {
    dispatch(orderCartActions.fetchStoredShoppingCart());
  },
  openToolDrawer: () => {
    dispatch(toolDrawerActions.openToolDrawer());
  },
  setUrl: (newUrl, history) => {
    dispatch(urlTrackerActions.setUrl(newUrl, history))
  },
  setViewCatalog: () => {
    dispatch(catalogActions.setViewCatalog());
  }
})

const CatalogContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(Catalog);

export default CatalogContainer;
