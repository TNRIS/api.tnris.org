import React from 'react';

export default class Details extends React.Component {

  render() {
    return (
      <li className='mdc-image-list__item'>
        <div className='mdc-typography--headline4'>
          DETAILS
        </div>
        <ul className="mdc-list">
          <li className="mdc-list-item">Category: {this.props.collection.category}</li>
          <li className="mdc-list-item">Bands: {this.props.collection.band_types}</li>
          <li className="mdc-list-item">Data Type: {this.props.collection.data_types}</li>
          <li className="mdc-list-item">File Type: {this.props.collection.file_type}</li>
          <li className="mdc-list-item">Known Issues: {this.props.collection.known_issues}</li>
          <li className="mdc-list-item">Recommended Use: {this.props.collection.recommended_use}</li>
          <li className="mdc-list-item">Coverage Extent: {this.props.collection.coverage_extent}</li>
          <li className="mdc-list-item">Resource Types: {this.props.collection.resource_types}</li>
          <li className="mdc-list-item">Resolution: {this.props.collection.resolution}</li>
          <li className="mdc-list-item">Tags: {this.props.collection.tags}</li>
        </ul>
      </li>
    )
  }
}
