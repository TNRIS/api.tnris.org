import React from 'react';
import mapboxgl from 'mapbox-gl';

import loadingImage from '../../images/loading.jpg';

const cartodb = window.cartodb;

export default class TnrisDownloadTemplateDownload extends React.Component {
  constructor(props) {
      super(props);
      this.createMap = this.createMap.bind(this);
      this.createLayers = this.createLayers.bind(this);
  }

  componentDidMount() {
    if (this.props.loadingResources === false) {
      this.areaLookup = this.props.selectedCollectionResources.entities.resourcesByAreaId;
      this.createMap();
    }
  }

  componentDidUpdate () {
    if (this.props.loadingResources === false) {
      this.areaLookup = this.props.selectedCollectionResources.entities.resourcesByAreaId;
      this.createMap();
    }
  }

  createMap() {
    // define mapbox map
    mapboxgl.accessToken = 'undefined';
    const map = new mapboxgl.Map({
        container: 'tnris-download-map', // container id
        style: 'https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json',
        center: [-99.341389, 31.330000],
        zoom: 6.1
    });

    map.addControl(new mapboxgl.NavigationControl(), 'top-left');
    const resourcesString = this.props.selectedCollectionResources.result.join("','");
    const boundsQuery = "SELECT * FROM area_type WHERE area_type_id IN ('" + resourcesString + "')";
    const sql = new cartodb.SQL({ user: 'tnris-flood' });
    sql.getBounds(boundsQuery).done(function(bounds) {
      map.fitBounds([[bounds[1][1],bounds[1][0]],[bounds[0][1],bounds[0][0]]],{padding: 20});
    });

    const thous = this.props.selectedCollectionResources.result.slice(0,1000);

    const resourceList = this.props.selectedCollectionResources.result;
    const total = resourceList.length;

    if (total < 1000) {
      this.createLayers(boundsQuery, map, "0");
    }
    else {
      let loop = 0;
      let s = 0;
      let e = 500;
      while (s < total) {
        console.log('------------');
        console.log(loop);
        console.log(s);
        console.log(e);

        let chunk = resourceList.slice(s, e);
        let chunkString = chunk.join("','");
        let chunkQuery = "SELECT * FROM area_type WHERE area_type_id IN ('" + chunkString + "')";
        console.log(chunk.length);
        this.createLayers(chunkQuery, map, loop.toString());
        loop += 1;
        s += 500;
        e += 500;
      }

    }

  }

  createLayers(query, map, loop) {
    var layerData = {
        user_name: 'tnris-flood',
        sublayers: [{
                sql: query,
                cartocss: '{}'
            }],
        maps_api_template: 'https://tnris-flood.carto.com'
    };

    cartodb.Tiles.getTiles(layerData, function (result, error) {
      if (result == null) {
        console.log("error: ", error.errors.join('\n'));
        return;
      }
      // console.log("url template is ", result.tiles[0]);

      var areaTiles = result.tiles.map(function (tileUrl) {
        return tileUrl
          .replace('{s}', 'a')
          .replace(/.png/, '.mvt');
      });

      map.addSource('area_type_source' + loop, { type: 'vector', tiles: areaTiles });
      map.addLayer({
          id: 'area_type' + loop,
          'type': 'fill',
          'source': 'area_type_source' + loop,
          'source-layer': 'layer0',
          'layout': {},
          'paint': {
            'fill-color': 'rgba(97,12,239,0.3)',
            'fill-outline-color': '#FFFFFF'
          }
      });

      map.addLayer({
          id: 'area_type_hover' + loop,
          'type': 'fill',
          'source': 'area_type_source' + loop,
          'source-layer': 'layer0',
          'paint': {
            'fill-color': 'rgba(130,109,186,.7)',
            'fill-outline-color': '#FFFFFF'
          },
          'filter': ['==', 'area_type_name', '']
      }, 'area_type' + loop);

      map.addLayer({
          id: 'area_type_label' + loop,
          'type': 'symbol',
          'source': 'area_type_source' + loop,
          'source-layer': 'layer0',
          // 'minzoom': 10,
          'layout': {
            "text-field": "{area_type_name}"
          },
          'paint': {
            "text-color": "#FFFFFF"
          }
      });
    });

    const areaLookup = this.areaLookup;
    map.on('click', 'area_type' + loop, function (e) {
      // console.log(e.features[0].properties);
      // console.log(e.lngLat);
      const clickedAreaId = e.features[0].properties.area_type_id;
      const downloadUrl = areaLookup[clickedAreaId];
      window.location = downloadUrl.resource;
    });
    // Change the cursor to a pointer when it enters a feature in the 'county-extended' layer
    // highlight the county polys on hover if the zoom range is right
    map.on('mousemove', 'area_type' + loop, function (e) {
      map.getCanvas().style.cursor = 'pointer';
      map.setFilter('area_type_hover' + loop, ['==', 'area_type_name', e.features[0].properties.area_type_name]);
    });

    // Change it back to a karate when it leaves 'area_type'
    // remove the hover effect on mouseleave
    map.on('mouseleave', 'area_type' + loop, function () {
      map.getCanvas().style.cursor = '';
      map.setFilter('area_type_hover' + loop, ['==', 'area_type_name', '']);
    });
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
