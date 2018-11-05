import React from 'react';

import OrderTnrisDataFormContainer from '../../containers/OrderTnrisDataFormContainer';

export default class TnrisOrderTemplateOrder extends React.Component {
  render() {

    return (
      <div className="tnris-download-template-details">
        <div className="template-content-div">
          <div className='mdc-typography--headline5 template-content-div-header' onClick={this.toggleOrder}>
            Order
          </div>
          <div>
            <OrderTnrisDataFormContainer />
          </div>
        </div>
      </div>

    );
  }
}
