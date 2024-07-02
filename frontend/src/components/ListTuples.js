import React, { useState, useEffect } from 'react';
import { Button, Typography, Box, List, ListItem, ListItemText } from '@mui/material/';
import axios from 'axios';

function ListTuples({ username, onUpdateCredits, credits }) {
  const [books, setBooks] = useState([]);

  const fetchTuples = async () => {
    try {
      const response = await axios.get('http://localhost:5000/list_tuples');
      setBooks(response.data.tuples || []);
    } catch (error) {
      console.error('Error listing tuples:', error);
    }
  };


// Caso queiram remover pela lista de tuplas
//   const handleRemoveBook = async (book) => {
//     if (credits <= 0) {
//       alert("Insuficient Credits. Donate more books!");
//       return;
//     }

//     try {
//       const response = await axios.post('http://localhost:5000/get_tuple', {
//         searched_tuple: book,
//         username,
//       });
//       if (response.data.tuple) {
//         alert(`Book removed: ${response.data.tuple}`);
//         onUpdateCredits();
//         fetchTuples();
//       } else {
//         alert(response.data.message);
//       }
//     } catch (error) {
//       console.error('Error removing book:', error);
//     }
//   };

  useEffect(() => {
    fetchTuples();
  }, []);

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold' }}>
        Lista de Livros
      </Typography>
      <Button variant="contained" color="success" onClick={fetchTuples} fullWidth>
        Atualizar
      </Button>
      <List sx={{ mt: 2 }}>
        {books.map((book, index) => (
          <ListItem key={index}>
            <ListItemText primary={book} />
            {/* <ListItemSecondaryAction>
              <IconButton edge="end" aria-label="delete" onClick={() => handleRemoveBook(book)}>
                <DeleteIcon />
              </IconButton>
            </ListItemSecondaryAction> */}
          </ListItem>
        ))}
      </List>
    </Box>
  );
}

export default ListTuples;
