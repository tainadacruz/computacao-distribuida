import React, { useState } from 'react';
import { Button, Grid, TextField, Typography, Box } from '@mui/material/';

function Signup({ onSignup }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSignup(username, password);
  };

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold' }}>
        Signup
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={12}>
          <TextField
            id="username"
            label="Username"
            variant="outlined"
            fullWidth
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} md={12}>
          <TextField
            id="password"
            label="Password"
            variant="outlined"
            fullWidth
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} md={10} />
        <Grid item xs={12} md={2}>
          <Button variant="contained" onClick={handleSubmit} fullWidth>
            Signup
          </Button>
        </Grid>
      </Grid>
    </Box>
  );
}

export default Signup;
