import React from 'react';

export default class TnrisDownloadTemplate extends React.Component {
  constructor(props) {
      super(props);
      console.log(this.props);
      // this.doSomethingElse = this.doSomethingElse.bind(this);
  }

  // doSomethingElse () {
  //
  // }

  render() {
    const epsgUrl = "https://epsg.io/" + this.props.collection.spatial_reference;

    return (
      <ul className='tnris-download-template mdc-image-list mdc-image-list--masonry' tabIndex='1'>
            <li className='mdc-image-list__item'>
              <div className='mdc-typography--headline4'>
                {this.props.collection.name}
              </div>
            </li>

            <li className='mdc-image-list__item'>
              <div className='mdc-typography--headline4'>
                METADATA
              </div>
              <ul className="mdc-list">
                <li className="mdc-list-item">Source: {this.props.collection.source}</li>
                <li className="mdc-list-item">Agency Name: {this.props.collection.agency_name} ({this.props.collection.agency_abbreviation})</li>
                <li className="mdc-list-item">Agency Website: {this.props.collection.agency_website}</li>
                <li className="mdc-list-item">Spatial Reference: <a href={epsgUrl} target="_blank" rel="noopener noreferrer">EPSG {this.props.collection.spatial_reference}</a></li>
                <li className="mdc-list-item">License: <a href={this.props.collection.license_url} target="_blank" rel="noopener noreferrer">{this.props.collection.license_name}</a></li>
              </ul>
            </li>
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

            <li className='mdc-image-list__item'>
              <div className='mdc-typography--headline4'>
                OUTSIDE ENTITY LINK
              </div>
              <div>
              </div>
            </li>
            <li className='mdc-image-list__item'>
              <div className='mdc-typography--headline4'>
                LIDAR DEETS
              </div>
              <p>
                Lidar data for Texas is made available online through the use of data compression using <a href="https://rapidlasso.com/lastools/" target="_blank" rel="noopener noreferrer">LASTools</a>. LASTools is an open-source collection of tools for lidar data viewing and manipulation. TNRIS uses the LASzip portion of LASTools for compression\decompression. LASTools provides a lossless compression of the data from las to laz formats.
              </p>
              <ul className="mdc-list">
                <li className="mdc-list-item">Software with native LAZ support</li>
                <li className="mdc-list-item">ERDAS IMAGINE (14.1 and up) by Hexagon Geospatial</li>
                <li className="mdc-list-item">Global Mapper (13.1 and up) by Blue Marble Geo</li>
                <li className="mdc-list-item">ENVI LiDAR (5.1 and up) by Exelis VIS</li>
                <li className="mdc-list-item">FME (2012 and up) by Safe Software</li>
                <li className="mdc-list-item">LAStools by rapidlasso</li>
                <li className="mdc-list-item">plas.io 3D Web Viewer by Hobu Inc.</li>
                <li className="mdc-list-item">FUSION (3.40 and up) by Bob McGaughey of the USDA</li>
                <li className="mdc-list-item">Voyager (1.3 and up) by Voyager GIS</li>
                <li className="mdc-list-item">GRASS GIS (7.0 and up) by Open Source Geospatial Foundation (OSGeo)</li>
              </ul>
            </li>

            <li className='mdc-image-list__item'>
              <div className='mdc-typography--headline4'>
                DESCRIPTION
              </div>
              <div>
                {this.props.collection.description}
              </div>
            </li>
      </ul>
    );
  }
}
