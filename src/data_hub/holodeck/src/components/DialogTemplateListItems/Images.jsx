import React from 'react';

import { Carousel } from 'react-responsive-carousel';

export default class Images extends React.Component {
  render() {
    const carousel_images = this.props.images.split(',');
    const multiImage = carousel_images.length > 1 ? true : false;

    return (

      <div className="template-content-div">
        <div>
          <Carousel
            autoPlay={multiImage}
            infiniteLoop={multiImage}
            showThumbs={multiImage}
            emulateTouch
            useKeyboardArrows={true}
            transitionTime={700}
            interval={6000}
            showIndicators={multiImage}
            showStatus={multiImage} >
            {
              carousel_images.map(url => (
                <div key={url}>
                  <img className='max-img-size' src={url} alt='' />
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
