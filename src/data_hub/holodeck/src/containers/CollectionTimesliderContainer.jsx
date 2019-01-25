import { connect } from 'react-redux';

import CollectionTimeslider from '../components/CollectionTimeslider';
import { collectionTimesliderActions, urlTrackerActions } from '../actions';
import { getCollectionTimesliderRange } from '../selectors/collectionSelectors';

const mapStateToProps = (state) => ({
  collectionTimeslider: state.collectionTimeslider.collectionTimeslider,
  collectionTimesliderRange: getCollectionTimesliderRange(state)
});

const mapDispatchToProps = dispatch => ({
  setCollectionTimeslider: (collectionTimeslider) => {
    dispatch(collectionTimesliderActions.setCollectionTimeslider(collectionTimeslider));
  },
  setUrl: (newUrl, history) => {
    dispatch(urlTrackerActions.setUrl(newUrl, history))
  },
  logFilterChange: (url) => {
    dispatch(urlTrackerActions.logFilterChange(url));
  }
})

const CollectionTimesliderContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(CollectionTimeslider);

export default CollectionTimesliderContainer;
