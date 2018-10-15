import { connect } from 'react-redux';

import OrderCart from '../components/OrderCart';

import { orderCartActions } from '../actions';

const mapStateToProps = state => ({
  orders: state.orderCart.orders
});

const mapDispatchToProps = dispatch => ({
  removeCollectionFromCart: (collectionId) => {
    dispatch(orderCartActions.removeCollectionFromCart(collectionId));
  }
})

const OrderCartContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(OrderCart);

export default OrderCartContainer;
