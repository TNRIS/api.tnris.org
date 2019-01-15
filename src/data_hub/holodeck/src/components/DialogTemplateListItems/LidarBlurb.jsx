import React from 'react';

export default class LidarBlurb extends React.Component {

  render() {
    return (
      <div className="template-content-div">
        <p>
          Lidar data for Texas is made available online through the use of data compression using <a href="https://rapidlasso.com/lastools/" target="_blank" rel="noopener noreferrer">LASTools</a>. LASTools is an open-source collection of tools for lidar data viewing and manipulation. TNRIS uses the LASzip portion of LASTools for compression\decompression. LASTools provides a lossless compression of the data from las to laz formats.
        </p>
      </div>
    )
  }
}
