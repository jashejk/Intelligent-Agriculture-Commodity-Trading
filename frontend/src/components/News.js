import React from 'react';
import Card from "react-bootstrap/Card";
import styles from './News.module.css';

class News extends React.Component {
  render() {
    const { articles, market } = this.props;
    return (
      <div className={styles.container}>
        {articles.map((article, index) => (
          <a key={index} href={article.link} className={styles.cardLink}>
            <Card className={styles.card}>
              <Card.Body>
                <Card.Title>{article.title}</Card.Title>
                <div className={styles.imageContainer}>
                  <Card.Img variant="top" src={article.media} className={styles.image} />
                </div>
                <Card.Text>{article.body}</Card.Text>
              </Card.Body>
              <Card.Footer>
                <small className="text-muted">{article.time}</small>
              </Card.Footer>
            </Card>
          </a>
        ))}
      </div>
    );
  }
}

export default News;
