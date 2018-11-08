import React from 'react';

export default class Metadata extends React.Component {
  render() {
    const source = this.props.collection.template !== 'outside-entity' && this.props.collection.source ? (
      <li className="mdc-list-item">
        <strong>Source:</strong>{this.props.collection.source}
      </li>
    ) : "";

    const agency = this.props.collection.agency_name ? (
      <li className="mdc-list-item">
        <strong>Agency Name:</strong>{this.props.collection.agency_name} ({this.props.collection.agency_abbreviation})
      </li>
    ) : "";

    const agency_contact = this.props.collection.agency_contact ? (
      <li className="mdc-list-item">
        <strong>Agency Contact:</strong><a href={"mailto:" + this.props.collection.agency_contact + "?subject=GIS data question"}>{this.props.collection.agency_contact}</a>
      </li>
    ) : "";

    const agency_site = this.props.collection.agency_website ? (
      <li className="mdc-list-item">
        <strong>Agency Website:</strong><a href={this.props.collection.agency_website} target="_blank">{this.props.collection.agency_website}</a>
      </li>
    ) : "";

    const epsg = this.props.collection.template !== 'outside-entity' && this.props.collection.spatial_reference ? (
      <li className="mdc-list-item">
        <strong>Spatial Reference:</strong>
          {
            this.props.collection.spatial_reference.split(",").map((code,i) => {
              const epsgUrl = "https://epsg.io/" + code;
              return (<span key={i}><a href={epsgUrl} target="_blank" rel="noopener noreferrer">EPSG {code}</a>&nbsp;&nbsp;</span>);
            })
          }
      </li>
    ) : "";

    const license = this.props.collection.template !== 'outside-entity' && this.props.collection.license_name ? (
      <li className="mdc-list-item">
        <strong>License:</strong>
          <a href={this.props.collection.license_url} target="_blank" rel="noopener noreferrer">{this.props.collection.license_name}</a>
      </li>
    ) : "";

    const acquisition = this.props.collection.acquisition_date ? this.props.collection.acquisition_date.substring(0, 4) : '';
    const acq_year = this.props.collection.template !== 'outside-entity' && this.props.collection.acquisition_date ? (
      <li className="mdc-list-item">
        <strong>Acquisition:</strong>{acquisition}
      </li>
    ) : "";

    const category = this.props.collection.template !== 'outside-entity' && this.props.collection.category ? (
      <li className="mdc-list-item">
        <strong>Category:</strong>{this.props.collection.category}
      </li>
    ) : "";

    const dataTypes = this.props.collection.template !== 'outside-entity' && this.props.collection.data_types ? (
      <li className="mdc-list-item">
        <strong>Data Types:</strong>{this.props.collection.data_types}
      </li>
    ) : "";

    const fileType = this.props.collection.template !== 'outside-entity' && this.props.collection.file_type ? (
      <li className="mdc-list-item">
        <strong>File Type:</strong>{this.props.collection.file_type}
      </li>
    ) : "";

    const resourceTypes = this.props.collection.template !== 'outside-entity' && this.props.collection.resource_types ? (
      <li className="mdc-list-item">
        <strong>Resource Types:</strong>{this.props.collection.resource_types}
      </li>
    ) : "";

    const resolution = this.props.collection.template !== 'outside-entity' && this.props.collection.resolution ? (
      <li className="mdc-list-item">
        <strong>Resolution:</strong>{this.props.collection.resolution}
      </li>
    ) : "";

    const bandTypes = this.props.collection.template !== 'outside-entity' && this.props.collection.band_types ? (
      <li className="mdc-list-item">
        <strong>Bands:</strong>{this.props.collection.band_types}
      </li>
    ) : "";

    const coverageExtent = this.props.collection.template !== 'outside-entity' && this.props.collection.coverage_extent ? (
      <li className="mdc-list-item">
        <strong>Coverage Extent:</strong>{this.props.collection.coverage_extent}
      </li>
    ) : "";

    const knownIssues = this.props.collection.template !== 'outside-entity' && this.props.collection.known_issues ? (
      <li className="mdc-list-item">
        <strong>Known Issues:</strong>{this.props.collection.known_issues}
      </li>
    ) : "";

    const recommendedUse = this.props.collection.template !== 'outside-entity' && this.props.collection.recommended_use ? (
      <li className="mdc-list-item">
        <strong>Recommended Use:</strong>{this.props.collection.recommended_use}
      </li>
    ) : "";

    const tags = this.props.collection.template !== 'outside-entity' && this.props.collection.tags ? (
      <li className="mdc-list-item">
        <strong>Tags:</strong>{this.props.collection.tags}
      </li>
    ) : "";

    return (
      <div className="template-content-div metadata">
        <div className='mdc-typography--headline5 template-content-div-header'>
          Metadata
        </div>
        <ul className="mdc-list">
          {source}
          {agency}
          {agency_site}
          {agency_contact}
          {epsg}
          {license}
          {acq_year}

          {category}
          {dataTypes}
          {fileType}
          {resourceTypes}
          {resolution}
          {bandTypes}

          {coverageExtent}
          {knownIssues}
          {recommendedUse}
          {tags}
        </ul>
      </div>
    )
  }
}
