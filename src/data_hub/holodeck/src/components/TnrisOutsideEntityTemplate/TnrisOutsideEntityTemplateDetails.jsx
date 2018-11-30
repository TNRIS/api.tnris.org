import React from 'react';

import Description from '../DialogTemplateListItems/Description'
import Metadata from '../DialogTemplateListItems/Metadata'
import ShareButtons from '../DialogTemplateListItems/ShareButtons'

import ContactOutsideContainer from '../../containers/ContactOutsideContainer';

export default class TnrisOutsideEntityTemplateDetails extends React.Component {

  render() {

    const agency_contact = this.props.collection.agency_contact ? (
      <div className="template-content-div">
        <div className='mdc-typography--headline5 template-content-div-header'>
          Contact
        </div>
        <div>
          <ContactOutsideContainer collection={this.props.collection} />
        </div>
      </div>
    ) : "";

    return (
      <div className='outside-entity-template-details'>
        <Metadata collection={this.props.collection} />
        <Description collection={this.props.collection} />
          <div className="template-content-div">
            <div className='mdc-typography--headline5 template-content-div-header'>
              Share
            </div>
            <ShareButtons />
          </div>
        {agency_contact}
      </div>
    );
  }
}
