import { connect } from 'react-redux';

import {
  collectionSearcherActions,
  sortActions,
  collectionFilterActions,
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
  sortAZ: () => {
    dispatch(sortActions.setSortAZ());
  },
  setCollectionFilter: (collectionFilter) => {
    dispatch(collectionFilterActions.setCollectionFilter(collectionFilter));
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
