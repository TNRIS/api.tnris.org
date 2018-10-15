import React from 'react';

import mapboxgl from 'mapbox-gl';
// the carto core api is a CDN in the app template HTML (not available as NPM package)
// so we create a constant to represent it so it's available to the component
const cartodb = window.cartodb;

export default class CollectionFilterMap extends React.Component {
  constructor(props) {
    super(props);
    // bind our map builder functions
    this.createMap = this.createMap.bind(this);
  }

  componentDidMount() {
    this.createMap(this.props);
  }

  createMap(props) {
    // define mapbox map
    mapboxgl.accessToken = 'undefined';
    const map = new mapboxgl.Map({
        container: 'collection-filter-map', // container id
        style: 'https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json',
        center: [-99.341389, 31.330000],
        zoom: 5.8
    });
    map.addControl(new mapboxgl.NavigationControl(), 'top-left');

    const sql = new cartodb.SQL({user: 'tnris-flood'});

    map.on('moveend', function() {
      // get the map bounds from the current extent and query carto
      // to find the area_type polygons that intersect this mbr
      let bounds = map.getBounds();
      let query = `SELECT area_type_id from area_type WHERE the_geom &&
        ST_MakeEnvelope(${bounds._ne.lng}, ${bounds._sw.lat}, ${bounds._sw.lng}, ${bounds._ne.lat})`;
      console.log(query);
      sql.execute(query).done(function(data) {
        props.setCollectionFilterMapFilter(data.rows);
      }).error(function(errors) {
        // errors contains a list of errors
        console.log("errors:" + errors);
      })
    })
  }

  render() {
    console.log(this.props);
    return (
      <div className='collection-filter-map-component'>
        <div id='collection-filter-map'>
        </div>
      </div>
    );
  }
}
