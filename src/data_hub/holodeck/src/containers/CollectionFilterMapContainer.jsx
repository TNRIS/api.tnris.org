import { connect } from 'react-redux';

import { collectionActions, resourceActions } from '../actions';
import CollectionFilterMap from '../components/CollectionFilterMap';

const mapStateToProps = state => ({
  collections: state.collections.items,
  resources: state.resources.items,
  loading: state.collections.loading,
  error: state.collections.error
});

const mapDispatchToProps = dispatch => ({
  fetchCollections: () => {
    dispatch(collectionActions.fetchCollections());
  },
  fetchResources: () => {
    dispatch(resourceActions.fetchResources());
  }
})

const CollectionFilterMapContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(CollectionFilterMap);

export default CollectionFilterMapContainer;
