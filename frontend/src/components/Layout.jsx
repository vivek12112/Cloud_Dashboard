import { useState } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import {
  AppBar, Toolbar, Typography, Drawer, List, ListItem, ListItemIcon,
  ListItemText, IconButton, Box, Menu, MenuItem
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Storage as StorageIcon,
  Assessment as AssessmentIcon,
  AttachMoney as MoneyIcon,
  Support as SupportIcon,
  People as PeopleIcon,
  Menu as MenuIcon,
  AccountCircle
} from '@mui/icons-material';
import { useAuth } from '../context/AuthContext';

const drawerWidth = 240;

const Layout = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [anchorEl, setAnchorEl] = useState(null);
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    { text: 'Dashboard', icon: <DashboardIcon />, path: '/', roles: ['user', 'admin', 'operator', 'analyst', 'engineer', 'support'] },
    { text: 'Resources', icon: <StorageIcon />, path: '/resources', roles: ['user', 'admin', 'operator'] },
    { text: 'Monitoring', icon: <AssessmentIcon />, path: '/monitoring', roles: ['user', 'admin', 'operator'] },
    { text: 'Billing', icon: <MoneyIcon />, path: '/billing', roles: ['user', 'admin', 'analyst'] },
    { text: 'Support', icon: <SupportIcon />, path: '/support', roles: ['user', 'admin', 'support'] },
    { text: 'Users', icon: <PeopleIcon />, path: '/users', roles: ['admin'] },
  ];

  const filteredMenuItems = menuItems.filter(item => 
    item.roles.includes(user?.role)
  );

  const handleDrawerToggle = () => setMobileOpen(!mobileOpen);
  const handleMenuOpen = (event) => setAnchorEl(event.currentTarget);
  const handleMenuClose = () => setAnchorEl(null);
  
  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const drawer = (
    <div style={{ backgroundColor: '#ffffff', height: '100%' }}>
      <Toolbar sx={{ backgroundColor: '#1976d2' }}>
        <Typography variant="h6" noWrap sx={{ color: '#ffffff' }}>
          Cloud Platform
        </Typography>
      </Toolbar>
      <List>
        {filteredMenuItems.map((item) => (
          <ListItem
            button
            key={item.text}
            onClick={() => navigate(item.path)}
            selected={location.pathname === item.path}
            sx={{
              '&.Mui-selected': {
                backgroundColor: '#e3f2fd',
              },
            }}
          >
            <ListItemIcon sx={{ color: '#1976d2' }}>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} sx={{ color: '#000000' }} />
          </ListItem>
        ))}
      </List>
    </div>
  );

  return (
    <Box sx={{ display: 'flex', backgroundColor: '#ffffff' }}>
      <AppBar position="fixed" sx={{ zIndex: 1201, backgroundColor: '#1976d2' }}>
        <Toolbar>
          <IconButton
            color="inherit"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1, color: '#ffffff' }}>
            Cloud Infrastructure Management
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Typography variant="body2" sx={{ color: '#ffffff' }}>{user?.username}</Typography>
            <IconButton sx={{ color: '#ffffff' }} onClick={handleMenuOpen}>
              <AccountCircle />
            </IconButton>
            <Menu
              anchorEl={anchorEl}
              open={Boolean(anchorEl)}
              onClose={handleMenuClose}
            >
              <MenuItem disabled>
                <Typography variant="caption">Role: {user?.role}</Typography>
              </MenuItem>
              <MenuItem onClick={handleLogout}>Logout</MenuItem>
            </Menu>
          </Box>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={handleDrawerToggle}
        sx={{
          display: { xs: 'block', sm: 'none' },
          '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth, backgroundColor: '#ffffff' },
        }}
      >
        {drawer}
      </Drawer>

      <Drawer
        variant="permanent"
        sx={{
          display: { xs: 'none', sm: 'block' },
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': { width: drawerWidth, boxSizing: 'border-box', backgroundColor: '#ffffff' },
        }}
      >
        {drawer}
      </Drawer>

      <Box 
        component="main" 
        sx={{ 
          flexGrow: 1, 
          p: 3, 
          mt: 8,
          backgroundColor: '#f5f5f5',
          minHeight: '100vh',
          color: '#000000'
        }}
      >
        <Outlet />
      </Box>
    </Box>
  );
};

export default Layout;