import { connect } from 'react-redux';

import CollectionSearcher from '../components/CollectionSearcher';
import {
  collectionSearcherActions,
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
  collectionSearchSuggestionsQuery: state.collectionSearcher.collectionSearchSuggestionsQuery
});

const mapDispatchToProps = dispatch => ({
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
  }
})

const CollectionSearcherContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(CollectionSearcher);

export default CollectionSearcherContainer;
