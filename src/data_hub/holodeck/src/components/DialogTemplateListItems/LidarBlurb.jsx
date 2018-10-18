import React from 'react';

export default class LidarBlurb extends React.Component {

  render() {
    return (
      <div className="template-content-div">
        <div className='mdc-typography--headline5 template-content-div-header'>
          Lidar Note
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
      </div>
    )
  }
}
