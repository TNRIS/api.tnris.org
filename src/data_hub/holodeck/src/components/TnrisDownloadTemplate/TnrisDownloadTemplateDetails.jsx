import React from 'react';

import Description from '../DialogTemplateListItems/Description'
import LidarBlurb from '../DialogTemplateListItems/LidarBlurb'
import Metadata from '../DialogTemplateListItems/Metadata'
import Services from '../DialogTemplateListItems/Services'
import Supplementals from '../DialogTemplateListItems/Supplementals'
import ShareButtons from '../DialogTemplateListItems/ShareButtons'
import Images from '../DialogTemplateListItems/Images'


export default class TnrisDownloadTemplateDetails extends React.Component {

  render() {
    const imageCarousel = this.props.collection.images ? (
                        <Images
                          thumbnail={this.props.collection.thumbnail_image}
                          images={this.props.collection.images} />)
                        : "";

    const lidarCard = this.props.collection.category === 'Lidar' ? (
                        <LidarBlurb />)
                        : "";


    const supplementalDownloadsCard = (this.props.collection.tile_index_url ||
                                        this.props.collection.supplemental_report_url ||
                                        this.props.collection.lidar_breaklines_url) ? (
                                          <Supplementals collection={this.props.collection} />)
                                          : "";

    const servicesCard = this.props.collection.wms_link ? (
                          <Services collection={this.props.collection} />)
                          : "";

    const description = this.props.collection.description ? (
                          <Description collection={this.props.collection} />)
                          : "";

    // using mdc classes to determine grid layout depending on screen size (desktop/tablet)
    // special case with phone or smaller device because order of divs changes
    const gridLayout = window.innerWidth >= 1000 ? (
                          <div className="mdc-layout-grid__inner">
                            <div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-4'>
                              <Metadata collection={this.props.collection} />
                              {lidarCard}
                              {servicesCard}
                              {supplementalDownloadsCard}
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
                              {lidarCard}
                              {servicesCard}
                              {supplementalDownloadsCard}
                              <ShareButtons />
                            </div>
                          </div>);


    return (
      <div className='tnris-download-template-details'>
        <div className='mdc-layout-grid'>

          {gridLayout}

        </div>
      </div>

    );
  }
}
