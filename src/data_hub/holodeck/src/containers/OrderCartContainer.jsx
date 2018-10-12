import { connect } from 'react-redux';

import OrderCart from '../components/OrderCart';

const mapStateToProps = state => ({
});

const mapDispatchToProps = dispatch => ({
})

const OrderCartContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(OrderCart);

export default OrderCartContainer;
