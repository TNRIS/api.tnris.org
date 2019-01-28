import React from 'react';

import Metadata from '../DialogTemplateListItems/Metadata'
import CountyCoverageContainer from '../../containers/CountyCoverageContainer'
import HistoricalProducts from '../DialogTemplateListItems/HistoricalProducts'
import Ls4Links from '../DialogTemplateListItems/Ls4Links'
import ShareButtons from '../DialogTemplateListItems/ShareButtons'


export default class TnrisDownloadTemplateDetails extends React.Component {


  render() {
    const productsCard = this.props.collection.products ? (
                          <HistoricalProducts products={this.props.collection.products} />)
                          : "";

    const countyCoverageCard = this.props.collection.counties ? (
                                <CountyCoverageContainer counties={this.props.collection.counties} />)
                                : "";

    const ls4LinksCard = (this.props.collection.index_service_url && this.props.collection.index_service_url !== "") ||
                         (this.props.collection.mosaic_service_url && this.props.collection.mosaic_service_url !== "") ||
                         (this.props.collection.frames_service_url && this.props.collection.frames_service_url !== "") ||
                         (this.props.collection.scanned_index_ls4_links && this.props.collection.scanned_index_ls4_links) !== "" ? (
                         <Ls4Links index={this.props.collection.index_service_url}
                                     mosaic={this.props.collection.mosaic_service_url}
                                     frames={this.props.collection.frames_service_url}
                                     scans={this.props.collection.scanned_index_ls4_links} />)
                         : "";

     // using mdc classes to determine grid layout depending on screen size (desktop/tablet)
     // special case with phone or smaller device (<840px) because order of divs changes
     const gridLayout = window.innerWidth >= 900 ? (
                           <div className="mdc-layout-grid__inner">
                             <div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-4'>
                               <Metadata collection={this.props.collection} />
                               {productsCard}
                               {ls4LinksCard}
                               <ShareButtons />
                             </div>
                             <div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-8'>
                               {countyCoverageCard}
                             </div>
                           </div>) : (
                           <div className="mdc-layout-grid__inner">
                             <div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-12'>
                               <Metadata collection={this.props.collection} />
                               {countyCoverageCard}
                               {productsCard}
                               {ls4LinksCard}
                               <ShareButtons />
                             </div>
                           </div>);

    return (
      <div className='historical-aerial-template-details'>
        <div className='mdc-layout-grid'>

          {gridLayout}

        </div>
      </div>
    );
  }
}
