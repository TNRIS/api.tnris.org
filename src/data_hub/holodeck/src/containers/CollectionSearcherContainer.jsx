import { connect } from 'react-redux';

import CollectionSearcher from '../components/CollectionSearcher';
import {
  collectionActions,
  collectionDialogActions,
  collectionSearcherActions,
  toolDrawerActions,
  urlTrackerActions
} from '../actions';
import {
  getAllCollections,
  getSearchSuggestions
} from '../selectors/collectionSelectors';

const mapStateToProps = (state) => ({
  collections: getAllCollections(state),
  collectionSearchQuery: state.collectionSearcher.collectionSearchQuery,
  collectionSearchSuggestions: getSearchSuggestions(state),
  collectionSearchSuggestionsQuery: state.collectionSearcher.collectionSearchSuggestionsQuery,
  showCollectionDialog: state.collectionDialog.showCollectionDialog
});

const mapDispatchToProps = dispatch => ({
  clearSelectedCollection: () => {
    dispatch(collectionActions.clearSelectedCollection());
  },
  closeCollectionDialog: () => {
    dispatch(collectionDialogActions.closeCollectionDialog());
  },
  openToolDrawer: () => {
    dispatch(toolDrawerActions.openToolDrawer());
  },
  setCollectionSearchQuery: (collectionSearchQuery) => {
    dispatch(collectionSearcherActions.setCollectionSearchQuery(collectionSearchQuery));
  },
  setCollectionSearchSuggestionsQuery: (collectionSearchSuggestionsQuery) => {
    dispatch(collectionSearcherActions.setCollectionSearchSuggestionsQuery(collectionSearchSuggestionsQuery));
  },
  setUrl: (newUrl, history) => {
    dispatch(urlTrackerActions.setUrl(newUrl, history))
  }
})

const CollectionSearcherContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(CollectionSearcher);

export default CollectionSearcherContainer;
