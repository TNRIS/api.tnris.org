import React from 'react';
import mapboxgl from 'mapbox-gl';

import loadingImage from '../../images/loading.jpg';

const cartodb = window.cartodb;

export default class TnrisDownloadTemplateDownload extends React.Component {
  constructor(props) {
      super(props);
      console.log(this.props.selectedCollectionResources.entities.resourcesByAreaId);
      this.areaLookup = this.props.selectedCollectionResources.entities.resourcesByAreaId;
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

      const resourcesString = this.props.selectedCollectionResources.result.join("','");
      const query = "SELECT * FROM area_type WHERE area_type_id IN ('" + resourcesString + "')";
      console.log(query);
      // define county layer and add it to the map
      var layerData = {
          user_name: 'tnris-flood',
          sublayers: [{
                  sql: query,
                  cartocss: '{}'
              }],
          maps_api_template: 'https://tnris-flood.carto.com'
      };

      const sql = new cartodb.SQL({ user: 'tnris-flood' });
      sql.getBounds(query).done(function(bounds) {
        map.fitBounds([[bounds[1][1],bounds[1][0]],[bounds[0][1],bounds[0][0]]],{padding: 20});
      });


      cartodb.Tiles.getTiles(layerData, function (result, error) {
        if (result == null) {
          console.log("error: ", error.errors.join('\n'));
          return;
        }
        console.log("url template is ", result.tiles[0]);

        var areaTiles = result.tiles.map(function (tileUrl) {
          return tileUrl
            .replace('{s}', 'a')
            .replace(/.png/, '.mvt');
        });

        map.addSource('area_type_source', { type: 'vector', tiles: areaTiles });
        map.addLayer({
            id: 'area_type',
            'type': 'fill',
            'source': 'area_type_source',
            'source-layer': 'layer0',
            'layout': {},
            'paint': {
              'fill-color': 'rgba(130,109,186,0)',
              'fill-outline-color': '#969696'
            }
        });

        map.addLayer({
            id: 'area_type_hover',
            'type': 'fill',
            'source': 'area_type_source',
            'source-layer': 'layer0',
            // 'maxzoom': 9,
            'paint': {
              'fill-color': 'rgba(97,12,239,0.3)',
              'fill-outline-color': '#FFFFFF'
            },
            'filter': ['==', 'area_type_name', '']
        }, 'area_type');
      });

      const areaLookup = this.areaLookup;
      map.on('click', 'area_type', function (e) {
        console.log(e.features[0].properties);
        // console.log(e.lngLat);
        const clickedAreaId = e.features[0].properties.area_type_id;
        const downloadUrl = areaLookup[clickedAreaId];
        window.location = downloadUrl.resource;
      });
      // Change the cursor to a pointer when it enters a feature in the 'county-extended' layer
      // highlight the county polys on hover if the zoom range is right
      map.on('mousemove', 'area_type', function (e) {
        map.getCanvas().style.cursor = 'pointer';
        map.setFilter('area_type_hover', ['==', 'area_type_name', e.features[0].properties.area_type_name]);
      });

      // Change it back to a karate when it leaves 'area_type'
      // remove the hover effect on mouseleave
      map.on('mouseleave', 'area_type', function () {
        map.getCanvas().style.cursor = '';
        map.setFilter('area_type_hover', ['==', 'area_type_name', '']);
      });

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
