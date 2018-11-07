import React from 'react';

import mapboxgl from 'mapbox-gl';
// the carto core api is a CDN in the app template HTML (not available as NPM package)
// so we create a constant to represent it so it's available to the component
const cartodb = window.cartodb;

export default class CollectionFilterMap extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      collectionIds: this.props.collectionFilterMapFilter,
      initialCenter: this.props.collectionFilterMapCenter,
      initialZoom: this.props.collectionFilterMapZoom,
      mapFilter: false,
    }
    // bind our map builder and other custom functions
    this.enableUserInteraction = this.enableUserInteraction.bind(this);
    this.disableUserInteraction = this.disableUserInteraction.bind(this);
    this.handleFilterButtonClick = this.handleFilterButtonClick.bind(this);
  }

  componentDidMount() {
    // define mapbox map
    mapboxgl.accessToken = 'undefined';
    this.map = new mapboxgl.Map({
        container: 'collection-filter-map', // container id
        style: 'https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json',
        center: this.props.collectionFilterMapCenter,
        zoom: this.props.collectionFilterMapZoom
    });
    this.map.addControl(new mapboxgl.NavigationControl(), 'top-left');

    if (this.props.collectionFilterMapFilter.length > 0) {
      this.disableUserInteraction();
    }

    console.log(this.map);

    function getExtentIntersectedCollectionIds(_this) {
      // get the map bounds from the current extent and query carto
      // to find the area_type polygons that intersect this mbr and
      // return the collection_ids associated with those areas
      const sql = new cartodb.SQL({user: 'tnris-flood'});
      let center = _this.map.getCenter();
      let zoom = _this.map.getZoom();
      let bounds = _this.map.getBounds();
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
        console.log("errors:" + errors);
      })
    }

    const _this = this;
    this.map.on('moveend', function() {
      getExtentIntersectedCollectionIds(_this);
    })
    getExtentIntersectedCollectionIds(this);
  }

  enableUserInteraction() {
    this.map.boxZoom.enable();
    this.map.doubleClickZoom.enable();
    this.map.dragPan.enable();
    this.map.dragRotate.enable();
    this.map.keyboard.enable();
    this.map.scrollZoom.enable();
    this.map.touchZoomRotate.enable();

  }

  disableUserInteraction() {
    this.map.boxZoom.disable();
    this.map.doubleClickZoom.disable();
    this.map.dragPan.disable();
    this.map.dragRotate.disable();
    this.map.keyboard.disable();
    this.map.scrollZoom.disable();
    this.map.touchZoomRotate.disable();
  }

  handleFilterButtonClick() {
    // set the collection_ids array in the filter to drive the view and set the
    // current map center and zoom in the state for the next time we open the map
    if (this.props.collectionFilterMapFilter.length > 0) {
      this.props.setCollectionFilterMapFilter([]);
      this.setState({mapFilter: !this.state.mapFilter})
      this.enableUserInteraction();
    } else {
      this.props.setCollectionFilterMapFilter(this.state.collectionIds);
      this.setState({mapFilter: !this.state.mapFilter});
      this.disableUserInteraction();
    }
  }

  render() {
    console.log(this.props);
    console.log(this.state);
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
