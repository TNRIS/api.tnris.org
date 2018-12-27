import { connect } from 'react-redux';

import { collectionActions,
         collectionDialogActions,
         toolDrawerActions,
         urlTrackerActions } from '../actions';
import CatalogCard from '../components/CatalogCard';

const mapStateToProps = state => ({
  showCollectionDialog: state.collectionDialog.showCollectionDialog,
  selectedCollection: state.collections.selectedCollection
});

const mapDispatchToProps = (dispatch) => ({
    closeCollectionDialog: () => {
      dispatch(collectionDialogActions.closeCollectionDialog());
    },
    closeToolDrawer: () => {
      dispatch(toolDrawerActions.closeToolDrawer());
    },
    fetchCollectionResources: (collectionId) => {
      dispatch(collectionActions.fetchCollectionResources(collectionId))
    },
    openCollectionDialog: () => {
      dispatch(collectionDialogActions.openCollectionDialog());
    },
    selectCollection: (collectionId) => {
      dispatch(collectionActions.selectCollection(collectionId));
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
