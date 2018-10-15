import { connect } from 'react-redux';

import {
  collectionFilterActions,
  collectionFilterMapDialogActions
} from '../actions';
import CollectionFilter from '../components/CollectionFilter';
import { getCollectionFilterChoices } from '../selectors/collectionSelectors';

const mapStateToProps = (state) => ({
  collectionFilter: state.collectionFilter.collectionFilter,
  collectionFilterChoices: getCollectionFilterChoices(state),
  showCollectionFilterMapDialog: state.collectionFilterMapDialog.showCollectionFilterMapDialog
});

const mapDispatchToProps = dispatch => ({
  setCollectionFilter: (collectionFilter) => {
    dispatch(collectionFilterActions.setCollectionFilter(collectionFilter));
  },
  openCollectionFilterMapDialog: () => {
    dispatch(collectionFilterMapDialogActions.openCollectionFilterMapDialog());
  }
})

const CollectionFilterContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(CollectionFilter);

export default CollectionFilterContainer;
