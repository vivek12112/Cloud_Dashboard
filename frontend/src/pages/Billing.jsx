import { useState, useEffect } from 'react';
import {
  Box, Typography, Grid, Card, CardContent, Table, TableBody,
  TableCell, TableContainer, TableHead, TableRow, Paper
} from '@mui/material';
import { AttachMoney, TrendingUp, AccountBalance } from '@mui/icons-material';
import { billingAPI } from '../services/api';

const Billing = () => {
  const [summary, setSummary] = useState({
    total_cost: 0,
    monthly_cost: 0,
    active_resources_hourly_cost: 0,
    estimated_monthly: 0,
  });
  const [records, setRecords] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [summaryRes, recordsRes] = await Promise.all([
        billingAPI.getSummary(),
        billingAPI.getRecords(),
      ]);
      setSummary(summaryRes.data);
      setRecords(recordsRes.data.results || recordsRes.data);
    } catch (error) {
      console.error('Error fetching billing data:', error);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Billing & Costs
      </Typography>

      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Total Cost
                  </Typography>
                  <Typography variant="h5">
                    ${summary.total_cost.toFixed(2)}
                  </Typography>
                </Box>
                <AttachMoney color="primary" fontSize="large" />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    This Month
                  </Typography>
                  <Typography variant="h5">
                    ${summary.monthly_cost.toFixed(2)}
                  </Typography>
                </Box>
                <TrendingUp color="success" fontSize="large" />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Hourly Cost
                  </Typography>
                  <Typography variant="h5">
                    ${summary.active_resources_hourly_cost.toFixed(4)}
                  </Typography>
                </Box>
                <AccountBalance color="info" fontSize="large" />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Estimated Monthly
                  </Typography>
                  <Typography variant="h5">
                    ${summary.estimated_monthly.toFixed(2)}
                  </Typography>
                </Box>
                <TrendingUp color="warning" fontSize="large" />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Billing Records
          </Typography>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Date</TableCell>
                  <TableCell>Resource</TableCell>
                  <TableCell>Usage Hours</TableCell>
                  <TableCell>Cost/Hour</TableCell>
                  <TableCell>Total Cost</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {records.map((record) => (
                  <TableRow key={record.id}>
                    <TableCell>{new Date(record.billing_date).toLocaleDateString()}</TableCell>
                    <TableCell>{record.resource_name}</TableCell>
                    <TableCell>{record.usage_hours}</TableCell>
                    <TableCell>${record.cost_per_hour}</TableCell>
                    <TableCell>${record.total_cost}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Billing;
