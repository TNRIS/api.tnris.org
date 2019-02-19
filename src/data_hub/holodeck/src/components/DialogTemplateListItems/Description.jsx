import React from 'react';

// import {MDCMenuSurface} from '@material/menu-surface';

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
      <div id="oe_services mdc-menu-surface--anchor">
        <div className="mdc-menu mdc-menu-surface">
          <p>
            Currently, there are <strong>{namesArray.length}</strong> available services that you can access below, or by
            visiting the agency's <a href="" target="_blank">open data portal</a>.
          </p>
          <ul className="mdc-list" role="menu" aria-hidden="true" aria-orientation="vertical">
            {
              Object.entries(servicesObj).map((i) => {
                let key = i[0];
                // let value = i[1];
                return <li className="mdc-list-item" role="menuitem" key={key}>
                  <span className="mdc-list-item__text">{key}</span>
                </li>;
              })
            }
          </ul>
        </div>
      </div>
      ) : '';

    // <li key={key}><a href={value} target="_blank" rel="noopener noreferrer">{key}</a></li>

    return (
      <div className="template-content-div">
        <p>
          {this.props.collection.description}
        </p>
        {services}
      </div>
    )
  }
}
