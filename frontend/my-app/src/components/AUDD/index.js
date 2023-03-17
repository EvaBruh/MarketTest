import React, { useState } from 'react';
import axios from 'axios';

function Mp3Uploader() {
    const [mp3File, setMp3File] = useState(null);
    const [trackData, setTrackData] = useState(null);

    const handleFileChange = (event) => {
        setMp3File(event.target.files[0]);
    };

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append('file', mp3File);

        try {
            const response = await axios.post('https://api.audd.io/', {
                data: formData,
                params: {
                    method: 'recognize',
                    api_token: 'cf02182b4372d0a1cd23d4de1be5c8c4',

                },
            });

            setTrackData(response.data);
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload</button>
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

export default Mp3Uploader;
