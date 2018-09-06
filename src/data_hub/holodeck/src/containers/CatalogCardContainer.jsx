import { connect } from 'react-redux';

import { collectionActions } from '../actions';
import { collectionDialogActions } from '../actions';
import CatalogCard from '../components/CatalogCard';

const mapStateToProps = state => ({
  showCollectionDialog: state.collectionDialog.showCollectionDialog,
  selectedCollection: state.collections.selectedCollection
});

const mapDispatchToProps = (dispatch) => ({
    openCollectionDialog: () => {
      dispatch(collectionDialogActions.openCollectionDialog());
    },
    closeCollectionDialog: () => {
      dispatch(collectionDialogActions.closeCollectionDialog());
    },
    selectCollection: (collectionId) => {
      dispatch(collectionActions.selectCollection(collectionId));
    }
})

const CatalogCardContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(CatalogCard);

export default CatalogCardContainer;
