import React from 'react';

export default class HistoricalProducts extends React.Component {
  render() {
    const printTypes = {
      'B&W': 'Black & White',
      'NC': 'Natural Color',
      'CIR': 'Color Infrared'
    };

    const products = JSON.parse("[" + this.props.products + "]");
    let uniqueProducts = [];
    products.map(product => {
      let p = product.medium + "," + printTypes[product.print_type];
      if (uniqueProducts.indexOf(p) === -1) {
        uniqueProducts.push(p);
      }
      return true;
    })

    return (
      <div className="template-content-div historical-products">
        <div className='mdc-typography--headline5 template-content-div-header'>
          Historical Imagery Products
        </div>
        <p className="mdc-typography--body2">
          Many historical imagery projects occasionally produced multiple printed photographs of the same imagery varying in scale and frame size. The available printed photograph products for this dataset are listed below.
        </p>
        <ul className="mdc-list product-table">
            <li className="mdc-list-item product-table-header">
              <div>Product #</div>
              <div>Medium</div>
              <div>Print Type</div>
            </li>
            {uniqueProducts.map((product, index) =>
              <li key={product} className="mdc-list-item">
                <div>{index + 1}</div>
                <div>{product.split(",")[0]}</div>
                <div>{product.split(",")[1]}</div>
              </li>
            )}
        </ul>
      </div>
    )
  }
}
