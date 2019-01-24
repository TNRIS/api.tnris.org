import { connect } from 'react-redux';

import {
  catalogActions,
  collectionFilterActions,
  collectionFilterMapActions,
  urlTrackerActions
} from '../actions';
import CollectionFilter from '../components/CollectionFilter';
import { getCollectionFilterChoices } from '../selectors/collectionSelectors';

const mapStateToProps = (state) => ({
  collectionFilter: state.collectionFilter.collectionFilter,
  collectionFilterChoices: getCollectionFilterChoices(state),
  collectionFilterMapFilter: state.collectionFilterMap.collectionFilterMapFilter
});

const mapDispatchToProps = dispatch => ({
  setCollectionFilter: (collectionFilter) => {
    dispatch(collectionFilterActions.setCollectionFilter(collectionFilter));
  },
  setUrl: (newUrl, history) => {
    dispatch(urlTrackerActions.setUrl(newUrl, history))
  },
  logFilterChange: (url) => {
    dispatch(urlTrackerActions.logFilterChange(url));
  },
  setCollectionFilterMapAoi: (collectionFilterMapAoi) => {
    dispatch(collectionFilterMapActions.setCollectionFilterMapAoi(collectionFilterMapAoi));
  },
  setCollectionFilterMapFilter: (collectionFilterMapFilter) => {
    dispatch(collectionFilterMapActions.setCollectionFilterMapFilter(collectionFilterMapFilter));
  },
  setViewGeoFilter: () => {
    dispatch(catalogActions.setViewGeoFilter());
  }
})

const CollectionFilterContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(CollectionFilter);

export default CollectionFilterContainer;
