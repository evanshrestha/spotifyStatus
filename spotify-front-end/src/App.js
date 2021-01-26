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
      const loadingStrings = ["Asking the magic conch...", "Wingardiuming some leviosas..."];
      const loadingString = loadingStrings[Math.floor(Math.random()*loadingStrings.length)];

      return <div>{loadingString}</div>;
    } else {

      if (current) {

        const songLink = current.link;
        const songName = current.name;
        const songImageLink = current.image;
        var artistNames = [];

        for (var i = 0; i < current.artists.length; i++) {
          artistNames.push(<a href={current.artists[i].link} target="_parent">{current.artists[i].name}</a>);
          if ((i < current.artists.length - 1) && (current.artists.length > 2)) {
            artistNames.push(', ');
          }
          if (i === current.artists.length - 2) {
            artistNames.push(' and ');
          }
        }
        const listeningStrings = ["Join in!", "Typical.", "Maybe you should fix him.", "Wanna listen?"];
        const listeningString = listeningStrings[Math.floor(Math.random()*listeningStrings.length)];

        return (
          <div class='card' style={{ width: '500px' }}>
            <div class='row no-gutters'>
              <div class='col-sm-5'>
                <img class='card-img' src={songImageLink} />
              </div>
              <div class='col-sm-7'>
                <div class='card-body'>
                  <h5 class='card-title'>Evan's listening to <a href={ songLink } target="_parent">{ songName }</a> by { artistNames }.</h5>
                  <p class='card-text'>{ listeningString }</p>
                </div>
              </div>
            </div>
          </div>
        );
      } else {

        const notListeningStrings = ["Maybe later!", "That'll change soon.", "We'll see how long that lasts."];
        const notListeningString = notListeningStrings[Math.floor(Math.random()*notListeningStrings.length)];

        return (
          <div class='card' style={{ width: '500px' }}>
            <div class='row no-gutters'>
              <div class='col-sm-7'>
                <div class='card-body'>
                  <h5 class='card-title'>Evan's not listening to anything right now.</h5>
                  <p class='card-text'>{ notListeningString }</p>
                </div>
              </div>
            </div>
          </div>
        );
      }
    }
  }
}
export default App;
