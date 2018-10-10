import React from 'react';

import { Carousel } from 'react-responsive-carousel';

export default class TnrisDownloadTemplateImages extends React.Component {
  constructor(props) {
      super(props);
      console.log(this.props);
  }

  render() {

    const imageUrls = [];
    Object.keys(this.props).map(key => this.props[key] !== null ? imageUrls.push(this.props[key]) : '')

    console.log(imageUrls);

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
              imageUrls.map(url =>
                <div key={url}>
                  <img src={url} alt='' />
                </div>
              )
            }
          </Carousel>
        </div>

        <div className="mobile">
          {
            imageUrls.map(url =>
              <div key={url}>
                <img src={url} alt='' />

                  

              </div>
            )
          }
        </div>
      </div>
    )
  }
}
