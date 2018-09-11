import { connect } from 'react-redux';

import { sortActions } from '../actions';
import Sort from '../components/Sort';

const mapStateToProps = state => ({
  sortOrder: state.sorter.sorter
});

const mapDispatchToProps = dispatch => ({
  sortAZ: () => {
    dispatch(sortActions.setSortAZ());
  },
  sortZA: () => {
    dispatch(sortActions.setSortZA());
  }
})

const SortContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(Sort);

export default SortContainer;
