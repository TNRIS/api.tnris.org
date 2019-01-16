import React from 'react';

export default class Metadata extends React.Component {
  render() {
    const source = this.props.collection.template !== 'outside-entity' && this.props.collection.source ? (
      <li className="mdc-list-item">
        <span className="mdc-list-item__text">
          <strong>Source:</strong>
        </span>
        <span className="mdc-list-item__meta">
          {this.props.collection.source}
        </span>
      </li>
    ) : "";

    const agency = this.props.collection.agency_name ? (
      <li className="mdc-list-item">
        <span className="mdc-list-item__text">
          <strong>Agency Name:</strong>
        </span>
        <span className="mdc-list-item__meta">
          {this.props.collection.agency_name} ({this.props.collection.agency_abbreviation})
        </span>
      </li>
    ) : "";

    const agency_contact = this.props.collection.agency_contact ? (
      <li className="mdc-list-item">
        <span className="mdc-list-item__text">
          <strong>Agency Contact:</strong>
        </span>
        <span className="mdc-list-item__meta">
            {
              this.props.collection.agency_contact.includes('http') ? <a href={this.props.collection.agency_contact} target="_blank" rel="noopener noreferrer">{this.props.collection.agency_contact}</a>
              : this.props.collection.agency_contact.includes('@') ? <a href={"mailto:" + this.props.collection.agency_contact + "?subject=GIS data question"}>{this.props.collection.agency_contact}</a>
              : <p>{this.props.collection.agency_contact}</p>
            }
        </span>
      </li>
    ) : "";

    const agency_site = this.props.collection.agency_website ? (
      <li className="mdc-list-item">
        <span className="mdc-list-item__text">
          <strong>Agency Website:</strong>
        </span>
        <span className="mdc-list-item__meta">
          <a href={this.props.collection.agency_website} target="_blank" rel="noopener noreferrer">{this.props.collection.agency_website}</a>
        </span>
      </li>
    ) : "";

    const epsg = this.props.collection.template !== 'outside-entity' && this.props.collection.spatial_reference ? (
      <li className="mdc-list-item">
        <span className="mdc-list-item__text">
          <strong>Spatial Reference:</strong>
        </span>
        <span className="mdc-list-item__meta">
          {
            this.props.collection.spatial_reference.split(",").map((code,i) => {
              const epsgUrl = "https://epsg.io/" + code;
              return (<span key={i}><a href={epsgUrl} target="_blank" rel="noopener noreferrer">EPSG {code}</a>&nbsp;&nbsp;</span>);
            })
          }
        </span>
      </li>
    ) : "";

    const license = this.props.collection.template !== 'outside-entity' && this.props.collection.license_name ? (
      <li className="mdc-list-item">
        <span className="mdc-list-item__text">
          <strong>License:</strong>
        </span>
        <span className="mdc-list-item__meta">
          <a href={this.props.collection.license_url} target="_blank" rel="noopener noreferrer">{this.props.collection.license_name}</a>
        </span>
      </li>
    ) : "";

    const acquisition = this.props.collection.acquisition_date ? this.props.collection.acquisition_date.substring(0, 4) : '';
    const acq_year = this.props.collection.template !== 'outside-entity' && this.props.collection.acquisition_date ? (
      <li className="mdc-list-item">
        <span className="mdc-list-item__text">
          <strong>Acquisition:</strong>
        </span>
        <span className="mdc-list-item__meta">
          {acquisition}
        </span>
      </li>
    ) : "";

    const category = this.props.collection.template !== 'outside-entity' && this.props.collection.category ? (
      <li className="mdc-list-item">
        <span className="mdc-list-item__text">
          <strong>Category:</strong>
        </span>
        <span className="mdc-list-item__meta">
          {this.props.collection.category}
        </span>
      </li>
    ) : "";

    const dataTypes = this.props.collection.template !== 'outside-entity' && this.props.collection.data_types ? (
      <li className="mdc-list-item">
        <span className="mdc-list-item__text">
          <strong>Data Types:</strong>
        </span>
        <span className="mdc-list-item__meta">
          {this.props.collection.data_types}
        </span>
      </li>
    ) : "";

    const fileType = this.props.collection.template !== 'outside-entity' && this.props.collection.file_type ? (
      <li className="mdc-list-item">
        <span className="mdc-list-item__text">
          <strong>File Type:</strong>
        </span>
        <span className="mdc-list-item__meta">
          {this.props.collection.file_type}
        </span>
      </li>
    ) : "";

    const resourceTypes = this.props.collection.template !== 'outside-entity' && this.props.collection.resource_types ? (
      <li className="mdc-list-item">
        <span className="mdc-list-item__text">
          <strong>Resource Types:</strong>
        </span>
        <span className="mdc-list-item__meta">
          {this.props.collection.resource_types}
        </span>
      </li>
    ) : "";

    const resolution = this.props.collection.template !== 'outside-entity' && this.props.collection.resolution ? (
      <li className="mdc-list-item">
        <span className="mdc-list-item__text">
          <strong>Resolution:</strong>
        </span>
        <span className="mdc-list-item__meta">
          {this.props.collection.resolution}
        </span>
      </li>
    ) : "";

    const bandTypes = this.props.collection.template !== 'outside-entity' && this.props.collection.band_types ? (
      <li className="mdc-list-item">
        <span className="mdc-list-item__text">
          <strong>Bands:</strong>
        </span>
        <span className="mdc-list-item__meta">
          {this.props.collection.band_types}
        </span>
      </li>
    ) : "";

    const coverageExtent = this.props.collection.template !== 'outside-entity' && this.props.collection.coverage_extent ? (
      <li className="mdc-list-item">
        <span className="mdc-list-item__text">
          <strong>Coverage Extent:</strong>
        </span>
        <span className="mdc-list-item__meta">
          {this.props.collection.coverage_extent}
        </span>
      </li>
    ) : "";

    const knownIssues = this.props.collection.template !== 'outside-entity' && this.props.collection.known_issues ? (
      <li className="mdc-list-item">
        <span className="mdc-list-item__text">
          <strong>Known Issues:</strong>
        </span>
        <span className="mdc-list-item__meta">
          {this.props.collection.known_issues}
        </span>
      </li>
    ) : "";

    const recommendedUse = this.props.collection.template !== 'outside-entity' && this.props.collection.recommended_use ? (
      <li className="mdc-list-item">
        <span className="mdc-list-item__text">
          <strong>Recommended Use:</strong>
        </span>
        <span className="mdc-list-item__meta">
          {this.props.collection.recommended_use}
        </span>
      </li>
    ) : "";

    const tags = this.props.collection.template !== 'outside-entity' && this.props.collection.tags ? (
      <li className="mdc-list-item">
        <span className="mdc-list-item__text">
          <strong>Tags:</strong>
        </span>
        <span className="mdc-list-item__meta">
          {this.props.collection.tags}
        </span>
      </li>
    ) : "";

    return (
      <div className="template-content-div metadata">
        <ul className="mdc-list mdc-list--non-interactive">
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
