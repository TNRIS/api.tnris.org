import React from 'react';

export default class Description extends React.Component {

  render() {

    // create service name and url arrays from aggregated string
    const namesArray = this.props.collection.oe_service_names !== null ? this.props.collection.oe_service_names.split(', ') : [];
    const servicesArray = this.props.collection.oe_service_urls !== null ? this.props.collection.oe_service_urls.split(', ') : [];

    const servicesObj = {};

    namesArray.map((key) => {
      const compare = key.split(' ').join('_');
      servicesArray.map((service) => {
        const stringArray = service.split("/");
        stringArray.map((i) => {
          if (i === compare) {
            servicesObj[key] = servicesArray[servicesArray.indexOf(service)];
          }
          return i;
        })
        return service;
      })
      return key;
    });

    const services = namesArray.length !== 0 ? (
      <div id="oe_services">
        <p>Currently, there are <strong>{namesArray.length}</strong> available services that you can access below, or by visiting TxDOT's open data portal at the link above.</p>
        <ul>
          {
            Object.entries(servicesObj).map((i) => {
              let key = i[0];
              let value = i[1];
              return <li key={key}><a href={value} target="_blank">{key}</a></li>;
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
