import { connect } from 'react-redux';

import { collectionActions, collectionDialogActions } from '../actions';
import CollectionDialog from '../components/CollectionDialog';

const mapStateToProps = state => ({
  collections: state.collections.items,
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
