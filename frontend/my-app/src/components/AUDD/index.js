import React, {useCallback, useState} from 'react';
import axios from 'axios';
import DISCOGS from "../discogs";
import './audd.css';

function TrackInfo() {
  const [file, setFile] = useState(null);
  const [trackData, setTrackData] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = useCallback((event) => {
    setFile(event.target.files[0]);
  }, []);

  const handleSearch = useCallback(async () => {
    try {
      setError(null);
      const formData = new FormData();
      formData.append('file', file);

      const {data} = await axios.post('http://127.0.0.1:8000/api/audd/', formData);
      setTrackData(data);
        console.log(data)
    } catch (error) {
      setError(error.message);
    }
  }, [file]);

  return (
      <div>
          <div className='TrackInfo'>
                <h5>AUDD mp3 & Genuis Search</h5>
            </div>
          <div className='TrackInfo_buttons'>
        <input type="file" name="file" onChange={handleFileChange}/>
        <button onClick={handleSearch}>Search</button>
        {error && <p>Error: {error}</p>}
          </div>

        {trackData && (
            <div className='TrackInfo'>
              <p>Трек: {trackData.title}</p>
              <p>Исполнитель: {trackData.artist}</p>
              <p>Дата выхода: {trackData.release_date}</p>
              <p>Жанр: {trackData.genre}</p>
              <p>Стиль: {trackData.style}</p>
              <p>Текст песни: {trackData.lyrics}</p>
                <h5>Genuis search</h5>
                <ul>
          {trackData.gen_tracklist.map((item) => (
            <li key={item.url}>
              Название трека: {item.title}
                -Страничка на Genuis: <a href={item.url}>{item.url}</a>
            </li>
          ))}
        </ul>
                <img src ={trackData.gen_url} />
            </div>

        )}
        <div><DISCOGS/></div>
      </div>
  );
}

export default TrackInfo;

/* Рабочий вариант поиска по полям, но на фронте все запросы.
import React, { useState } from 'react';
import axios from 'axios';

function TrackInfo() {
  const [searchType, setSearchType] = useState('fields'); // Режим по умолчанию - поиск по полям
  const [artist, setArtist] = useState('');
  const [title, setTitle] = useState('');
  const [trackData, setTrackData] = useState(null);

  const handleRadioChange = (event) => {
    setSearchType(event.target.value);
  };

  const handleArtistChange = (event) => {
    setArtist(event.target.value);
  };

  const handleTitleChange = (event) => {
    setTitle(event.target.value);
  };

  const handleSearchFields = async () => {
    try {
      const response = await axios.get('https://api.audd.io/', {
        params: {
          method: 'findLyrics',
          q_artist: artist,
          q_track: title,
          q: `${artist} ${title}`,
          api_token: 'cf02182b4372d0a1cd23d4de1be5c8c4',
        },
      });

      setTrackData(response.data.result[0]);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <div>
        <label>
          <input type="radio" value="fields" checked={searchType === 'fields'} onChange={handleRadioChange} />
          Search by fields
        </label>
      </div>

      {searchType === 'fields' && (
        <div>
          <label>Artist:</label>
          <input type="text" name="artist" value={artist} onChange={handleArtistChange} />

          <label>Title:</label>
          <input type="text" name="title" value={title} onChange={handleTitleChange} />

          <button onClick={handleSearchFields}>Search</button>
        </div>
      )}

      {trackData && (
        <div>
          <p>Title: {trackData.title}</p>
          <p>Artist: {trackData.artist}</p>
          <p>Release date: {trackData.release_date}</p>
          <p>Genre: {trackData.genre}</p>
          <p>Style: {trackData.style}</p>
          <p>Lyrics: {trackData.lyrics}</p>
        </div>
      )}
    </div>
  );
}
export default TrackInfo;*/
