import React from 'react';

export default class Description extends React.Component {

  render() {

    // create service name and url arrays from aggregated string
    const namesArray = this.props.collection.oe_service_names !== null ? this.props.collection.oe_service_names.split(', ') : [];
    const servicesArray = this.props.collection.oe_service_urls !== null ? this.props.collection.oe_service_urls.split(', ') : [];

    // console.log(this.props.collection.oe_service_names === null ? console.log('null') : console.log('not null'));

    // if (servicesArray.length !== 0) {
    //   const s = servicesArray.map((service) => {
    //     console.log('service');
    //     // return service.split("/")[-2];
    //   });
    //   return s;
    // }

    // console.log(s);

    // <a href={s} target="_blank"></a>

    const services = namesArray ? (
      <div id="oe_services">
        <p><strong>Available services include:</strong></p>
        <ul>
          {
            namesArray.map((i) => {
              // return service name with hyperlink to service url, trim whitespaces and replace '_' with ' ' using regex
              return <li key={i}>{i.trim().replace(/ /g,' ')}</li>;
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
