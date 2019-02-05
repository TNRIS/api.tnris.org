import React from 'react';

import Description from '../DialogTemplateListItems/Description'
import Metadata from '../DialogTemplateListItems/Metadata'
import ShareButtons from '../DialogTemplateListItems/ShareButtons'
import Images from '../DialogTemplateListItems/Images'

export default class TnrisOutsideEntityTemplateDetails extends React.Component {

  render() {
    const imageCarousel = this.props.collection.images ? (
                        <Images images={this.props.collection.images} />)
                        : "";

    const description = this.props.collection.description ? (
                          <Description collection={this.props.collection} />)
                          : "";

    // using mdc classes to determine grid layout depending on screen size (desktop/tablet)
    // special case with phone or smaller device because order of components changes
    const gridLayout = window.innerWidth >= 1000 ? (
                          <div className="mdc-layout-grid__inner">
                            <div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-4'>
                              <Metadata collection={this.props.collection} />
                              <ShareButtons />
                            </div>
                            <div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-8'>
                              {imageCarousel}
                              {description}
                            </div>
                          </div>) : (
                          <div className="mdc-layout-grid__inner">
                            <div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-12'>
                              {imageCarousel}
                              <Metadata collection={this.props.collection} />
                              {description}
                              <ShareButtons />
                            </div>
                          </div>);

    return (
      <div className='outside-entity-template-details'>
        <div className='mdc-layout-grid'>

          {gridLayout}

        </div>
      </div>
    );
  }
}
