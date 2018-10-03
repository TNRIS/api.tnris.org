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
      this.toggleLayers = this.toggleLayers.bind(this);
      this.layerRef = {};
  }

  componentDidMount() {
    // on mount/load, try and launch the map. if the api response with the list
    // of downloadable resources hasn't returned we won't launch it
    if (this.props.loadingResources === false) {
      this.areaLookup = this.props.resourceAreas;
      this.createMap();
    }
  }


  componentDidUpdate () {
    // when the api response with the list of downloadable resources finally
    // returns, the component will update so we launch the map at that time
    if (this.props.loadingResources === false) {
      this.areaLookup = this.props.resourceAreas;
      this.createMap();
    }
  }

  toggleLayers (e, map, areaType) {
    console.log(this.layerRef);
    Object.keys(this.layerRef).map(layer => {
      if (layer === areaType) {
        // iterate layer id's for clicked areaType and toggle their visibility
        this.layerRef[areaType].map(layerName => {
          // var visibility = map.getLayoutProperty(layerName, 'visibility');
          // if (visibility === 'visible') {
          //     return map.setLayoutProperty(layerName, 'visibility', 'none');
          // } else {
              return map.setLayoutProperty(layerName, 'visibility', 'visible');
          // }
        }, this);

      }
      // else {
      //
      // }
    }, this);




    // const menuList = document.querySelectorAll('.dld-map-layer-menu.mdc-list-item');
    // console.log(menuList);
    // menuList.forEach((l) => {
    //   console.log(l.id);
    //   if (l.id === areaType) {
    //     l.className = 'dld-map-layer-menu mdc-list-item mdc-list-item--activated';
    //   }
    //   else {
    //     l.className = 'dld-map-layer-menu mdc-list-item';
    //   }
    // });

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
    const areaTypesAry = Object.keys(this.props.resourceAreaTypes).sort();
    // set the active areaType to be the one with the largest area polygons
    // for faster initial load
    let startLayer = 'qquad';
    if (areaTypesAry.includes('state')) {
      startLayer = 'state';
    } else if (areaTypesAry.includes('county')) {
      startLayer = 'county';
    } else if (areaTypesAry.includes('quad')) {
      startLayer = 'quad';
    }

    // iterate our area_types so we can add them to different layers for
    // layer control in the map and prevent overlap of area polygons
    areaTypesAry.map(areaType => {
        // set aside array in layerRef object for populating with layer ids for
        // layers of this areaType
        this.layerRef[areaType] = [];
        // create the layer control in the DOM
        var link = document.createElement('a');
        link.href = '#';
        link.id = 'dld-' + areaType;
        link.textContent = areaType.toUpperCase();
        // determine if it is the active layer
        let linkClass;
        switch (areaType === startLayer) {
          case true:
            linkClass = 'mdc-list-item mdc-list-item--activated';
            break;
          default:
            linkClass = 'mdc-list-item';
        }
        link.className = linkClass;
        link.onclick = (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.toggleLayers(e, map, areaType);
        };
        var menuItems = document.getElementById('tnris-download-menu');
        menuItems.appendChild(link);

        // get the api response with all available resources (downloads) for this dataset
        // and query Carto for the bounds of area_types associated with the resources
        const areasList = this.props.resourceAreaTypes[areaType];
        const areasString = areasList.join("','");
        const boundsQuery = "SELECT * FROM area_type WHERE area_type_id IN ('" + areasString + "')";
        // const sql = new cartodb.SQL({ user: 'tnris-flood' });
        // sql.getBounds(boundsQuery).done(function(bounds) {
        //   // set map to extent of download areas
        //   map.fitBounds([[bounds[1][1],bounds[1][0]],[bounds[0][1],bounds[0][0]]],{padding: 20});
        // });

        // get total number of resources available for download
        const total = areasList.length;
        // if < 1000 downloads, we know the map can perform so we'll just get them
        // all at once
        if (total < 1000) {
          this.createLayers(boundsQuery, map, "0", areaType);
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
            this.createLayers(chunkQuery, map, loop.toString(), areaType);
            loop += 1;
            s += 1000;
            e += 1000;
          }
        }
        return areaType;
    }, this);
  }

  createLayers(query, map, loop, areaType) {
    // prepare carto tile api information
    var layerData = {
        user_name: 'tnris-flood',
        sublayers: [{
                sql: query,
                cartocss: '{}'
            }],
        maps_api_template: 'https://tnris-flood.carto.com'
    };
    const layerSourceName = areaType + '__area_type_source' + loop;
    const layerBaseName = areaType + '__area_type' + loop;
    const layerHoverName = areaType + '__area_type_hover' + loop;
    const layerLabelName = areaType + '__area_type_label' + loop;
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
      map.addSource(layerSourceName, { type: 'vector', tiles: areaTiles });
      // add the polygon area_type layer
      map.addLayer({
          id: layerBaseName,
          'type': 'fill',
          'source': layerSourceName,
          'source-layer': 'layer0',
          'layout': {'visibility': 'visible'},
          'paint': {
            'fill-color': 'rgba(97,12,239,0.3)',
            'fill-outline-color': '#FFFFFF'
          }
      });
      // add the polygon area_type hover layer. wired below to toggle on hover
      map.addLayer({
          id: layerHoverName,
          'type': 'fill',
          'source': layerSourceName,
          'source-layer': 'layer0',
          'layout': {'visibility': 'visible'},
          'paint': {
            'fill-color': 'rgba(130,109,186,.7)',
            'fill-outline-color': '#FFFFFF'
          },
          'filter': ['==', 'area_type_name', '']
      }, layerBaseName);
      // add the labels layer for the area_type polygons
      map.addLayer({
          id: layerLabelName,
          'type': 'symbol',
          'source': layerSourceName,
          'source-layer': 'layer0',

          // 'minzoom': 10,
          'layout': {
            "text-field": "{area_type_name}",
            'visibility': 'visible'
          },
          'paint': {
            "text-color": "#FFFFFF"
          }
      });
    });
    // add the layer id's to the areaType's array in the layerRef for toggling
    this.layerRef[areaType].push(layerBaseName, layerHoverName, layerLabelName);

    // wire an on-click event to the area_type polygons to show a popup of
    // available resource downloads for clicked area
    const areaLookup = this.areaLookup;
    map.on('click', layerBaseName, function (e) {
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
    map.on('mousemove', layerBaseName, function (e) {
      map.getCanvas().style.cursor = 'pointer';
      map.setFilter(layerHoverName, ['==', 'area_type_name', e.features[0].properties.area_type_name]);
    });
    // Undo the cursor pointer when it leaves a feature in the 'area_type' layer
    // Also, untoggle the hover layer with a filter
    map.on('mouseleave', layerBaseName, function () {
      map.getCanvas().style.cursor = '';
      map.setFilter(layerHoverName, ['==', 'area_type_name', '']);
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
        <nav id='tnris-download-menu' className='mdc-list'></nav>
        <div id='tnris-download-map'></div>
      </div>
    );
  }
}
