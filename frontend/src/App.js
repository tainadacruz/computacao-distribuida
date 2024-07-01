import React, { useState, useEffect, Fragment } from 'react';
import axios from 'axios';
import { Button, Grid, TextField, Typography, Container, Box, List, ListItem, AppBar, Toolbar, Tabs, Tab } from '@mui/material/';

function App() {
  const [bookName, setBookName] = useState('');
  const [author, setAuthor] = useState('');
  const [publisher, setPublisher] = useState('');
  const [year, setYear] = useState('');
  const [genre, setGenre] = useState('');
  const [searchedTuple, setSearchedTuple] = useState('');
  const [result, setResult] = useState('');
  const [books, setBooks] = useState([]);
  const [tabValue, setTabValue] = useState(0);

  const handleWriteTuple = async () => {
    const tupleData = `${bookName || '*'}, ${author || '*'}, ${publisher || '*'}, ${year || '*'}, ${genre || '*'}`;
    try {
      const response = await axios.post('http://localhost:5000/write_tuple', { tuple_data: tupleData });
      alert(response.data.message);
      fetchTuples();
    } catch (error) {
      console.error('Error writing tuple:', error);
    }
  };

  const handleGetTuple = async () => {
    try {
      const response = await axios.post('http://localhost:5000/get_tuple', { searched_tuple: searchedTuple });
      setResult(response.data.tuple || response.data.message);
      fetchTuples();
    } catch (error) {
      console.error('Error getting tuple:', error);
    }
  };

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

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  return (
    <div className="App">
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Sistema de Registro de Livros
          </Typography>
          <Tabs value={tabValue} onChange={handleTabChange} indicatorColor="secondary" textColor="inherit">
            <Tab label="Registrar Livros" />
            <Tab label="Buscar Livros" />
            <Tab label="Lista de Livros Registrados" />
          </Tabs>
        </Toolbar>
      </AppBar>
      <Container maxWidth="md">
        <Box sx={{ textAlign: 'center', mt: 4 }}>
          <Typography variant="h3" gutterBottom sx={{ fontWeight: 'bold' }}>
            Sistema de Registro de Livros
          </Typography>
        </Box>
        {tabValue === 0 && (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold' }}>
              Registrar Livros
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
        )}
        {tabValue === 1 && (
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
        )}
        {tabValue === 2 && (
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
        )}
      </Container>
    </div>
  );
}

export default App;
