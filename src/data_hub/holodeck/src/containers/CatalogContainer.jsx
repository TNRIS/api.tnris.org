import { connect } from 'react-redux';

import Catalog from '../components/Catalog';
import {
  collectionActions,
  collectionDialogActions,
  orderCartActions,
  resourceActions,
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
  showCollectionDialog: state.collectionDialog.showCollectionDialog,
  sortOrder: state.collectionSorter.sortOrder,
  visibleCollections: getSortedCollections(state),
  theme: state.colorTheme.theme,
  previousUrl: state.urlTracker.previousUrl,
});

const mapDispatchToProps = dispatch => ({
  clearSelectedCollection: () => {
    dispatch(collectionActions.clearSelectedCollection());
  },
  closeCollectionDialog: () => {
    dispatch(collectionDialogActions.closeCollectionDialog());
  },
  fetchCollections: () => {
    dispatch(collectionActions.fetchCollections());
  },
  fetchResources: () => {
    dispatch(resourceActions.fetchResources());
  },
  openCollectionDialog: () => {
    dispatch(collectionDialogActions.openCollectionDialog());
  },
  fetchStoredShoppingCart: () => {
    dispatch(orderCartActions.fetchStoredShoppingCart());
  },
  setUrl: (newUrl, history) => {
    dispatch(urlTrackerActions.setUrl(newUrl, history))
  }
})

const CatalogContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(Catalog);

export default CatalogContainer;
