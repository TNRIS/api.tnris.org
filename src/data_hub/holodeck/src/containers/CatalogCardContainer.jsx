import { connect } from 'react-redux';

import { collectionActions } from '../actions';
import { dialogActions } from '../actions';
import CatalogCard from '../components/CatalogCard';

const mapStateToProps = state => ({
  showDialog: state.dialog.showDialog,
  selectedCollection: state.collections.selectedCollection
});

const mapDispatchToProps = (dispatch) => ({
    openDialog: () => {
      dispatch(dialogActions.openDialog());
    },
    closeDialog: () => {
      dispatch(dialogActions.closeDialog());
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
