import { useState, useEffect } from 'react';
import {
  Box, Typography, Button, Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Paper, Chip, Dialog, DialogTitle, DialogContent,
  DialogActions, TextField, Select, MenuItem, FormControl, InputLabel
} from '@mui/material';
import { Add } from '@mui/icons-material';
import { supportAPI } from '../services/api';

const Support = () => {
  const [tickets, setTickets] = useState([]);
  const [open, setOpen] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority: 'medium',
  });

  useEffect(() => {
    fetchTickets();
  }, []);

  const fetchTickets = async () => {
    try {
      const response = await supportAPI.getTickets();
      setTickets(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching tickets:', error);
    }
  };

  const handleCreate = async () => {
    try {
      await supportAPI.createTicket(formData);
      setOpen(false);
      fetchTickets();
      setFormData({ title: '', description: '', priority: 'medium' });
    } catch (error) {
      console.error('Error creating ticket:', error);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      open: 'error',
      in_progress: 'warning',
      resolved: 'success',
      closed: 'default',
    };
    return colors[status] || 'default';
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Support Tickets</Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => setOpen(true)}
        >
          Create Ticket
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Title</TableCell>
              <TableCell>Priority</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Created</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {tickets.map((ticket) => (
              <TableRow key={ticket.id}>
                <TableCell>#{ticket.id}</TableCell>
                <TableCell>{ticket.title}</TableCell>
                <TableCell>
                  <Chip label={ticket.priority} size="small" />
                </TableCell>
                <TableCell>
                  <Chip
                    label={ticket.status}
                    color={getStatusColor(ticket.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>{new Date(ticket.created_at).toLocaleDateString()}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Create Support Ticket</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Title"
            margin="normal"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
          />
          <TextField
            fullWidth
            label="Description"
            multiline
            rows={4}
            margin="normal"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
          />
          <FormControl fullWidth margin="normal">
            <InputLabel>Priority</InputLabel>
            <Select
              value={formData.priority}
              label="Priority"
              onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
            >
              <MenuItem value="low">Low</MenuItem>
              <MenuItem value="medium">Medium</MenuItem>
              <MenuItem value="high">High</MenuItem>
              <MenuItem value="urgent">Urgent</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button onClick={handleCreate} variant="contained">Create</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Support;
