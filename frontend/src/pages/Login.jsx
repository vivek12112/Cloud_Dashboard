import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  Container, Paper, TextField, Button, Typography, Box, Alert
} from '@mui/material';
import { useAuth } from '../context/AuthContext';

const Login = () => {
  const [credentials, setCredentials] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    try {
      await login(credentials);
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed');
    }
  };

  return (
    <div style={{ backgroundColor: '#f5f5f5', minHeight: '100vh', paddingTop: '64px' }}>
      <Container maxWidth="sm">
        <Paper elevation={3} sx={{ p: 4, backgroundColor: '#ffffff' }}>
          <Typography variant="h4" align="center" gutterBottom sx={{ color: '#1976d2' }}>
            Cloud Platform Login
          </Typography>
          
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          
          <Box component="form" onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label="Username"
              margin="normal"
              value={credentials.username}
              onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
              required
              sx={{ backgroundColor: '#ffffff' }}
            />
            <TextField
              fullWidth
              label="Password"
              type="password"
              margin="normal"
              value={credentials.password}
              onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
              required
              sx={{ backgroundColor: '#ffffff' }}
            />
            <Button
              fullWidth
              type="submit"
              variant="contained"
              size="large"
              sx={{ mt: 3, backgroundColor: '#1976d2', color: '#ffffff' }}
            >
              Login
            </Button>
            <Box sx={{ mt: 2, textAlign: 'center' }}>
              <Link to="/register" style={{ color: '#1976d2' }}>
                Don't have an account? Register
              </Link>
            </Box>
          </Box>
        </Paper>
      </Container>
    </div>
  );
};

export default Login;