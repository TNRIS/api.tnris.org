import React from 'react';

import Description from '../DialogTemplateListItems/Description'
import Details from '../DialogTemplateListItems/Details'
import LidarBlurb from '../DialogTemplateListItems/LidarBlurb'
import Metadata from '../DialogTemplateListItems/Metadata'
import OutsideEntityLink from '../DialogTemplateListItems/OutsideEntityLink'
import Services from '../DialogTemplateListItems/Services'
import Supplementals from '../DialogTemplateListItems/Supplementals'

import ContactContainer from '../../containers/ContactContainer';

export default class TnrisDownloadTemplateDetails extends React.Component {
  render() {
    return (
      <ul className='tnris-download-template-details mdc-image-list mdc-image-list--masonry'>

          <Metadata collection={this.props.collection} />
          <Details collection={this.props.collection} />
          <Supplementals collection={this.props.collection} />
          <Services collection={this.props.collection} />
          <OutsideEntityLink collection={this.props.collection} />
          <LidarBlurb />
          <Description collection={this.props.collection} />

          <li className='mdc-image-list__item'>
            <div className='mdc-typography--headline4'>
              ORDER
            </div>
            <div>
              Too large to download everything you're looking for? Every dataset is available for order directly from TNRIS by completing this <a href="https://tnris.org/order-data/">Order Form</a>.
            </div>
          </li>

          <li className='mdc-image-list__item'>
            <div className='mdc-typography--headline4'>
              Contact
            </div>
            <div>
              <ContactContainer collection={this.props.collection} />
            </div>
          </li>
        </ul>
    );
  }
}
