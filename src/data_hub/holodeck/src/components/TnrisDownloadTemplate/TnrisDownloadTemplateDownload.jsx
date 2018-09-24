import React from 'react';
import mapboxgl from 'mapbox-gl';

export default class TnrisDownloadTemplateDownload extends React.Component {
  constructor(props) {
      super(props);
      console.log(this.props);
  }

  componentDidMount() {
    // define mapbox map
    mapboxgl.accessToken = 'undefined';
    const map = new mapboxgl.Map({
        container: 'tnris-download-map', // container id
        style: 'https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json',
        center: [-99.341389, 31.330000],
        zoom: 6.1
    });

    map.addControl(new mapboxgl.NavigationControl(), 'top-left');
  }

  render() {
    return (
      <div className='tnris-download-template-download'>
        <div id='tnris-download-map'>
        </div>
      </div>
    );
  }
}
