import React, { useState } from 'react';
import { Button, Grid, TextField, Typography, Box } from '@mui/material/';
import axios from 'axios';

function Write({ username, onUpdateCredits }) {
  const [bookName, setBookName] = useState('');
  const [author, setAuthor] = useState('');
  const [publisher, setPublisher] = useState('');
  const [year, setYear] = useState('');
  const [genre, setGenre] = useState('');

  const handleWriteTuple = async () => {
    const tupleData = `${bookName || '*'}, ${author || '*'}, ${publisher || '*'}, ${year || '*'}, ${genre || '*'}`;
    try {
      const response = await axios.post('http://localhost:5000/write_tuple', {
        tuple_data: tupleData,
        username,
      });
      alert(response.data.message);
      onUpdateCredits();
    } catch (error) {
      console.error('Error writing tuple:', error);
    }
  };

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold' }}>
        Registrar Livro
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <TextField
            id="book-name"
            label="Título"
            variant="outlined"
            fullWidth
            value={bookName}
            onChange={(e) => setBookName(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <TextField
            id="author"
            label="Autor"
            variant="outlined"
            fullWidth
            value={author}
            onChange={(e) => setAuthor(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <TextField
            id="publisher"
            label="Editora"
            variant="outlined"
            fullWidth
            value={publisher}
            onChange={(e) => setPublisher(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <TextField
            id="year"
            label="Ano"
            variant="outlined"
            fullWidth
            value={year}
            onChange={(e) => setYear(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} md={12}>
          <TextField
            id="genre"
            label="Gênero"
            variant="outlined"
            fullWidth
            value={genre}
            onChange={(e) => setGenre(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} md={10} />
        <Grid item xs={12} md={2}>
          <Button variant="contained" onClick={handleWriteTuple} fullWidth>
            Registrar
          </Button>
        </Grid>
      </Grid>
    </Box>
  );
}

export default Write;
