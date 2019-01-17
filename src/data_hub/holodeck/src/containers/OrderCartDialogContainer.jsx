import { connect } from 'react-redux';

import OrderCartDialog from '../components/OrderCartDialog';

const mapStateToProps = state => ({
  showOrderCartDialog: state.orderCart.showOrderCartDialog,
});

const mapDispatchToProps = dispatch => ({
})

const OrderCartDialogContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(OrderCartDialog);

export default OrderCartDialogContainer;
