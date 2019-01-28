import { connect } from 'react-redux';

import CollectionSearcher from '../components/CollectionSearcher';
import {
  catalogActions,
  collectionActions,
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
  view: state.catalog.view
});

const mapDispatchToProps = dispatch => ({
  clearSelectedCollection: () => {
    dispatch(collectionActions.clearSelectedCollection());
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
    dispatch(urlTrackerActions.setUrl(newUrl, history));
  },
  logFilterChange: (url) => {
    dispatch(urlTrackerActions.logFilterChange(url));
  },
  setViewCatalog: () => {
    dispatch(catalogActions.setViewCatalog());
  }
})

const CollectionSearcherContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(CollectionSearcher);

export default CollectionSearcherContainer;
