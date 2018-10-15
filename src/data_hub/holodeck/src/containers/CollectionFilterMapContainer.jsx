import { connect } from 'react-redux';

import {
  collectionActions,
  collectionFilterMapActions,
  resourceActions
} from '../actions';
import CollectionFilterMap from '../components/CollectionFilterMap';
import { getAllCollections } from '../selectors/collectionSelectors';
import { getAllResources } from '../selectors/resourceSelectors';

const mapStateToProps = state => ({
  collectionFilterMapFilter: state.collectionFilterMap.collectionFilterMapFilter,
  collections: getAllCollections(state),
  resources: getAllResources(state),
});

const mapDispatchToProps = dispatch => ({
  fetchCollections: () => {
    dispatch(collectionActions.fetchCollections());
  },
  fetchResources: () => {
    dispatch(resourceActions.fetchResources());
  },
  setCollectionFilterMapFilter: (collectionFilterMapFilter) => {
    dispatch(collectionFilterMapActions.setCollectionFilterMapFilter(collectionFilterMapFilter));
  }
})

const CollectionFilterMapContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(CollectionFilterMap);

export default CollectionFilterMapContainer;
