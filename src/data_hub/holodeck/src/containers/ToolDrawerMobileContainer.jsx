import { connect } from 'react-redux';

import {
  collectionFilterActions,
  collectionFilterMapActions,
  collectionSorterActions,
  collectionTimesliderActions,
  toolDrawerActions,
  urlTrackerActions
} from '../actions';
import { getCollectionTimesliderRange } from '../selectors/collectionSelectors';

import ToolDrawerMobile from '../components/ToolDrawerMobile';

const mapStateToProps = (state) => ({
  collectionTimesliderRange: getCollectionTimesliderRange(state),
  toolDrawerStatus: state.toolDrawer.toolDrawerStatus
});

const mapDispatchToProps = dispatch => ({
  sortNew: () => {
    dispatch(collectionSorterActions.setSortNew());
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
  },
  logFilterChange: (url) => {
    dispatch(urlTrackerActions.logFilterChange(url));
  },
  closeToolDrawer: () => {
    dispatch(toolDrawerActions.closeToolDrawer());
  }
})

const ToolDrawerMobileContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(ToolDrawerMobile);

export default ToolDrawerMobileContainer;
