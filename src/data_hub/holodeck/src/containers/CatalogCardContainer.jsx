import { connect } from 'react-redux';

import { collectionActions,
         collectionDialogActions,
         urlTrackerActions } from '../actions';
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
    },
    fetchCollectionResources: (collectionId) => {
      dispatch(collectionActions.fetchCollectionResources(collectionId))
    },
    setUrl: (newUrl, history) => {
      dispatch(urlTrackerActions.setUrl(newUrl, history))
    }
})

const CatalogCardContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(CatalogCard);

export default CatalogCardContainer;
