import { connect } from 'react-redux';

import { collectionFilterMapDialogActions } from '../actions';
import CollectionFilterMapDialog from '../components/CollectionFilterMapDialog';
import { getAllCollections } from '../selectors/collectionSelectors';

const mapStateToProps = state => ({
  collections: getAllCollections(state),
  showCollectionFilterMapDialog: state.collectionFilterMapDialog.showCollectionFilterMapDialog
});

const mapDispatchToProps = dispatch => ({
  closeCollectionFilterMapDialog: () => {
    dispatch(collectionFilterMapDialogActions.closeCollectionFilterMapDialog());
  }
})

const CollectionFilterMapDialogContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(CollectionFilterMapDialog);

export default CollectionFilterMapDialogContainer;
