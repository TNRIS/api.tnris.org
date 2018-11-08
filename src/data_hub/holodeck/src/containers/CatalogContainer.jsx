import { connect } from 'react-redux';

import Catalog from '../components/Catalog';
import {
  collectionActions,
  collectionDialogActions,
  orderCartActions,
  resourceActions } from '../actions';
import {
  getAllCollections,
  getSortedCollections
} from '../selectors/collectionSelectors';

const mapStateToProps = (state) => ({
  collections: getAllCollections(state),
  error: state.collections.error,
  loading: state.collections.loading,
  resources: state.resources.items,
  showCollectionDialog: state.collectionDialog.showCollectionDialog,
  sortOrder: state.sorter.sortOrder,
  visibleCollections: getSortedCollections(state),
});

const mapDispatchToProps = dispatch => ({
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
  }
})

const CatalogContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(Catalog);

export default CatalogContainer;
