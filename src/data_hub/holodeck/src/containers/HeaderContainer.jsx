import { connect } from 'react-redux';

import { orderCartDialogActions } from '../actions';
import Header from '../components/Header';

const mapStateToProps = state => ({
  orders: state.orderCart.orders
});

const mapDispatchToProps = dispatch => ({
  openOrderCartDialog: () => {
    dispatch(orderCartDialogActions.openOrderCartDialog());
  }
})

const HeaderContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(Header);

export default HeaderContainer;
