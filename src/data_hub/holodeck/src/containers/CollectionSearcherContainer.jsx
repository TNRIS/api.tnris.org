import { connect } from 'react-redux';

import CollectionSearcher from '../components/CollectionSearcher';
import { collectionSearcherActions } from '../actions';

const mapStateToProps = (state) => ({
  collectionSearchQuery: state.collectionSearcher.collectionSearchQuery
});

const mapDispatchToProps = dispatch => ({
  setCollectionSearchQuery: (collectionSearchQuery) => {
    dispatch(collectionSearcherActions.setCollectionSearchQuery(collectionSearchQuery));
  }
})

const CollectionSearcherContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(CollectionSearcher);

export default CollectionSearcherContainer;
