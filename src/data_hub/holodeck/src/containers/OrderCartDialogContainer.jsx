import { connect } from 'react-redux';

import { orderCartDialogActions } from '../actions';
import OrderCartDialog from '../components/OrderCartDialog';

const mapStateToProps = state => ({
  showOrderCartDialog: state.orderCart.showOrderCartDialog,
});

const mapDispatchToProps = dispatch => ({
  closeOrderCartDialog: () => {
    dispatch(orderCartDialogActions.closeOrderCartDialog());
  }
})

const OrderCartDialogContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(OrderCartDialog);

export default OrderCartDialogContainer;
