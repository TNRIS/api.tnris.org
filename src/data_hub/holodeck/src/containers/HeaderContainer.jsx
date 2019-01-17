import { connect } from 'react-redux';

import { collectionActions,
         collectionDialogActions,
         orderCartDialogActions,
         toolDrawerActions,
         urlTrackerActions } from '../actions';
import Header from '../components/Header';

const mapStateToProps = state => ({
  orders: state.orderCart.orders,
  previousUrl: state.urlTracker.previousUrl,
  selectedCollection: state.collections.selectedCollection,
  showCollectionDialog: state.collectionDialog.showCollectionDialog,
  showOrderCartDialog: state.orderCart.showOrderCartDialog,
  theme: state.colorTheme.theme
});

const mapDispatchToProps = dispatch => ({
  clearSelectedCollection: () => {
    dispatch(collectionActions.clearSelectedCollection());
  },
  closeCollectionDialog: () => {
    dispatch(collectionDialogActions.closeCollectionDialog());
  },
  openOrderCartDialog: () => {
    dispatch(orderCartDialogActions.openOrderCartDialog());
  },
  closeOrderCartDialog: () => {
    dispatch(orderCartDialogActions.closeOrderCartDialog());
  },
  openToolDrawer: () => {
    dispatch(toolDrawerActions.openToolDrawer());
  },
  setUrl: (newUrl, history) => {
    dispatch(urlTrackerActions.setUrl(newUrl, history))
  }
})

const HeaderContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(Header);

export default HeaderContainer;
