import { connect } from 'react-redux';

import { orderCartActions } from '../actions';
import { getAllCollections } from '../selectors/collectionSelectors';
import OrderTnrisDataForm from '../components/OrderTnrisDataForm';

const mapStateToProps = state => ({
  collections: getAllCollections(state),
  selectedCollection: state.collections.selectedCollection,
  orders: state.orderCart.orders
});

const mapDispatchToProps = dispatch => ({
  addCollectionToCart: (collectionId, formInfo) => {
    dispatch(orderCartActions.addCollectionToCart(collectionId, formInfo));
  }
})

const OrderTnrisDataFormContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(OrderTnrisDataForm);

export default OrderTnrisDataFormContainer;
