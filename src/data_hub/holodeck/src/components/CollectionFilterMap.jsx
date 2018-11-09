import React from 'react';

import mapboxgl from 'mapbox-gl';
import MapboxDraw from '@mapbox/mapbox-gl-draw/dist/mapbox-gl-draw.js';
import '@mapbox/mapbox-gl-draw/dist/mapbox-gl-draw.css';
// the carto core api is a CDN in the app template HTML (not available as NPM package)
// so we create a constant to represent it so it's available to the component
const cartodb = window.cartodb;

export default class CollectionFilterMap extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      collectionIds: this.props.collectionFilterMapFilter
    }
    // bind our map builder and other custom functions
    this.enableUserInteraction = this.enableUserInteraction.bind(this);
    this.disableUserInteraction = this.disableUserInteraction.bind(this);
    this.handleFilterButtonClick = this.handleFilterButtonClick.bind(this);
  }

  componentDidMount() {
    // define mapbox map
    mapboxgl.accessToken = 'undefined';
    // define the map bounds for Texas at the initial zoom and center,
    // these will keep the map bounds centered around Texas
    const bounds = [
      [-108.83792172606844, 25.535364049344025], // Southwest coordinates
      [-89.8448562738755, 36.78883840623598] // Northeast coordinates
    ]
    this._map = new mapboxgl.Map({
        container: 'collection-filter-map', // container id
        style: 'https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json',
        center: this.props.collectionFilterMapCenter,
        zoom: this.props.collectionFilterMapZoom,
        maxBounds: bounds, // sets bounds as max to prevent panning
        interactive: true
    });
    this._navControl = new mapboxgl.NavigationControl()
    this._map.addControl(this._navControl, 'top-left');

    // create the draw control and define its functionality
    const draw = new MapboxDraw({
      displayControlsDefault: false,
      controls: {'polygon': true, 'trash': true}
    });
    this._map.addControl(draw, 'top-left');
    // Check if the draw mode is draw_polygon, if so, check if there
    // are previously drawn features on the map and if so, delete them.
    // We do this so there is only ever one aoi polygon in the map at a time.
    this._map.on('draw.modechange', function(e) {
      if (e.mode === 'draw_polygon') {
        let features = draw.getAll();
        if (features.features.length > 1) {
          draw.delete(features.features[0].id);
        }
      }
    })
    this._map.on('draw.create', function(e) {
      // console.log(e.features);
    })

    if (this.props.collectionFilterMapFilter.length > 0) {
      this.disableUserInteraction();
    }

    const _this = this;
    this._map.on('moveend', function() {
      getExtentIntersectedCollectionIds(_this);
    })
    getExtentIntersectedCollectionIds(this);

    function getExtentIntersectedCollectionIds(_this) {
      // get the map bounds from the current extent and query carto
      // to find the area_type polygons that intersect this mbr and
      // return the collection_ids associated with those areas
      const sql = new cartodb.SQL({user: 'tnris-flood'});
      let center = _this._map.getCenter();
      let zoom = _this._map.getZoom();
      let bounds = _this._map.getBounds();
      let query = `SELECT
                     areas.collections
                   FROM
                     area_type, areas
                   WHERE
                     area_type.area_type_id = areas.area_type_id
                   AND
                     area_type.the_geom && ST_MakeEnvelope(
                       ${bounds._ne.lng}, ${bounds._sw.lat}, ${bounds._sw.lng}, ${bounds._ne.lat})`;

      sql.execute(query).done(function(data) {
        // set up the array of collection_id arrays from the returned
        // query object
        let collectionIds = data.rows.map(function (obj) {
          return obj.collections.split(",");
        });
        // combine all collection_id arrays into a single array of unique ids
        let uniqueCollectionIds = [...new Set([].concat(...collectionIds))];
        _this.setState({
          collectionIds: uniqueCollectionIds
        });
        _this.props.setCollectionFilterMapCenter(center);
        _this.props.setCollectionFilterMapZoom(zoom);
      }).error(function(errors) {
        // errors contains a list of errors
        // console.log("errors:" + errors);
      })
    }
  }

  enableUserInteraction() {
    // enables panning, rotating, and zooming of the map
    this._map.boxZoom.enable();
    this._map.doubleClickZoom.enable();
    this._map.dragPan.enable();
    this._map.dragRotate.enable();
    this._map.keyboard.enable();
    this._map.scrollZoom.enable();
    this._map.touchZoomRotate.enable();
    this._navControl._compass.disabled = false;
    this._navControl._zoomInButton.disabled = false;
    this._navControl._zoomOutButton.disabled = false;

  }

  disableUserInteraction() {
    // disables panning, rotating, and zooming of the map
    this._map.boxZoom.disable();
    this._map.doubleClickZoom.disable();
    this._map.dragPan.disable();
    this._map.dragRotate.disable();
    this._map.keyboard.disable();
    this._map.scrollZoom.disable();
    this._map.touchZoomRotate.disable();
    this._navControl._compass.disabled = true;
    this._navControl._zoomInButton.disabled = true;
    this._navControl._zoomOutButton.disabled = true;
  }

  handleFilterButtonClick() {
    // sets the collection_ids array in the filter to drive the view, sets the
    // current map center and zoom in the state for the next time we open the map,
    // and disables/enables the user interaction handlers and navigation controls
    if (this.props.collectionFilterMapFilter.length > 0) {
      this.props.setCollectionFilterMapFilter([]);
      this.enableUserInteraction();
    } else {
      this.props.setCollectionFilterMapFilter(this.state.collectionIds);
      this.disableUserInteraction();
    }
  }

  render() {
    return (
      <div className='collection-filter-map-component'>
        <div id='collection-filter-map'></div>
        <button
          className='map-filter-button mdc-fab mdc-fab--extended'
          onClick={this.handleFilterButtonClick}>
          {this.props.collectionFilterMapFilter.length > 0 ? 'clear map filter' : 'set map filter'}
        </button>
      </div>
    );
  }
}
