import React from 'react';

export default class Supplementals extends React.Component {

  render() {
    return (
      <li className='mdc-image-list__item'>
        <div className='mdc-typography--headline4'>
          SUPPLEMENTAL DOWNLOADS
        </div>
        <ul className="mdc-list">
          <li className="mdc-list-item">Tile Index: <a href={this.props.collection.tile_index_url}><i className="material-icons">description</i> Download File</a></li>
          <li className="mdc-list-item">Project Report(s):  <a href={this.props.collection.supplemental_report_url}><i className="material-icons">description</i> Download File</a></li>
          <li className="mdc-list-item">Lidar Breaklines:  <a href={this.props.collection.lidar_breaklines_url}><i className="material-icons">description</i> Download File</a></li>
        </ul>
      </li>
    )
  }
}
