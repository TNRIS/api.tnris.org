import React from 'react';

import { Carousel } from 'react-responsive-carousel';

export default class TnrisDownloadTemplateImages extends React.Component {
  constructor(props) {
      super(props);
  }

  render() {

    const all_images = this.props.images.split(',');
    const thumbnail = this.props.thumbnail;
    const carousel_images = [];

    all_images.map(function(url) {
      if (url !== thumbnail) {
        carousel_images.push(url);
      }
    });

    return (

      <div className="tnris-download-template-images">
        <div className="desktop-lg">
          <Carousel
            autoPlay={true}
            showThumbs={false}
            infiniteLoop={true}
            emulateTouch
            useKeyboardArrows={true}
            transitionTime={700}
          >

            {
              carousel_images.map(url => ( <div key={url}><img src={url} alt='' /></div> ))
            }
          </Carousel>
        </div>

        <div className="mobile">
          {
            carousel_images.map(url => ( <div key={url}><img src={url} alt='' /></div> ))
          }
        </div>
      </div>
    )
  }
}
