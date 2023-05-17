import React, { Component, createRef } from 'react';
import Header from './Header';
import CropSelection from './CropSelection';
import News from './News';
import { Container, Row, Col, Card } from 'react-bootstrap';
import Tableau from "tableau-react";
import styles from './App.css';

class App extends React.Component {
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

  componentDidMount() {
    this.scrollDivToBottom();
  }

  componentDidUpdate() {
    this.scrollDivToBottom();
  }

  scrollDivToBottom() {
    const scrollTo = (element, from, to, duration) => {
      if (duration <= 0) return;
    
      if (typeof from === 'object') from = from.offsetTop;
      if (typeof to === 'object') to = to.offsetTop;
    
      scrollToX(element, from, to, 0, 1 / duration, 20, easeOutCuaic);
    };
    
    const scrollToX = (element, xFrom, xTo, t01, speed, step, motion) => {
      if (t01 < 0 || t01 > 1 || speed <= 0) {
        element.scrollTop = xTo;
        return;
      }
    
      element.scrollTop = xFrom - (xFrom - xTo) * motion(t01);
      t01 += speed * step;
    
      setTimeout(() => {
        scrollToX(element, xFrom, xTo, t01, speed, step, motion);
      }, step);
    };
    
    const easeOutCuaic = (t) => {
      t--;
      return t * t * t + 1;
    };
  
    const { current: scrollableDiv } = this.scrollableDivRef;
    if (scrollableDiv) {
      scrollTo(scrollableDiv, scrollableDiv.scrollTop, 0, 10); // Scroll to top in 4 seconds and some milliseconds
    
      setTimeout(() => {
        scrollTo(scrollableDiv, scrollableDiv.scrollTop, scrollableDiv.scrollHeight, 10000); // Scroll to bottom in 4 seconds and some milliseconds
      }, 4000); // Delay the second scroll by 4 seconds to match the original code
    }
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
                  <Card style={{ marginBottom: '20px', backgroundColor: this.state.market === 1 ? 'rgb(10, 200, 10)' : 'rgb(255, 50, 10)' }}>
                    <Card.Body>
                      <Card.Text>
                        {this.state.market === 1 ? 'Market will be up tomorrow' : 'Market will be down tomorrow'}
                      </Card.Text>
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

export default App;
