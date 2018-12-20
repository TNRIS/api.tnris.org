import { connect } from 'react-redux';

import {
  collectionSearcherActions,
  sortActions,
  collectionFilterActions,
  collectionFilterMapActions,
  collectionTimesliderActions,
  urlTrackerActions
} from '../actions';
import { getCollectionTimesliderRange } from '../selectors/collectionSelectors';

import ToolDrawer from '../components/ToolDrawer';

const mapStateToProps = (state) => ({
  collectionTimesliderRange: getCollectionTimesliderRange(state)
});

const mapDispatchToProps = dispatch => ({
  setCollectionSearchQuery: (collectionSearchQuery) => {
    dispatch(collectionSearcherActions.setCollectionSearchQuery(collectionSearchQuery));
  },
  sortNew: () => {
    dispatch(sortActions.setSortNew());
  },
  setCollectionFilter: (collectionFilter) => {
    dispatch(collectionFilterActions.setCollectionFilter(collectionFilter));
  },
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
  },
  setCollectionTimeslider: (collectionTimeslider) => {
    dispatch(collectionTimesliderActions.setCollectionTimeslider(collectionTimeslider));
  },
  setUrl: (newUrl, history) => {
    dispatch(urlTrackerActions.setUrl(newUrl, history))
  }
})

const ToolDrawerContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(ToolDrawer);

export default ToolDrawerContainer;
