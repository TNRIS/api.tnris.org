import React from 'react';

import OrderTnrisDataFormContainer from '../../containers/OrderTnrisDataFormContainer';

export default class TnrisOrderTemplateOrder extends React.Component {
  render() {

    return (
      <div className="tnris-download-template-details">
        <div className="template-content-div">
          <div>
            <OrderTnrisDataFormContainer />
          </div>
        </div>
      </div>

    );
  }
}
