import { connect } from 'react-redux';

import CollectionSearcher from '../components/CollectionSearcher';
import { collectionSearcherActions, urlTrackerActions } from '../actions';

const mapStateToProps = (state) => ({
  collectionSearchQuery: state.collectionSearcher.collectionSearchQuery
});

const mapDispatchToProps = dispatch => ({
  setCollectionSearchQuery: (collectionSearchQuery) => {
    dispatch(collectionSearcherActions.setCollectionSearchQuery(collectionSearchQuery));
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
