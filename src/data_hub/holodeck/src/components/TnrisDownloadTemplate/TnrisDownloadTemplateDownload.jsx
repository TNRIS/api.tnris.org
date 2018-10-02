import React from 'react';
import mapboxgl from 'mapbox-gl';

import loadingImage from '../../images/loading.jpg';
// the carto core api is a CDN in the app template HTML (not available as NPM package)
// so we create a constant to represent it so it's available to the component
const cartodb = window.cartodb;

export default class TnrisDownloadTemplateDownload extends React.Component {
  constructor(props) {
      super(props);
      // bind our map builder functions
      this.createMap = this.createMap.bind(this);
      this.createLayers = this.createLayers.bind(this);
  }

  componentDidMount() {
    // wait for the api response with the list of downloadable resources
    if (this.props.loadingResources === false) {
      this.areaLookup = this.props.resourceAreas;
      this.createMap();
    }
  }

  componentDidUpdate () {
    // wait for the api response with the list of downloadable resources
    if (this.props.loadingResources === false) {
      console.log(this.props);
      this.areaLookup = this.props.resourceAreas;
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
    // add those controls!
    map.addControl(new mapboxgl.NavigationControl(), 'top-left');
    // get the api response with all available resources (downloads) for this dataset
    // and query Carto for the bounds of area_types associated with the resources
    const areasList = Object.keys(this.props.resourceAreas);
    const areasString = areasList.join("','");
    const boundsQuery = "SELECT * FROM area_type WHERE area_type_id IN ('" + areasString + "')";
    const sql = new cartodb.SQL({ user: 'tnris-flood' });
    sql.getBounds(boundsQuery).done(function(bounds) {
      // set map to extent of download areas
      map.fitBounds([[bounds[1][1],bounds[1][0]],[bounds[0][1],bounds[0][0]]],{padding: 20});
    });

    // get total number of resources available for download
    const total = areasList.length;
    // if < 1000 downloads, we know the map can perform so we'll just get them
    // all at once
    if (total < 1000) {
      this.createLayers(boundsQuery, map, "0");
    }
    // if more than 1000, we will get area_types to display on the map in chunks
    // since the carto api payload has a maximum limit
    else {
      let loop = 0;
      let s = 0;
      let e = 1000;
      // iterate resources in 1000 record chunks creating the polygon, hover, and label
      // layers for each chunk as separate 'chunk layers'
      while (s < total) {
        let chunk = areasList.slice(s, e);
        let chunkString = chunk.join("','");
        let chunkQuery = "SELECT * FROM area_type WHERE area_type_id IN ('" + chunkString + "')";
        this.createLayers(chunkQuery, map, loop.toString());
        loop += 1;
        s += 1000;
        e += 1000;
      }
    }
  }

  createLayers(query, map, loop) {
    // prepare carto tile api information
    var layerData = {
        user_name: 'tnris-flood',
        sublayers: [{
                sql: query,
                cartocss: '{}'
            }],
        maps_api_template: 'https://tnris-flood.carto.com'
    };
    // get the raster tiles from the carto api
    cartodb.Tiles.getTiles(layerData, function (result, error) {
      if (result == null) {
        console.log("error: ", error.errors.join('\n'));
        return;
      }
      // reformat the tile urls in the carto api response to convert them to
      // vector rather than raster tiles
      var areaTiles = result.tiles.map(function (tileUrl) {
        return tileUrl
          .replace('{s}', 'a')
          .replace(/.png/, '.mvt');
      });
      // use the tiles from the response to add a source to the map
      map.addSource('area_type_source' + loop, { type: 'vector', tiles: areaTiles });
      // add the polygon area_type layer
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
      // add the polygon area_type hover layer. wired below to toggle on hover
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
      // add the labels layer for the area_type polygons
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
    // wire an on-click event to the area_type polygons show a popup of
    // available resource downloads for clicked area
    const areaLookup = this.areaLookup;
    map.on('click', 'area_type' + loop, function (e) {
      // console.log(e.lngLat);
      const clickedAreaId = e.features[0].properties.area_type_id;
      const clickedAreaName = e.features[0].properties.area_type_name;
      const downloads = areaLookup[clickedAreaId];
      let popupContent = "";
      // iterate available downloads for the area
      Object.keys(downloads).sort().map(abbr => {
        const dldInfo = downloads[abbr];
        // if a filesize is populated in the resource table so the popup,
        // we don't want to display empty popups, right?
        let filesizeString = "";
        if (dldInfo.filesize != null) {
          const filesize = parseFloat(dldInfo.filesize / 1000000).toFixed(2).toString();
          filesizeString = " - " + filesize + "MB";
        }
        // create html link and append to content string
        const dld = `<li><a href="${dldInfo.link}" target="_blank">${dldInfo.name}${filesizeString}</a></li>`;
        return popupContent += dld;
      });
      // create popup with constructed content string
      new mapboxgl.Popup()
        .setLngLat(e.lngLat)
        .setHTML(`<strong>${clickedAreaName}</strong><ul>${popupContent}</ul>`)
        .addTo(map);
    });

    // Change the cursor to a pointer when it enters a feature in the 'area_type' layer
    // Also, toggle the hover layer with a filter based on the cursor
    map.on('mousemove', 'area_type' + loop, function (e) {
      map.getCanvas().style.cursor = 'pointer';
      map.setFilter('area_type_hover' + loop, ['==', 'area_type_name', e.features[0].properties.area_type_name]);
    });
    // Undo the cursor pointer when it leaves a feature in the 'area_type' layer
    // Also, untoggle the hover layer with a filter
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
