import React from 'react';
import Row from 'react-bootstrap/Row';
import Container from 'react-bootstrap/Container';
import Image from 'react-bootstrap/Image';
import Col from 'react-bootstrap/Col';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return <Status />;
}

class Status extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      current: null
    };
  }

  componentDidMount() {
    fetch("https://spotify.evanshrestha.com:5002/api/current")
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            current: result
          });
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
  }

  render() {
    const { error, isLoaded, current } = this.state;
    if (error) {
      return <div>Hmm, something went wrong: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Asking the magic conch...</div>;
    } else {

      if (current) {

        const songLink = current.link;
        const songName = current.name;
        const songImageLink = current.image;
        var artistNames = [];

        for (var i = 0; i < current.artists.length; i++) {
          artistNames.push(<a href={current.artists[i].link}>{current.artists[i].name}</a>);
          if ((i < current.artists.length - 1) && (current.artists.length > 2)) {
            artistNames.push(', ');
          }
          if (i === current.artists.length - 2) {
            artistNames.push(' and ');
          }
        }
        const ListeningStrings = ["Join in!", "Typical.", "Maybe you should fix him.", "Wanna listen?"];
        const notListeningString = ListeningStrings[Math.floor(Math.random()*ListeningStrings.length)];

        return (
          <Container>
            <Row>
              <Col>
                <Image variant="top" src={songImageLink} width={ 100 }/>
                <span style={{ marginLeft: '10px' }}>Evan's listening to <a href={ songLink }>{ songName }</a> by { artistNames } right now. { notListeningString }</span>
              </Col>
            </Row>
          </Container>
        );
      } else {

        const notListeningStrings = ["It doesn't look like Evan's listening to anything right now. Maybe later!",
                                     "Looks like Evan's Spotify isn't playing. That'll change soon."];

        const notListeningString = notListeningStrings[Math.floor(Math.random()*notListeningStrings.length)];
        return (
          <Container>
            <Row>
              <Col>
                <span style={{ marginLeft: '10px' }}>{ notListeningString }</span>
              </Col>
            </Row>
          </Container>
        );
      }
    }
  }
}
export default App;
