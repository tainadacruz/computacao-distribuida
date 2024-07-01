import React, { useState, useEffect } from 'react';
import { Button, Typography, Box, List, ListItem } from '@mui/material/';
import axios from 'axios';

function ListTuples() {
  const [books, setBooks] = useState([]);

  const fetchTuples = async () => {
    try {
      const response = await axios.get('http://localhost:5000/list_tuples');
      setBooks(response.data.tuples || []);
    } catch (error) {
      console.error('Error listing tuples:', error);
    }
  };

  useEffect(() => {
    fetchTuples();
  }, []);

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold' }}>
        Lista de Livros Registrados
      </Typography>
      <Button variant="contained" color="success" onClick={fetchTuples} fullWidth>
        Atualizar
      </Button>
      <List sx={{ mt: 2 }}>
        {books.map((book, index) => (
          <ListItem key={index}>{book}</ListItem>
        ))}
      </List>
    </Box>
  );
}

export default ListTuples;
