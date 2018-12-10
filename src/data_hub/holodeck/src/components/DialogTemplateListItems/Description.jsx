import React from 'react';

export default class Description extends React.Component {

  render() {
    const oe_service_names = this.props.collection.oe_service_names ? (
      <p><strong>Available services include:</strong> {this.props.collection.oe_service_names}</p>
      ) : '';

    return (
      <div className="template-content-div">
        <div className='mdc-typography--headline5 template-content-div-header'>
          Description
        </div>
        <p>
          {this.props.collection.description}
        </p>
        {oe_service_names}
      </div>
    )
  }
}
