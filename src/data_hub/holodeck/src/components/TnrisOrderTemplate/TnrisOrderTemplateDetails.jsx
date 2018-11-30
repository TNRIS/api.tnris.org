import React from 'react';

import CountyCoverageContainer from '../../containers/CountyCoverageContainer'
import Description from '../DialogTemplateListItems/Description'
import LidarBlurb from '../DialogTemplateListItems/LidarBlurb'
import Metadata from '../DialogTemplateListItems/Metadata'
import Services from '../DialogTemplateListItems/Services'
import Supplementals from '../DialogTemplateListItems/Supplementals'
import ShareButtons from '../DialogTemplateListItems/ShareButtons'

import ContactContainer from '../../containers/ContactContainer';

export default class TnrisDownloadTemplateDetails extends React.Component {

  render() {
    const countyCoverageCard = this.props.collection.counties ? <CountyCoverageContainer counties={this.props.collection.counties} /> : "";
    const lidarCard = this.props.collection.category === 'Lidar' ? <LidarBlurb /> : "";
    const supplementalDownloadsCard = (this.props.collection.tile_index_url ||
                                        this.props.collection.supplemental_report_url ||
                                        this.props.collection.lidar_breaklines_url) ?
                                        <Supplementals collection={this.props.collection} /> : "";
    const servicesCard = this.props.collection.wms_link ? <Services collection={this.props.collection} /> : "";

    return (
      <div className='tnris-order-template-details'>
        <Metadata collection={this.props.collection} />
        {countyCoverageCard}
        {supplementalDownloadsCard}
        {servicesCard}
        <Description collection={this.props.collection} />
        {lidarCard}
        <div className="template-content-div">
          <div className='mdc-typography--headline5 template-content-div-header'>
            Share
          </div>
          <ShareButtons />
        </div>
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
