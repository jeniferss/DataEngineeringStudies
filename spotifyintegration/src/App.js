import React, { useEffect, useState } from "react";
import axios from "axios";
import { Typography, Button, Card, List, Avatar } from "antd";

const { Title } = Typography;
const { Meta } = Card;

function App() {
  const CLIENT_ID = process.env.REACT_APP_CLIENT_ID;
  const REDIRECT_URI = process.env.REACT_APP_REDIRECT_URI;
  const AUTH_ENDPOINT = process.env.REACT_APP_AUTH_ENDPOINT;
  const RESONSE_TYPE = process.env.REACT_APP_RESONSE_TYPE;

  const GENRES = ["chill", "classical", "sleep", "study"];

  const [token, setToken] = useState("");
  const [tracks, setTracks] = useState([]);

  const logIn = () => {
    window.open(
      `${AUTH_ENDPOINT}?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=${RESONSE_TYPE}`
    );
  };

  const logOut = () => {
    setTracks([]);
    window.localStorage.removeItem("tracks");
    
    setToken("");
    window.localStorage.removeItem("token");
  };

  const recommendations = async (event) => {
    event.preventDefault();

    const tracksCache = window.localStorage.getItem("tracks");
    if (tracksCache) return

    const { data } = await axios.get(
      "https://api.spotify.com/v1/recommendations",
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        params: {
          limit: 10,
          market: "BR", 
          seed_genres: GENRES.join(","),
        },
      }
    );

    setTracks(data.tracks);
    window.localStorage.setItem("tracks", JSON.stringify(data.tracks));
  };

  const renderTracks = () => {
    return (
      <List
        grid={{
          gutter: 16,
          xs: 1,
          sm: 2,
          md: 3,
          lg: 2,
          xl: 2,
          xxl: 6,
        }}
        dataSource={tracks}
        renderItem={(item) => (
          <List.Item>
            <Card
              hoverable
              style={{
                width: "100%",
              }}
              onClick={() => window.open(`https://open.spotify.com/track/${item.id}`)}
            >
              <Meta
                avatar={
                  <Avatar
                    src={
                      item.album.images.length
                        ? item.album.images[0].url
                        : "/undraw_happy_music_g6wc.svg"
                    }
                  />
                }
                title={`${item.name} #${item.popularity}`}
                description={item.artists
                  .map((artist) => artist.name)
                  .join(", ")}
              />
            </Card>
          </List.Item>
        )}
      />
    );
  };

  useEffect(() => {
    const hash = window.location.hash;
    let tokenString = window.localStorage.getItem("token");

    if (!tokenString && hash) {
      tokenString = hash
        .substring(1)
        .split("&")
        .find((part) => part.startsWith("access_token"))
        .split("=")[1];

      window.localStorage.setItem("token", tokenString);
      window.location.hash = "";
    }

    setToken(tokenString);
  }, []);

  useEffect(() => {
    const tracksCache = window.localStorage.getItem("tracks");
    setTracks(tracksCache ? JSON.parse(tracksCache) : []);
  }, []);

  const frameStyles = {
    padding: "3% 6%",
  };

  const actionBarStyles = {
    display: "flex",
    justifyContent: "flex-end",
    marginBottom: "2%",
  };

  const authButtonStyles = {
    marginRight: "1%",
  };

  const imageStyles = {
    maxWidth: "38%"
  };

  return (
    <div style={frameStyles}>
      <Title level={2}>Recomendação de Músicas</Title>

      <div style={actionBarStyles}>
        <Button
          type="primary"
          size="large"
          onClick={token ? logOut : logIn}
          style={authButtonStyles}
        >
          {token ? "Desautenticar no Spotify" : "Autenticar no Spotify"}
        </Button>

        <Button
          type="primary"
          size="large"
          onClick={recommendations}
          disabled={!token | tracks.length}
        >
          Gerar Recomendações
        </Button>
      </div>

      <div>
        {tracks.length > 0 ? (
          renderTracks()
        ) : (
          <div>
            <Title level={5}>Sem dados para mostrar.</Title>
            <img
              alt="no data"
              style={imageStyles}
              src="/undraw_happy_music_g6wc.svg"
            />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
