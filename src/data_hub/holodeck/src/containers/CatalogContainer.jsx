import { connect } from 'react-redux';
import {
  getAllCollections,
  // getVisibleCollections,
  sortCollections
} from '../selectors/collectionSelectors';

import {
  collectionActions,
  resourceActions,
  collectionDialogActions,
  mapDialogActions } from '../actions';

import Catalog from '../components/Catalog';

const mapStateToProps = (state) => ({
  collections: getAllCollections(state),
  // visibleCollections: getVisibleCollections(state),
  visibleCollections: sortCollections(state),
  resources: state.resources.items,
  loading: state.collections.loading,
  error: state.collections.error,
  showCollectionDialog: state.collectionDialog.showCollectionDialog,
  showMapDialog: state.mapDialog.showMapDialog,
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
  openMapDialog: () => {
    dispatch(mapDialogActions.openMapDialog());
  }
})

const CatalogContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(Catalog);

export default CatalogContainer;
