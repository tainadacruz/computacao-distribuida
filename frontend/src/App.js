import React, { useState, useEffect, Fragment } from 'react';
import axios from 'axios';
import { Button, Grid, TextField, Typography, Container, Box, List, ListItem, AppBar, Toolbar, Tabs, Tab } from '@mui/material/';
import Login from './components/Login';
import Signup from './components/Signup';
import Write from './components/Write';
import Get from './components/Get';
import ListTuples from './components/ListTuples';

function App() {
  const [tabValue, setTabValue] = useState(0);
  const [authenticated, setAuthenticated] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleLogin = async (username, password) => {
    try {
      const response = await axios.post('http://localhost:5000/login', { username, password });
      if (response.data.authenticated) {
        setAuthenticated(true);
        setUsername(username);
        setPassword(password);
      } else {
        alert('Login failed');
      }
    } catch (error) {
      console.error('Error logging in:', error);
    }
  };

  const handleSignup = async (username, password) => {
    try {
      const response = await axios.post('http://localhost:5000/signup', { username, password });
      if (response.data.created) {
        alert('Signup successful');
        setTabValue(0); // Redirect to login
      } else {
        alert('Signup failed');
      }
    } catch (error) {
      console.error('Error signing up:', error);
    }
  };

  const handleLogout = () => {
    setAuthenticated(false);
    setUsername('');
    setPassword('');
    setTabValue(0);
  };

  return (
    <div className="App">
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Sistema de Registro de Livros
          </Typography>
          <Tabs value={tabValue} onChange={handleTabChange} indicatorColor="secondary" textColor="inherit">
            {!authenticated && <Tab label="Login" />}
            {!authenticated &&<Tab label="Signup" />}
            {authenticated && <Tab label="Registrar Livros" />}
            {authenticated && <Tab label="Buscar Livros" />}
            {authenticated && <Tab label="Lista de Livros Registrados" />}
          </Tabs>
          {authenticated && (
            <Button color="inherit" onClick={handleLogout}>
              Logout
            </Button>
          )}
        </Toolbar>
      </AppBar>
      <Container maxWidth="md">
        <Box sx={{ textAlign: 'center', mt: 4 }}>
          <Typography variant="h3" gutterBottom sx={{ fontWeight: 'bold' }}>
            Sistema de Registro de Livros
          </Typography>
        </Box>
        {!authenticated && tabValue === 0 && <Login onLogin={handleLogin} />}
        {!authenticated && tabValue === 1 && <Signup onSignup={handleSignup} />}
        {authenticated && tabValue === 0 && <Write username={username} password={password} />}
        {authenticated && tabValue === 1 && <Get username={username} password={password} />}
        {authenticated && tabValue === 2 && <ListTuples />}
      </Container>
    </div>
  );
}

export default App;
