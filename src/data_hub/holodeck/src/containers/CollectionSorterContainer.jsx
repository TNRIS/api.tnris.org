import { connect } from 'react-redux';

import { collectionSorterActions, urlTrackerActions } from '../actions';
import CollectionSorter from '../components/CollectionSorter';

const mapStateToProps = state => ({
  sortOrder: state.collectionSorter.sortOrder
});

const mapDispatchToProps = dispatch => ({
  sortAZ: () => {
    dispatch(collectionSorterActions.setSortAZ());
  },
  sortZA: () => {
    dispatch(collectionSorterActions.setSortZA());
  },
  sortNew: () => {
    dispatch(collectionSorterActions.setSortNew());
  },
  sortOld: () => {
    dispatch(collectionSorterActions.setSortOld());
  },
  setUrl: (newUrl, history) => {
    dispatch(urlTrackerActions.setUrl(newUrl, history));
  },
  logFilterChange: (url) => {
    dispatch(urlTrackerActions.logFilterChange(url));
  }
})

const CollectionSorterContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(CollectionSorter);

export default CollectionSorterContainer;
