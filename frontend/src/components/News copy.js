import React, { Component, createRef } from 'react';
import Header from './Header';
import CropSelection from './CropSelection';
import News from './News';
import { Container, Row, Col, Card } from 'react-bootstrap';
import Tableau from "tableau-react";
import styles from './App.css';

class Homepage extends React.Component {
  state = {
    selectedCrop: '',
    dashboardID: 'https://public.tableau.com/views/Historicalanalysiscornprice/Sheet1?:language=en-US&:display_count=y&:origin=viz_share_link',
    newsArticles: [],
    market: ''
  }

  handleCropSelection = (crop, dashboardID, newsArticles, market) => {
    this.setState({
      selectedCrop: crop,
      dashboardID: dashboardID,
      newsArticles: newsArticles,
      market: market
    });
  }

  constructor(props) {
    super(props);
    this.scrollableDivRef = React.createRef();
  }

  componentDidUpdate() {
    // Scroll to the bottom of the div whenever its content changes
    this.scrollableDivRef.current.scrollTop = this.scrollableDivRef.current.scrollHeight;
  }

  render() {
    return (
      <div>
        <Header />
        <main style={{ marginTop: '58px' }}>
          <Container fluid>
            <Row>
              <Col>
                <CropSelection onSelectCrop={this.handleCropSelection} />
              </Col>
            </Row>
            <Row>
              <Col md={9}>
                <Tableau 
                  url={this.state.dashboardID}
                  options={{ debug: false }}
                />
              </Col>
              <Col md={3}>
                {this.state.market && (
                  <Card style={{ marginBottom: '20px' }}>
                    <Card.Body>
                      <Card.Text>{this.state.market}</Card.Text>
                    </Card.Body>
                  </Card>
                )}
                <div className="scrollable-div" ref={this.scrollableDivRef}>
                  <News articles={this.state.newsArticles} market={this.state.market} />
                </div>
              </Col>
            </Row>
          </Container>
        </main>
      </div>
    );
  }
}

export default Homepage;
