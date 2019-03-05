import React from 'react';

import SourceCitation from '../DialogTemplateListItems/SourceCitation'
import Metadata from '../DialogTemplateListItems/Metadata'
import HistoricalProducts from '../DialogTemplateListItems/HistoricalProducts'
import Ls4Links from '../DialogTemplateListItems/Ls4Links'
import ShareButtons from '../DialogTemplateListItems/ShareButtons'
import Images from '../DialogTemplateListItems/Images'


export default class TnrisDownloadTemplateDetails extends React.Component {
  constructor(props) {
    super(props)

    window.innerWidth >= 1000 ? this.state = {
      gridLayout:'desktop'
    } : this.state = {
      gridLayout:'mobile'
    };

    this.handleResize = this.handleResize.bind(this);
  }

  componentDidMount() {
    window.addEventListener("resize", this.handleResize);
  }

  componentWillUnmount() {
    window.removeEventListener("resize", this.handleResize);
  }

  handleResize() {
    if (window.innerWidth >= 1000) {
      this.setState({gridLayout:'desktop'});
    }
    else {
      this.setState({gridLayout:'mobile'});
    }
  }

  render() {
    const imageCarousel = this.props.collection.images ? (
                          <Images
                            thumbnail={this.props.collection.thumbnail_image}
                            images={this.props.collection.images} />)
                        : (
                          <Images
                            thumbnail={this.props.collection.thumbnail_image}
                            images={this.props.collection.thumbnail_image} />
                        );

    const productsCard = this.props.collection.products ? (
                          <HistoricalProducts products={this.props.collection.products} />)
                          : "";

    const ls4LinksCard = (this.props.collection.index_service_url && this.props.collection.index_service_url !== "") ||
                         (this.props.collection.mosaic_service_url && this.props.collection.mosaic_service_url !== "") ||
                         (this.props.collection.frames_service_url && this.props.collection.frames_service_url !== "") ||
                         (this.props.collection.scanned_index_ls4_links && this.props.collection.scanned_index_ls4_links) !== "" ? (
                         <Ls4Links index={this.props.collection.index_service_url}
                                     mosaic={this.props.collection.mosaic_service_url}
                                     frames={this.props.collection.frames_service_url}
                                     scans={this.props.collection.scanned_index_ls4_links} />)
                         : "";

    const sourceCitation = this.props.collection.template === 'historical-aerial' ?
                            <SourceCitation collection={this.props.collection} />
                          : "";

    const acquisition = this.props.collection.acquisition_date ? this.props.collection.acquisition_date.substring(0, 4) : '';
    const acq_year = this.props.collection.template !== 'outside-entity' && this.props.collection.acquisition_date ? (
      <span>{acquisition}</span>
    ) : "";

    const description = (
      <div className="template-content-div">
        {this.props.collection.about ? <p>{this.props.collection.about}</p> : ""}
        <p>
          Use the <strong>Order</strong> tab to submit a request to RDC and acquire digital or physical copies of this {this.props.collection.name} {acq_year} Historic Imagery dataset.
        </p>
      </div>
    );

    const archiveAbout = (
      <div className="template-content-div">
        <p className="mdc-typography--headline6">About the Historic Imagery Archive</p>
        <p>
          The Historical Imagery Archive maintained by TNRIS is one of our most used and important data collections. It is comprised of over 1 million frames of photos covering all parts of Texas from dates as far back as the 1920s.
        </p>
        <p>
          The TNRIS Research & Distribution Center (RDC) is charged with preserving this collection, distributing it to the public, and continuing with the large task of digitizing the frames.
        </p>
      </div>
    );

     // using mdc classes to determine grid layout depending on screen size (desktop/tablet)
     // special case with phone or smaller device because order of divs changes
     const gridLayout = window.innerWidth >= 1000 ? (
                           <div className="mdc-layout-grid__inner">
                             <div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-4'>
                               <Metadata collection={this.props.collection} />
                               {archiveAbout}
                               {productsCard}
                               {ls4LinksCard}
                               <ShareButtons />
                             </div>
                             <div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-8'>
                               {imageCarousel}
                               <div className="mdc-layout-grid__inner">
                                 <div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-8'>
                                   {description}
                                 </div>
                                 <div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-4'>
                                   {sourceCitation}
                                 </div>
                               </div>
                             </div>
                           </div>) : (
                           <div className="mdc-layout-grid__inner">
                             <div className='mdc-layout-grid__cell mdc-layout-grid__cell--span-12'>
                               {imageCarousel}
                               <Metadata collection={this.props.collection} />
                               {description}
                               {sourceCitation}
                               {archiveAbout}
                               {productsCard}
                               {ls4LinksCard}
                               <ShareButtons />
                             </div>
                           </div>);

    return (
      <div className='historical-aerial-template-details'>
        <div className='mdc-layout-grid'>

          {gridLayout}

        </div>
      </div>
    );
  }
}
