import { useEffect, useState } from 'react';
import { Grid, Card, CardContent, Typography, Box } from '@mui/material';
import { Storage, Assessment, AttachMoney, People, Warning } from '@mui/icons-material';
import { monitoringAPI } from '../services/api';

const Dashboard = () => {
  const [stats, setStats] = useState({
    total_resources: 0,
    active_resources: 0,
    pending_resources: 0,
    total_users: 0,
    unresolved_alerts: 0,
  });

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await monitoringAPI.getDashboardStats();
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const statCards = [
    { title: 'Total Resources', value: stats.total_resources, icon: <Storage fontSize="large" />, color: '#1976d2' },
    { title: 'Active Resources', value: stats.active_resources, icon: <Assessment fontSize="large" />, color: '#2e7d32' },
    { title: 'Pending Approvals', value: stats.pending_resources, icon: <Warning fontSize="large" />, color: '#ed6c02' },
    { title: 'Total Users', value: stats.total_users, icon: <People fontSize="large" />, color: '#9c27b0' },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        {statCards.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center">
                  <Box>
                    <Typography color="textSecondary" gutterBottom>
                      {stat.title}
                    </Typography>
                    <Typography variant="h4">
                      {stat.value}
                    </Typography>
                  </Box>
                  <Box sx={{ color: stat.color }}>
                    {stat.icon}
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Welcome to Cloud Infrastructure Management Platform
          </Typography>
          <Typography variant="body2" color="textSecondary">
            This dashboard provides an overview of your cloud resources and system status.
            Use the sidebar to navigate to different sections of the platform.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Dashboard;
