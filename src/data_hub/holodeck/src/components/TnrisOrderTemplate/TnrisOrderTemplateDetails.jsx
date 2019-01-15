import React from 'react';

import CountyCoverageContainer from '../../containers/CountyCoverageContainer'
import Description from '../DialogTemplateListItems/Description'
import LidarBlurb from '../DialogTemplateListItems/LidarBlurb'
import Metadata from '../DialogTemplateListItems/Metadata'
import Services from '../DialogTemplateListItems/Services'
import Supplementals from '../DialogTemplateListItems/Supplementals'
import ShareButtons from '../DialogTemplateListItems/ShareButtons'
import Images from '../DialogTemplateListItems/Images'

// import ContactContainer from '../../containers/ContactContainer';

export default class TnrisDownloadTemplateDetails extends React.Component {

  render() {
    const countyCoverageCard = this.props.collection.counties ?
                                (<div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-6'>
                                  <CountyCoverageContainer counties={this.props.collection.counties} />
                                </div>)
                                : "";

    const imageCarousel = this.props.collection.images ?
                        (<div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-6'>
                          <Images
                            thumbnail={this.props.collection.thumbnail_image}
                            images={this.props.collection.images} />
                        </div>)
                        : "";

    const lidarCard = this.props.collection.category === 'Lidar' ?
                        (<div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-12'>
                          <LidarBlurb />
                        </div>)
                        : "";

    const supplementalDownloadsCard = (this.props.collection.tile_index_url ||
                                        this.props.collection.supplemental_report_url ||
                                        this.props.collection.lidar_breaklines_url) ?
                                          (<div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-6'>
                                            <Supplementals collection={this.props.collection} />
                                          </div>)
                                          : "";

    const servicesCard = this.props.collection.wms_link ?
                          (<div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-6'>
                            <Services collection={this.props.collection} />
                          </div>)
                          : "";

    const description = this.props.collection.description ?
                          (<div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-6'>
                            <Description collection={this.props.collection} />
                          </div>)
                          : "";

    return (
      <div className='tnris-order-template-details'>
        <div className='mdc-layout-grid'>
          <div className="mdc-layout-grid__inner">

            <div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-6'>
              <Metadata collection={this.props.collection} />
            </div>

            {imageCarousel}
            {description}
            {countyCoverageCard}
            {lidarCard}
            {servicesCard}
            {supplementalDownloadsCard}

            <div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-12'>
              <ShareButtons />
            </div>

          </div>
        </div>
      </div>
    );
  }
}
