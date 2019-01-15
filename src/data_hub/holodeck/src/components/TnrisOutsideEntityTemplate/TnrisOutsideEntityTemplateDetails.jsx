import React from 'react';

import Description from '../DialogTemplateListItems/Description'
import Metadata from '../DialogTemplateListItems/Metadata'
import ShareButtons from '../DialogTemplateListItems/ShareButtons'


export default class TnrisOutsideEntityTemplateDetails extends React.Component {

  render() {

    const description = this.props.collection.description ?
                          (<div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-12'>
                            <Description collection={this.props.collection} />
                          </div>)
                          : "";

    return (
      <div className='outside-entity-template-details'>
        <div className='mdc-layout-grid'>
          <div className="mdc-layout-grid__inner">

            <div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-12'>
              <Metadata collection={this.props.collection} />
            </div>

            {description}

            <div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-12'>
              <ShareButtons />
            </div>

          </div>
        </div>
      </div>
    );
  }
}
