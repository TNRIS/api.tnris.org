import { connect } from 'react-redux';

import { mapDialogActions } from '../actions';
import MapDialog from '../components/MapDialog';

const mapStateToProps = state => ({
  collections: state.collections.items,
  showMapDialog: state.mapDialog.showMapDialog
});

const mapDispatchToProps = dispatch => ({
  closeMapDialog: () => {
    dispatch(mapDialogActions.closeMapDialog());
  }
})

const MapDialogContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(MapDialog);

export default MapDialogContainer;
