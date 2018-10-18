import React from 'react';

export default class Supplementals extends React.Component {

  render() {
    const tileIndex = this.props.collection.tile_index_url ? (
      <li className="mdc-list-item">
        <strong>Tile Index:</strong>
        <a href={this.props.collection.tile_index_url}>
          <i className="material-icons">description</i>Download Zipfile
        </a>
      </li>
    ) : "";

    const supplementalReport = this.props.collection.supplemental_report_url ? (
      <li className="mdc-list-item">
        <strong>Project Report(s):</strong>
        <a href={this.props.collection.supplemental_report_url}>
          <i className="material-icons">description</i>Download Zipfile
        </a>
      </li>
    ) : "";

    const lidarBreaklines = this.props.collection.lidar_breaklines_url ? (
      <li className="mdc-list-item">
        <strong>Lidar Breaklines:</strong>
        <a href={this.props.collection.lidar_breaklines_url}>
          <i className="material-icons">description</i>Download Zipfile
        </a>
      </li>
    ) : "";

    return (
      <div className="template-content-div">
        <div className='mdc-typography--headline5 template-content-div-header'>
          Supplemental Downloads
        </div>
        <ul className="mdc-list supplemental-downloads">
          {tileIndex}
          {supplementalReport}
          {lidarBreaklines}
        </ul>
      </div>
    )
  }
}
