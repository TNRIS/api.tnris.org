import React from 'react';

import { Carousel } from 'react-responsive-carousel';

export default class Images extends React.Component {
  render() {

    const all_images = this.props.images.split(',');
    const thumbnail = this.props.thumbnail;
    const carousel_images = [];

    all_images.map(function(url) {
      if (url !== thumbnail) {
        carousel_images.push(url);
      }
      return url;
    });

    return (

      <div className="template-content-div">
        <div>
          <Carousel
            autoPlay={true}
            infiniteLoop={true}
            showThumbs={true}
            emulateTouch
            useKeyboardArrows={true}
            transitionTime={700} >
            {
              carousel_images.map(url => (
                <div key={url}>
                  <img src={url} alt='' />
                </div>
                )
              )
            }
          </Carousel>
        </div>
      </div>
    )
  }
}
