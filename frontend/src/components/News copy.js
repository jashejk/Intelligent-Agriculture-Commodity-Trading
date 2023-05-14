import React from 'react';
import Card from "react-bootstrap/Card";
import CardGroup from "react-bootstrap/Card";
import styles from './News.module.css';

class News extends React.Component {
    scrollContainer = React.createRef();
  
    componentDidMount() {
      this.startAutoScroll();
    }
    
    startAutoScroll = () => {
      const node = this.scrollContainer.current;
  
      if (node) {
        node.scrollLeft += 1;
  
        if (node.scrollLeft + node.offsetWidth >= node.scrollWidth) {
          node.scrollLeft = 0;
        }
  
        window.requestAnimationFrame(this.startAutoScroll);
      }
    }

  render() {
    const { articles, market } = this.props;
    return (
        <div ref={this.scrollContainer} className={styles.container}>
            <CardGroup>
                {articles.map((article, index) => (
                <Card key={index} >
                    <Card.Body>
                    <Card.Title>{article.title}</Card.Title>
                    <Card.Img variant="top" src={article.media} />
                    <Card.Text>{article.body}</Card.Text>
                    <Card.Link href={article.link}>Read article</Card.Link>
                    </Card.Body>
                    <Card.Footer>
                    <small className="text-muted">{market}</small>
                    </Card.Footer>
                </Card>
                
                ))}
            </CardGroup>
        </div>
      
    );
  }
}

export default News;

