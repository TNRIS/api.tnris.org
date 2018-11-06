import { connect } from 'react-redux';

import CollectionFilter from '../components/CollectionFilter';
import { collectionFilterActions, urlTrackerActions } from '../actions';
import { getCollectionFilterChoices } from '../selectors/collectionSelectors';

const mapStateToProps = (state) => ({
  collectionFilter: state.collectionFilter.collectionFilter,
  collectionFilterChoices: getCollectionFilterChoices(state)
});

const mapDispatchToProps = dispatch => ({
  setCollectionFilter: (collectionFilter) => {
    dispatch(collectionFilterActions.setCollectionFilter(collectionFilter));
  },
  setUrl: (newUrl, history) => {
    dispatch(urlTrackerActions.setUrl(newUrl, history))
  }
})

const CollectionFilterContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(CollectionFilter);

export default CollectionFilterContainer;
