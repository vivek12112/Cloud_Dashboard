import { useState, useEffect } from 'react';
import {
  Box, Typography, Button, Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Paper, Chip, Dialog, DialogTitle, DialogContent,
  DialogActions, TextField, Select, MenuItem, FormControl, InputLabel
} from '@mui/material';
import { Add, PlayArrow, Stop, Delete } from '@mui/icons-material';
import { resourcesAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';

const Resources = () => {
  const [resources, setResources] = useState([]);
  const [open, setOpen] = useState(false);
  const { user } = useAuth();
  const [formData, setFormData] = useState({
    name: '',
    resource_type: 'vm',
    cpu_cores: 2,
    memory_gb: 4,
    storage_gb: 50,
    region: 'us-east-1',
  });

  useEffect(() => {
    fetchResources();
  }, []);

  const fetchResources = async () => {
    try {
      const response = await resourcesAPI.getAll();
      setResources(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching resources:', error);
    }
  };

  const handleCreate = async () => {
    try {
      await resourcesAPI.create(formData);
      setOpen(false);
      fetchResources();
      setFormData({
        name: '',
        resource_type: 'vm',
        cpu_cores: 2,
        memory_gb: 4,
        storage_gb: 50,
        region: 'us-east-1',
      });
    } catch (error) {
      console.error('Error creating resource:', error);
    }
  };

  const handleAction = async (id, action) => {
    try {
      if (action === 'start') await resourcesAPI.start(id);
      else if (action === 'stop') await resourcesAPI.stop(id);
      else if (action === 'approve') await resourcesAPI.approve(id);
      else if (action === 'delete') await resourcesAPI.delete(id);
      fetchResources();
    } catch (error) {
      console.error('Error performing action:', error);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      running: 'success',
      stopped: 'default',
      pending: 'warning',
      terminated: 'error',
    };
    return colors[status] || 'default';
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Resources</Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => setOpen(true)}
        >
          Create Resource
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>CPU</TableCell>
              <TableCell>Memory</TableCell>
              <TableCell>Storage</TableCell>
              <TableCell>Region</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {resources.map((resource) => (
              <TableRow key={resource.id}>
                <TableCell>{resource.name}</TableCell>
                <TableCell>{resource.resource_type}</TableCell>
                <TableCell>
                  <Chip
                    label={resource.status}
                    color={getStatusColor(resource.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>{resource.cpu_cores} cores</TableCell>
                <TableCell>{resource.memory_gb} GB</TableCell>
                <TableCell>{resource.storage_gb} GB</TableCell>
                <TableCell>{resource.region}</TableCell>
                <TableCell>
                  <Box display="flex" gap={1}>
                    {resource.status === 'stopped' && (
                      <Button size="small" onClick={() => handleAction(resource.id, 'start')}>
                        <PlayArrow />
                      </Button>
                    )}
                    {resource.status === 'running' && (
                      <Button size="small" onClick={() => handleAction(resource.id, 'stop')}>
                        <Stop />
                      </Button>
                    )}
                    {resource.status === 'pending' && user?.role === 'admin' && (
                      <Button size="small" variant="contained" onClick={() => handleAction(resource.id, 'approve')}>
                        Approve
                      </Button>
                    )}
                    <Button size="small" color="error" onClick={() => handleAction(resource.id, 'delete')}>
                      <Delete />
                    </Button>
                  </Box>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Create New Resource</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Name"
            margin="normal"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          />
          <FormControl fullWidth margin="normal">
            <InputLabel>Resource Type</InputLabel>
            <Select
              value={formData.resource_type}
              label="Resource Type"
              onChange={(e) => setFormData({ ...formData, resource_type: e.target.value })}
            >
              <MenuItem value="vm">Virtual Machine</MenuItem>
              <MenuItem value="storage">Storage</MenuItem>
              <MenuItem value="database">Database</MenuItem>
            </Select>
          </FormControl>
          <TextField
            fullWidth
            label="CPU Cores"
            type="number"
            margin="normal"
            value={formData.cpu_cores}
            onChange={(e) => setFormData({ ...formData, cpu_cores: parseInt(e.target.value) })}
          />
          <TextField
            fullWidth
            label="Memory (GB)"
            type="number"
            margin="normal"
            value={formData.memory_gb}
            onChange={(e) => setFormData({ ...formData, memory_gb: parseInt(e.target.value) })}
          />
          <TextField
            fullWidth
            label="Storage (GB)"
            type="number"
            margin="normal"
            value={formData.storage_gb}
            onChange={(e) => setFormData({ ...formData, storage_gb: parseInt(e.target.value) })}
          />
          <FormControl fullWidth margin="normal">
            <InputLabel>Region</InputLabel>
            <Select
              value={formData.region}
              label="Region"
              onChange={(e) => setFormData({ ...formData, region: e.target.value })}
            >
              <MenuItem value="us-east-1">US East (N. Virginia)</MenuItem>
              <MenuItem value="us-west-2">US West (Oregon)</MenuItem>
              <MenuItem value="eu-west-1">EU (Ireland)</MenuItem>
              <MenuItem value="ap-south-1">Asia Pacific (Mumbai)</MenuItem>
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

export default Resources;
