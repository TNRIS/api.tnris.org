import React from 'react';
import OrderCartContainer from '../containers/OrderCartContainer';

class OrderCartDialog extends React.Component {

    componentDidMount() {
      console.log('order cart mount');
    }

    render() {
      return (
        <div className="order-cart-dialog">
          <h2 className="mdc-top-app-bar__title">
            Shopping Cart
          </h2>
          <OrderCartContainer />
        </div>
      );
    }
}

export default OrderCartDialog;
