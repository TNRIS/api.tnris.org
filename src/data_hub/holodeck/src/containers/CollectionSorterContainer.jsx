import { connect } from 'react-redux';

import { sortActions } from '../actions';
import CollectionSorter from '../components/CollectionSorter';

const mapStateToProps = state => ({
  sortOrder: state.sorter.sortOrder
});

const mapDispatchToProps = dispatch => ({
  sortAZ: () => {
    dispatch(sortActions.setSortAZ());
  },
  sortZA: () => {
    dispatch(sortActions.setSortZA());
  },
  sortNew: () => {
    dispatch(sortActions.setSortNew());
  },
  sortOld: () => {
    dispatch(sortActions.setSortOld());
  }
})

const CollectionSorterContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(CollectionSorter);

export default CollectionSorterContainer;
