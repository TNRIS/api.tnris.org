import { connect } from 'react-redux';

import {
  collectionFilterMapActions,
} from '../actions';
import CollectionFilterMap from '../components/CollectionFilterMap';

const mapStateToProps = state => ({
  collectionFilterMapAoi: state.collectionFilterMap.collectionFilterMapAoi,
  collectionFilterMapCenter: state.collectionFilterMap.collectionFilterMapCenter,
  collectionFilterMapFilter: state.collectionFilterMap.collectionFilterMapFilter,
  collectionFilterMapZoom: state.collectionFilterMap.collectionFilterMapZoom,
});

const mapDispatchToProps = dispatch => ({
  setCollectionFilterMapAoi: (collectionFilterMapAoi) => {
    dispatch(collectionFilterMapActions.setCollectionFilterMapAoi(collectionFilterMapAoi));
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
