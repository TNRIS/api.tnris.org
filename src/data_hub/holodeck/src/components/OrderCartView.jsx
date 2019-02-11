import React from 'react';
import OrderCartContainer from '../containers/OrderCartContainer';

class OrderCartView extends React.Component {
  constructor() {
    super();

    this.handleBack = this.handleBack.bind(this);
  }

  handleBack() {
    if (this.props.previousUrl.includes('/catalog/')) {
      this.props.setViewCatalog();
      this.props.openToolDrawer();
      this.props.setUrl(this.props.previousUrl, this.props.history);
    }
    else if (this.props.previousUrl.includes('/collection/')) {
      const collectionUuid = this.props.previousUrl.replace('/collection/', '');
      this.props.setViewCollection();
      this.props.selectCollection(collectionUuid);
      this.props.setUrl(this.props.previousUrl, this.props.history);
    }
    else {
      this.props.setViewCatalog();
      this.props.openToolDrawer();
      this.props.setUrl(this.props.previousUrl, this.props.history);
    }
  }
  

  render() {
    return (
      <div className="order-cart-view">
        <div className="mdc-top-app-bar__row">
          <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-start">
            <h2 className="mdc-top-app-bar__title">
              Shopping Cart
            </h2>
          </section>
          <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-end">
            <button onClick={this.handleBack} className="close-shopping-cart mdc-icon-button material-icons" title="Close shopping cart">close</button>
          </section>
        </div>
        <OrderCartContainer history={this.props.history} />
      </div>
    );
  }
}

export default OrderCartView;
