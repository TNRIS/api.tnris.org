import { connect } from 'react-redux';

import {
  collectionActions,
  collectionFilterMapActions,
} from '../actions';
import CollectionFilterMap from '../components/CollectionFilterMap';
import { getAllCollectionIds } from '../selectors/collectionSelectors';

const mapStateToProps = state => ({
  allCollectionIds: getAllCollectionIds(state),
  collectionFilterMapCenter: state.collectionFilterMap.collectionFilterMapCenter,
  collectionFilterMapFilter: state.collectionFilterMap.collectionFilterMapFilter,
  collectionFilterMapZoom: state.collectionFilterMap.collectionFilterMapZoom,

});

const mapDispatchToProps = dispatch => ({
  fetchCollections: () => {
    dispatch(collectionActions.fetchCollections());
  },
  setCollectionFilterMapCenter: (collectionFilterMapCenter) => {
    dispatch(collectionFilterMapActions.setCollectionFilterMapCenter(collectionFilterMapCenter));
  },
  setCollectionFilterMapFilter: (collectionFilterMapFilter) => {
    dispatch(collectionFilterMapActions.setCollectionFilterMapFilter(collectionFilterMapFilter));
  },
  setCollectionFilterMapZoom: (collectionFilterMapZoom) => {
    dispatch(collectionFilterMapActions.setCollectionFilterMapZoom(collectionFilterMapZoom));
  }
})

const CollectionFilterMapContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(CollectionFilterMap);

export default CollectionFilterMapContainer;
