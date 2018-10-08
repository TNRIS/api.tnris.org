import React from 'react';

export default class Metadata extends React.Component {
  constructor (props) {
    super(props);
  }

  render() {
    const source = this.props.collection.source ? (
      <li className="mdc-list-item">
        <strong>Source:</strong> {this.props.collection.source}
      </li>
    ) : "";

    const agency = this.props.collection.agency_name ? (
      <li className="mdc-list-item">
        <strong>Agency Name:</strong> {this.props.collection.agency_name} ({this.props.collection.agency_abbreviation})
      </li>
    ) : "";

    const agency_site = this.props.collection.agency_website ? (
      <li className="mdc-list-item">
        <strong>Agency Website:</strong>
          {this.props.collection.agency_website}
      </li>
    ) : "";

    const epsgUrl = "https://epsg.io/" + this.props.collection.spatial_reference;
    const epsg = this.props.collection.spatial_reference ? (
      <li className="mdc-list-item">
        <strong>Spatial Reference:</strong>
          <a href={epsgUrl} target="_blank" rel="noopener noreferrer">EPSG {this.props.collection.spatial_reference}</a>
      </li>
    ) : "";

    const license = this.props.collection.license_name ? (
      <li className="mdc-list-item">
        <strong>License:</strong>
          <a href={this.props.collection.license_url} target="_blank" rel="noopener noreferrer">{this.props.collection.license_name}</a>
      </li>
    ) : "";

    const acquisition = this.props.collection.acquisition_date.substring(0, 4);
    const acq_year = this.props.collection.acquisition_date ? (
      <li className="mdc-list-item">
        <strong>Acquisition:</strong>
          {acquisition}
      </li>
    ) : "";

    return (
      <li className='mdc-image-list__item metadata'>
        <div className='mdc-typography--headline4'>
          METADATA
        </div>
        <ul className="mdc-list">
          {source}
          {agency}
          {agency_site}
          {epsg}
          {license}
          {acq_year}
        </ul>
      </li>
    )
  }
}
