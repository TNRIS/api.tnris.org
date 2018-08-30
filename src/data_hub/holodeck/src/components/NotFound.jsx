import React, { Component } from 'react';
import Header from './Header';
import Footer from './Footer';

class NotFound extends Component {

  render() {
    return (
      <div className="notfound-component">
        <Header />
          <div className="notfound">
            <img
              src="http://www.startrek.com/uploads/assets/db_articles/d3c7e2f13d99edef700ed6b48fbfb694579299d2.jpg"
              alt="Lieutenant Commander Data"
              className="notfound-image"
              />
            <h2>ERROR 404: Not Found</h2>
            <p>The page you're looking for does not exist.</p>
          </div>
        <Footer className='footer navbarFixedBottom' />
      </div>
    )
  }
}

export default NotFound
