import React from 'react';

import Description from '../DialogTemplateListItems/Description'
import Metadata from '../DialogTemplateListItems/Metadata'
import ShareButtons from '../DialogTemplateListItems/ShareButtons'

// import ContactOutsideContainer from '../../containers/ContactOutsideContainer';

export default class TnrisOutsideEntityTemplateDetails extends React.Component {

  render() {

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
      </div>
    );
  }
}
