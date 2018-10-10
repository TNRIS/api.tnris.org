import React from 'react';

import mapboxgl from 'mapbox-gl';

export default class CollectionFilterMap extends React.Component {

  componentDidMount() {
    // define mapbox map
    mapboxgl.accessToken = 'undefined';
    const map = new mapboxgl.Map({
        container: 'collection-filter-map', // container id
        style: 'https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json',
        center: [-99.341389, 31.330000],
        zoom: 6.1
    });

    map.addControl(new mapboxgl.NavigationControl(), 'top-left');
  }

  render() {

    return (
      <div className='collection-filter-map-component'>
        <div id='collection-filter-map'>
        </div>
      </div>
    );
  }
}
