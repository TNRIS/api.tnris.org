import { connect } from 'react-redux';

import { collectionActions, collectionDialogActions, urlTrackerActions } from '../actions';
import { getAllCollections } from '../selectors/collectionSelectors';
import CollectionDialog from '../components/CollectionDialog';

const mapStateToProps = state => ({
  collections: getAllCollections(state),
  selectedCollection: state.collections.selectedCollection,
  showCollectionDialog: state.collectionDialog.showCollectionDialog,
  previousUrl: state.urlTracker.previousUrl
});

const mapDispatchToProps = dispatch => ({
  closeCollectionDialog: () => {
    dispatch(collectionDialogActions.closeCollectionDialog());
  },
  clearSelectedCollection: () => {
    dispatch(collectionActions.clearSelectedCollection());
  },
  setUrl: (newUrl, history) => {
    dispatch(urlTrackerActions.setUrl(newUrl, history))
  }
})

const CollectionDialogContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(CollectionDialog);

export default CollectionDialogContainer;
