import React, { useState } from 'react';
import { Button, Grid, TextField, Typography, Box } from '@mui/material/';
import axios from 'axios';

function Get({ username, password, onUpdateCredits }) {
  const [searchedTuple, setSearchedTuple] = useState('');
  const [result, setResult] = useState('');

  const handleGetTuple = async () => {
    try {
      const response = await axios.post('http://localhost:5000/get_tuple', {
        searched_tuple: searchedTuple,
        username,
      });
      setResult(response.data.tuple || response.data.message);
      onUpdateCredits();
    } catch (error) {
      console.error('Error getting tuple:', error);
    }
  };

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold' }}>
        Buscar Livros
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={12}>
          <TextField
            id="search-tuple"
            label="Digite o padrão de tupla"
            variant="outlined"
            fullWidth
            value={searchedTuple}
            onChange={(e) => setSearchedTuple(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} md={10} />
        <Grid item xs={12} md={2}>
          <Button variant="contained" onClick={handleGetTuple} fullWidth>
            Buscar
          </Button>
        </Grid>
      </Grid>
      {result && (
        <Box sx={{ mt: 2 }}>
          <Typography variant="body1">Resultado: {result}</Typography>
        </Box>
      )}
    </Box>
  );
}

export default Get;
