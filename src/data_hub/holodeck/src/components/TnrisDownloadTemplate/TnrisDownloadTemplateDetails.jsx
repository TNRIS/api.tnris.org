import React from 'react';

import Description from '../DialogTemplateListItems/Description'
import LidarBlurb from '../DialogTemplateListItems/LidarBlurb'
import Metadata from '../DialogTemplateListItems/Metadata'
import Services from '../DialogTemplateListItems/Services'
import Supplementals from '../DialogTemplateListItems/Supplementals'

import ContactContainer from '../../containers/ContactContainer';

export default class TnrisDownloadTemplateDetails extends React.Component {
  constructor(props) {
      super(props);
      this.state = {
        showContact: false
      };
      this.toggleContact = this.toggleContact.bind(this);
  }

  toggleContact () {
    this.setState({showContact: !this.state.showContact});
  }

  render() {
    const lidarCard = this.props.collection.category === 'Lidar' ? <LidarBlurb /> : "";
    const supplementalDownloadsCard = (this.props.collection.tile_index_url ||
                                        this.props.collection.supplemental_report_url ||
                                        this.props.collection.lidar_breaklines_url) ?
                                        <Supplementals collection={this.props.collection} /> : "";
    const servicesCard = this.props.collection.wms_link ? <Services collection={this.props.collection} /> : "";

    const contactIcon = this.state.showContact ? <i className="material-icons">expand_less</i> : <i className="material-icons">expand_more</i>;
    const contactDisplay = this.state.showContact ? (
      <div>
        <ContactContainer collection={this.props.collection} />
      </div>
    ) : "";

    return (
      <ul className='tnris-download-template-details mdc-image-list mdc-image-list--masonry'>

          <Metadata collection={this.props.collection} />
          {supplementalDownloadsCard}
          {servicesCard}
          <Description collection={this.props.collection} />
          {lidarCard}

          <li className='mdc-image-list__item'>
            <div className='mdc-typography--headline5'>
              ORDER
            </div>
            <p>
              Everything you're looking for too large to download? Every dataset is available for order directly from TNRIS by completing this <a href="https://tnris.org/order-data/">Order Form</a>.
            </p>
          </li>

          <li className='mdc-image-list__item'>
            <div id="contact-header" className='mdc-typography--headline5' onClick={this.toggleContact}>
              {contactIcon}Contact
            </div>
            {contactDisplay}
          </li>
        </ul>
    );
  }
}
