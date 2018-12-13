import React from 'react';

export default class Description extends React.Component {

  render() {

    // create service name and url arrays from aggregated string
    const namesArray = this.props.collection.oe_service_names ? this.props.collection.oe_service_names.split(', ') : '';
    const servicesArray = this.props.collection.oe_service_urls ? this.props.collection.oe_service_urls.split(', ') : '';

    const services = namesArray ? (
      <div id="oe_services">
        <p><strong>Available services include:</strong></p>
        <ul>
          {
            namesArray.map((i) => {
              return <li key={i}><a href="" target="_blank">{i}</a></li>;
            })
          }
        </ul>
      </div>
      ) : '';

    return (
      <div className="template-content-div">
        <div className='mdc-typography--headline5 template-content-div-header'>
          Description
        </div>
        <p>
          {this.props.collection.description}
        </p>
        {services}
      </div>
    )
  }
}
