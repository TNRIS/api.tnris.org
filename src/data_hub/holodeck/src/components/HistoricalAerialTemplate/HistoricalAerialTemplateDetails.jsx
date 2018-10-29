import React from 'react';

import Metadata from '../DialogTemplateListItems/Metadata'
import CountyCoverage from '../DialogTemplateListItems/CountyCoverage'
import HistoricalProducts from '../DialogTemplateListItems/HistoricalProducts'

import ContactContainer from '../../containers/ContactContainer';

export default class TnrisDownloadTemplateDetails extends React.Component {


  render() {
    const productsCard = this.props.collection.products ? <HistoricalProducts products={this.props.collection.products} /> : "";
    const countyCoverageCard = this.props.collection.counties ? <CountyCoverage counties={this.props.collection.counties} /> : "";

    return (
      <div className='historical-aerial-template-details'>
        <Metadata collection={this.props.collection} />
        {countyCoverageCard}
        {productsCard}

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
