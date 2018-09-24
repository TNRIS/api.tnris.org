import React from 'react';
import mapboxgl from 'mapbox-gl';

import loadingImage from '../../images/loading.jpg';

export default class TnrisDownloadTemplateDownload extends React.Component {
  constructor(props) {
      super(props);
      console.log(this.props);
      this.createMap = this.createMap.bind(this);
  }

  componentDidMount() {
    this.createMap();
  }

  componentDidUpdate () {
    this.createMap();
  }

  createMap() {
    // define mapbox map
    if (this.props.loadingResources === false) {
      mapboxgl.accessToken = 'undefined';
      const map = new mapboxgl.Map({
          container: 'tnris-download-map', // container id
          style: 'https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json',
          center: [-99.341389, 31.330000],
          zoom: 6.1
      });

      map.addControl(new mapboxgl.NavigationControl(), 'top-left');
    }
  }

  render() {
    const { errorResources, loadingResources } = this.props;
    const loadingMessage = (
      <div className='tnris-download-template-download'>
        <div className="tnris-download-template-download__loading">
          <img src={loadingImage} alt="Holodeck Loading..." className="holodeck-loading-image" />
        </div>
      </div>
      );

    if (errorResources) {
      return <div>Error! {errorResources.message}</div>;
    }

    if (loadingResources) {
      return loadingMessage;
    }

    return (
      <div className='tnris-download-template-download'>
        <div id='tnris-download-map'></div>
      </div>
    );
  }
}
