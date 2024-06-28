import React, { useState, useEffect, Fragment } from 'react';
import axios from 'axios';
import { Button, Grid, TextField, Typography, Container, Box, List, ListItem } from '@mui/material/';

function App() {
  const [tupleData, setTupleData] = useState('');
  const [searchedTuple, setSearchedTuple] = useState('');
  const [result, setResult] = useState('');
  const [tuples, setTuples] = useState([]);

  console.log(tupleData)

  const handleWriteTuple = async () => {
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
      setTuples(response.data.tuples || []);
    } catch (error) {
      console.error('Error listing tuples:', error);
    }
  };

  useEffect(() => {
    fetchTuples();
  }, []);

  return (
    <div className="App">
    <Fragment>
      <Container maxWidth="md">
        <Box sx={{ textAlign: 'center', mt: 4 }}>
          <Typography variant="h3" gutterBottom>Tuple Space</Typography>
        </Box>
        <Grid container spacing={2} justifyContent="center">
          <Grid item xs={12} md={6}>
            <TextField
              id="outlined-basic" 
              label="Write Tuple" 
              variant="outlined" 
              fullWidth
              value={tupleData} 
              onChange={(e) => setTupleData(e.target.value)}
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <Button variant="contained" onClick={handleWriteTuple} fullWidth>Write</Button>
          </Grid>
          <Grid item xs={12} mt={4}>
            <Typography variant="h5">Get Tuple</Typography>
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              id="search-tuple"
              label="Enter tuple pattern"
              variant="outlined"
              fullWidth
              value={searchedTuple}
              onChange={(e) => setSearchedTuple(e.target.value)}
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <Button variant="contained" onClick={handleGetTuple} fullWidth>Get</Button>
          </Grid>
          <Grid item xs={12}>
            {result && <Typography variant="body1">Result: {result}</Typography>}
          </Grid>
          <Grid item xs={12} mt={4}>
            <Typography variant="h5">List Tuples</Typography>
          </Grid>
          <Grid item xs={12}>
            <Button variant="contained" color="success" onClick={fetchTuples} fullWidth>Refresh</Button>
          </Grid>
          <Grid item xs={12}>
            <List>
              {tuples.map((tuple, index) => (
                <ListItem key={index}>{tuple}</ListItem>
              ))}
            </List>
          </Grid>
        </Grid>
      </Container>
    </Fragment>
    </div>
  );
}

export default App;
