import { connect } from 'react-redux';

import { collectionActions } from '../actions';
import { dialogActions } from '../actions';
import Dialog from '../components/Dialog';

const mapStateToProps = state => ({
  collections: state.collections.items,
  selectedCollection: state.collections.selectedCollection,
  showDialog: state.dialog.showDialog
});

const mapDispatchToProps = dispatch => ({
  closeDialog: () => {
    dispatch(dialogActions.closeDialog());
    // dispatch(collectionActions.clearSelectedCollection());
  },
  clearSelectedCollection: () => {
    dispatch(collectionActions.clearSelectedCollection());
  }
})

const DialogContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(Dialog);

export default DialogContainer;
