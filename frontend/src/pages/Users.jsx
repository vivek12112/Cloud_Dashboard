import { useState, useEffect } from 'react';
import {
  Box, Typography, Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Paper, Select, MenuItem, Button
} from '@mui/material';
import { authAPI } from '../services/api';

const Users = () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await authAPI.getUsers();
      setUsers(response.data);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const handleRoleChange = async (userId, newRole) => {
    try {
      await authAPI.updateUserRole(userId, newRole);
      fetchUsers();
    } catch (error) {
      console.error('Error updating role:', error);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        User Management
      </Typography>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Username</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Name</TableCell>
              <TableCell>Role</TableCell>
              <TableCell>Joined</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {users.map((user) => (
              <TableRow key={user.id}>
                <TableCell>{user.username}</TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell>{`${user.first_name} ${user.last_name}`}</TableCell>
                <TableCell>
                  <Select
                    value={user.role}
                    size="small"
                    onChange={(e) => handleRoleChange(user.id, e.target.value)}
                  >
                    <MenuItem value="user">Standard User</MenuItem>
                    <MenuItem value="admin">Administrator</MenuItem>
                    <MenuItem value="operator">Cloud Operator</MenuItem>
                    <MenuItem value="analyst">Finance Analyst</MenuItem>
                    <MenuItem value="engineer">Network Engineer</MenuItem>
                    <MenuItem value="support">Support Staff</MenuItem>
                  </Select>
                </TableCell>
                <TableCell>{new Date(user.created_at).toLocaleDateString()}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default Users;
