import React from 'react';

import Metadata from '../DialogTemplateListItems/Metadata'
import CountyCoverageContainer from '../../containers/CountyCoverageContainer'
import HistoricalProducts from '../DialogTemplateListItems/HistoricalProducts'
import Ls4Links from '../DialogTemplateListItems/Ls4Links'
import ShareButtons from '../DialogTemplateListItems/ShareButtons'
import Images from '../DialogTemplateListItems/Images'


export default class TnrisDownloadTemplateDetails extends React.Component {


  render() {
    const productsCard = this.props.collection.products ?
                          (<div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-6'>
                            <HistoricalProducts products={this.props.collection.products} />
                          </div>)
                          : "";

    const countyCoverageCard = this.props.collection.counties ?
                                (<div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-6'>
                                  <CountyCoverageContainer counties={this.props.collection.counties} />
                                </div>)
                                : "";

    const ls4LinksCard = (this.props.collection.index_service_url && this.props.collection.index_service_url !== "") ||
                         (this.props.collection.mosaic_service_url && this.props.collection.mosaic_service_url !== "") ||
                         (this.props.collection.frames_service_url && this.props.collection.frames_service_url !== "") ||
                         (this.props.collection.scanned_index_ls4_links && this.props.collection.scanned_index_ls4_links) !== "" ?
                         (<div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-6'>
                           <Ls4Links index={this.props.collection.index_service_url}
                                     mosaic={this.props.collection.mosaic_service_url}
                                     frames={this.props.collection.frames_service_url}
                                     scans={this.props.collection.scanned_index_ls4_links} />
                         </div>)
                         : "";

    return (
      <div className='historical-aerial-template-details'>
        <div className='mdc-layout-grid'>
          <div className="mdc-layout-grid__inner">

            <div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-6'>
              <Metadata collection={this.props.collection} />
            </div>

            {countyCoverageCard}
            {productsCard}
            {ls4LinksCard}

            <div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-12'>
              <ShareButtons />
            </div>

          </div>
        </div>
      </div>
    );
  }
}
