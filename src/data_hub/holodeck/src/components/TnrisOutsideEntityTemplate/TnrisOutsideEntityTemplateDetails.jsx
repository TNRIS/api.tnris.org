import React from 'react';

import Description from '../DialogTemplateListItems/Description'
import Metadata from '../DialogTemplateListItems/Metadata'

import ContactContainer from '../../containers/OutsideEntityContactContainer';

export default class TnrisOutsideEntityTemplateDetails extends React.Component {

  render() {

    return (

      <div className='tnris-download-template-details'>

        <Metadata collection={this.props.collection} />
        <Description collection={this.props.collection} />

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
