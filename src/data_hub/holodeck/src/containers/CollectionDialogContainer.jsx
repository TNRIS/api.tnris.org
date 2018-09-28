import { connect } from 'react-redux';

import { collectionActions, collectionDialogActions } from '../actions';
import { getAllCollections } from '../selectors/collectionSelectors';
import CollectionDialog from '../components/CollectionDialog';

const mapStateToProps = state => ({
  collections: getAllCollections(state),
  selectedCollection: state.collections.selectedCollection,
  showCollectionDialog: state.collectionDialog.showCollectionDialog
});

const mapDispatchToProps = dispatch => ({
  closeCollectionDialog: () => {
    dispatch(collectionDialogActions.closeCollectionDialog());
  },
  clearSelectedCollection: () => {
    dispatch(collectionActions.clearSelectedCollection());
  }
})

const CollectionDialogContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(CollectionDialog);

export default CollectionDialogContainer;
