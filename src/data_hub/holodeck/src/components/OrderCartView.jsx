import React from 'react';
import OrderCartContainer from '../containers/OrderCartContainer';

class OrderCartView extends React.Component {
    render() {
      return (
        <div className="order-cart-view">
          <h2 className="mdc-top-app-bar__title">
            Shopping Cart
          </h2>
          <OrderCartContainer history={this.props.history} />
        </div>
      );
    }
}

export default OrderCartView;
