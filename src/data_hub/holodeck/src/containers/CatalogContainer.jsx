import { connect } from 'react-redux';

import Catalog from '../components/Catalog';
import {
  areaActions,
  collectionActions,
  collectionDialogActions,
  mapDialogActions,
  orderCartActions } from '../actions';
import {
  getAllCollections,
  getSortedCollections
} from '../selectors/collectionSelectors';

const mapStateToProps = (state) => ({
  areas: state.areas.items,
  collections: getAllCollections(state),
  error: state.collections.error,
  loading: state.collections.loading,
  resources: state.resources.items,
  showCollectionDialog: state.collectionDialog.showCollectionDialog,
  sortOrder: state.sorter.sortOrder,
  visibleCollections: getSortedCollections(state),
});

const mapDispatchToProps = dispatch => ({
  fetchAreas: () => {
    dispatch(areaActions.fetchAreas());
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
  openMapDialog: () => {
    dispatch(mapDialogActions.openMapDialog());
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
