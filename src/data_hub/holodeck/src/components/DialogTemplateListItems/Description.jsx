import React from 'react';

export default class Description extends React.Component {

  render() {
    const oe_service_names = this.props.collection.oe_service_names ? (
      <p><strong>Available services include:</strong> {this.props.collection.oe_service_names}</p>
      ) : '';

      // create service name and url arrays from aggregated string
      const names = this.props.collection.oe_service_names.split(', ');
      const services = this.props.collection.oe_service_urls.split(', ');

      // test log to see if service name and url array order matches
      console.log(names[70], services[70]);

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
