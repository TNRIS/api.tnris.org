import React from 'react';

import Metadata from '../DialogTemplateListItems/Metadata'
import CountyCoverageContainer from '../../containers/CountyCoverageContainer'
import HistoricalProducts from '../DialogTemplateListItems/HistoricalProducts'
import Ls4Links from '../DialogTemplateListItems/Ls4Links'

import ContactContainer from '../../containers/ContactContainer';

export default class TnrisDownloadTemplateDetails extends React.Component {


  render() {
    const productsCard = this.props.collection.products ? <HistoricalProducts products={this.props.collection.products} /> : "";
    const countyCoverageCard = this.props.collection.counties ? <CountyCoverageContainer counties={this.props.collection.counties} /> : "";
    const ls4LinksCard = (this.props.collection.index_service_url && this.props.collection.index_service_url !== "") ||
                         (this.props.collection.mosaic_service_url && this.props.collection.mosaic_service_url !== "") ||
                         (this.props.collection.frames_service_url && this.props.collection.frames_service_url !== "") ||
                         (this.props.collection.scanned_index_ls4_links && this.props.collection.scanned_index_ls4_links) !== "" ?
                         <Ls4Links index={this.props.collection.index_service_url}
                                   mosaic={this.props.collection.mosaic_service_url}
                                   frames={this.props.collection.frames_service_url}
                                   scans={this.props.collection.scanned_index_ls4_links} />
                                 : "";

    return (
      <div className='historical-aerial-template-details'>
        <Metadata collection={this.props.collection} />
        {countyCoverageCard}
        {productsCard}
        {ls4LinksCard}

        <div className="template-content-div">
          <div className='mdc-typography--headline5 template-content-div-header'>
            Contact
          </div>
          <div>
            <ContactContainer collection={this.props.collection} />
          </div>
        </div>
      </div>
    );
  }
}
