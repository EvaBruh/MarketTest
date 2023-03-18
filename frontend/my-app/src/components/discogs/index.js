import React, {useCallback, useState} from 'react';
import axios from 'axios';
import '../AUDD/audd.css';

function TrackInfo() {
    const [artist, setArtist] = useState('');
    const [title, setTitle] = useState('');
    const [trackData, setTrackData] = useState(null);
    const [error, setError] = useState(null);

    const handleArtistChange = useCallback((event) => {
        setArtist(event.target.value);
    }, []);

    const handleTitleChange = useCallback((event) => {
        setTitle(event.target.value);
    }, []);

    const handleSearch = useCallback(async () => {
        try {
            setError(null);

            const {data} = await axios.post('http://127.0.0.1:8000/api/discogs/', {artist, title});
            setTrackData(data);

        } catch (error) {
            setError(error.message);
        }
    }, [artist, title]);

    return (
        <div>
            <div className='TrackInfo'>
                <h5>Discogs Search</h5>
            </div>
            <div className='TrackInfo_buttons'>
            <input type="text" name="artist" value={artist} onChange={handleArtistChange} placeholder="Исполнитель"/>
            <input type="text" name="title" value={title} onChange={handleTitleChange} placeholder="Имя трека"/>
            <button onClick={handleSearch}>Search</button>
            </div>
            {error && <p>Error: {error}</p>}

            {trackData && (
                <div className='TrackInfo'>
                    <p>Исполнитель: {trackData.artist}</p>
                    <p>Трек: {trackData.title}</p>
                    <p>Год: {trackData.year}</p>
                    <p>Лейбл: {trackData.label}</p>
                    <p>Cat No: {trackData.catno}</p>
                    <p>Формат: {trackData.format}</p>
                </div>
            )}
        </div>
    );
}

export default TrackInfo;