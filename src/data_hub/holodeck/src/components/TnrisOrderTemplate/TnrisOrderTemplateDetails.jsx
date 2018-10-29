import React from 'react';

import Description from '../DialogTemplateListItems/Description'
import LidarBlurb from '../DialogTemplateListItems/LidarBlurb'
import Metadata from '../DialogTemplateListItems/Metadata'

import ContactContainer from '../../containers/ContactContainer';
// import OrderTnrisDataFormContainer from '../../containers/OrderTnrisDataFormContainer';

export default class TnrisDownloadTemplateDetails extends React.Component {

  render() {
    const lidarCard = this.props.collection.category === 'Lidar' ? <LidarBlurb /> : "";

    return (
      <div className='tnris-download-template-details'>
        <Metadata collection={this.props.collection} />

        <Description collection={this.props.collection} />
        {lidarCard}
        <div className="template-content-div">
          <div className='mdc-typography--headline5 template-content-div-header' onClick={this.toggleContact}>
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
