import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  Container, Paper, TextField, Button, Typography, Box, Alert, Select,
  MenuItem, FormControl, InputLabel
} from '@mui/material';
import { useAuth } from '../context/AuthContext';

const Register = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password2: '',
    first_name: '',
    last_name: '',
    role: 'user',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    try {
      await register(formData);
      setSuccess(true);
      setTimeout(() => navigate('/login'), 2000);
    } catch (err) {
      setError(err.response?.data?.username?.[0] || 'Registration failed');
    }
  };

  return (
    <div style={{ backgroundColor: '#f5f5f5', minHeight: '100vh', paddingTop: '64px' }}>
      <Container maxWidth="sm">
        <Paper elevation={3} sx={{ p: 4, backgroundColor: '#ffffff' }}>
          <Typography variant="h4" align="center" gutterBottom sx={{ color: '#1976d2' }}>
            Register
          </Typography>
          
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          {success && <Alert severity="success" sx={{ mb: 2 }}>Registration successful! Redirecting...</Alert>}
          
          <Box component="form" onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label="Username"
              margin="normal"
              value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
              required
              sx={{ backgroundColor: '#ffffff' }}
            />
            <TextField
              fullWidth
              label="Email"
              type="email"
              margin="normal"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              required
              sx={{ backgroundColor: '#ffffff' }}
            />
            <TextField
              fullWidth
              label="First Name"
              margin="normal"
              value={formData.first_name}
              onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
              sx={{ backgroundColor: '#ffffff' }}
            />
            <TextField
              fullWidth
              label="Last Name"
              margin="normal"
              value={formData.last_name}
              onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
              sx={{ backgroundColor: '#ffffff' }}
            />
            <FormControl fullWidth margin="normal" sx={{ backgroundColor: '#ffffff' }}>
              <InputLabel>Role</InputLabel>
              <Select
                value={formData.role}
                label="Role"
                onChange={(e) => setFormData({ ...formData, role: e.target.value })}
              >
                <MenuItem value="user">Standard User</MenuItem>
                <MenuItem value="admin">Administrator</MenuItem>
                <MenuItem value="operator">Cloud Operator</MenuItem>
                <MenuItem value="analyst">Finance Analyst</MenuItem>
                <MenuItem value="engineer">Network Engineer</MenuItem>
                <MenuItem value="support">Support Staff</MenuItem>
              </Select>
            </FormControl>
            <TextField
              fullWidth
              label="Password"
              type="password"
              margin="normal"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              required
              sx={{ backgroundColor: '#ffffff' }}
            />
            <TextField
              fullWidth
              label="Confirm Password"
              type="password"
              margin="normal"
              value={formData.password2}
              onChange={(e) => setFormData({ ...formData, password2: e.target.value })}
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
              Register
            </Button>
            <Box sx={{ mt: 2, textAlign: 'center' }}>
              <Link to="/login" style={{ color: '#1976d2' }}>
                Already have an account? Login
              </Link>
            </Box>
          </Box>
        </Paper>
      </Container>
    </div>
  );
};

export default Register;