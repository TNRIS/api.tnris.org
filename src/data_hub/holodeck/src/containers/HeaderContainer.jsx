import { connect } from 'react-redux';

import { orderCartDialogActions } from '../actions';
import Header from '../components/Header';

import {
  getSortedCollections
} from '../selectors/collectionSelectors';

const mapStateToProps = state => ({
  orders: state.orderCart.orders,
  visibleCollections: getSortedCollections(state)
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
