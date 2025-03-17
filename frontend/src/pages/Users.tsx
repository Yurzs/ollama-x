import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField,
  IconButton,
  Tooltip,
  CircularProgress,
  Switch,
  FormControlLabel,
  Chip,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import RefreshIcon from "@mui/icons-material/Refresh";
import AddIcon from "@mui/icons-material/Add";
import KeyIcon from "@mui/icons-material/Key";
import toast from "react-hot-toast";
import { AdminService } from "../client";
import type { User, UserBase } from "../client";

interface APIError {
  detail: string;
  error: string;
}

export function Users() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Dialog states
  const [openCreateDialog, setOpenCreateDialog] = useState(false);
  const [openDeleteDialog, setOpenDeleteDialog] = useState(false);
  const [openResetKeyDialog, setOpenResetKeyDialog] = useState(false);

  // Form states
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isAdmin, setIsAdmin] = useState(false);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [resetApiKey, setResetApiKey] = useState<string | null>(null);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await AdminService.getAllUsers();
      if (Array.isArray(response)) {
        setUsers(response);
      } else {
        const apiError = response as APIError;
        throw new Error(
          apiError.detail || apiError.error || "Failed to fetch users"
        );
      }
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Failed to fetch users";
      setError(message);
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateUser = async () => {
    try {
      const response = await AdminService.createUser({
        username,
        password,
        is_admin: isAdmin,
      });
      if ("username" in response) {
        toast.success("User created successfully");
        setOpenCreateDialog(false);
        clearForm();
        fetchUsers();
      } else {
        const apiError = response as APIError;
        throw new Error(
          apiError.detail || apiError.error || "Failed to create user"
        );
      }
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Failed to create user";
      toast.error(message);
    }
  };

  const handleDeleteUser = async () => {
    if (!selectedUser) return;

    try {
      const response = await AdminService.deleteUser(selectedUser.username);
      if ("username" in response) {
        toast.success("User deleted successfully");
        setOpenDeleteDialog(false);
        setSelectedUser(null);
        fetchUsers();
      } else {
        const apiError = response as APIError;
        throw new Error(
          apiError.detail || apiError.error || "Failed to delete user"
        );
      }
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Failed to delete user";
      toast.error(message);
    }
  };

  const handleResetKey = async () => {
    if (!selectedUser) return;

    try {
      const response = await AdminService.changeKey(selectedUser.username);
      if ("key" in response) {
        setResetApiKey(response.key || null);
        toast.success("API key reset successfully");
        fetchUsers();
      } else {
        const apiError = response as APIError;
        throw new Error(
          apiError.detail || apiError.error || "Failed to reset API key"
        );
      }
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Failed to reset API key";
      toast.error(message);
    }
  };

  const openDelete = (user: User) => {
    setSelectedUser(user);
    setOpenDeleteDialog(true);
  };

  const openResetKey = (user: User) => {
    setSelectedUser(user);
    setOpenResetKeyDialog(true);
    setResetApiKey(null);
  };

  const clearForm = () => {
    setUsername("");
    setPassword("");
    setIsAdmin(false);
  };

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: "flex", justifyContent: "space-between", mb: 3 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Users
        </Typography>
        <Box>
          <Button
            startIcon={<RefreshIcon />}
            onClick={fetchUsers}
            sx={{ mr: 1 }}
            disabled={loading}
          >
            Refresh
          </Button>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setOpenCreateDialog(true)}
          >
            Add User
          </Button>
        </Box>
      </Box>

      {loading ? (
        <Box sx={{ display: "flex", justifyContent: "center", my: 4 }}>
          <CircularProgress />
        </Box>
      ) : error ? (
        <Typography color="error" sx={{ my: 2 }}>
          {error}
        </Typography>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Username</TableCell>
                <TableCell>Admin Status</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {users.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={4} align="center">
                    No users found
                  </TableCell>
                </TableRow>
              ) : (
                users.map((user) => (
                  <TableRow key={user._id}>
                    <TableCell>{user.username}</TableCell>
                    <TableCell>
                      {user.is_admin ? (
                        <Chip label="Admin" color="primary" size="small" />
                      ) : (
                        <Chip label="User" size="small" />
                      )}
                    </TableCell>
                    <TableCell>
                      {user.is_active ? (
                        <Chip label="Active" color="success" size="small" />
                      ) : (
                        <Chip label="Inactive" color="error" size="small" />
                      )}
                    </TableCell>
                    <TableCell>
                      <Tooltip title="Reset API key">
                        <IconButton
                          color="primary"
                          onClick={() => openResetKey(user)}
                          sx={{ mr: 0.5 }}
                        >
                          <KeyIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Delete user">
                        <IconButton
                          color="error"
                          onClick={() => openDelete(user)}
                        >
                          <DeleteIcon />
                        </IconButton>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {/* Create User Dialog */}
      <Dialog
        open={openCreateDialog}
        onClose={() => setOpenCreateDialog(false)}
      >
        <DialogTitle>Add New User</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Username"
            fullWidth
            variant="outlined"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="Password"
            type="password"
            fullWidth
            variant="outlined"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            sx={{ mb: 2 }}
          />
          <FormControlLabel
            control={
              <Switch
                checked={isAdmin}
                onChange={(e) => setIsAdmin(e.target.checked)}
              />
            }
            label="Admin privileges"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenCreateDialog(false)}>Cancel</Button>
          <Button
            onClick={handleCreateUser}
            variant="contained"
            disabled={!username || !password}
          >
            Create
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete User Dialog */}
      <Dialog
        open={openDeleteDialog}
        onClose={() => setOpenDeleteDialog(false)}
      >
        <DialogTitle>Delete User</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete this user?
            {selectedUser && (
              <Box
                component="span"
                sx={{ fontWeight: "bold", display: "block", mt: 1 }}
              >
                {selectedUser.username}
              </Box>
            )}
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDeleteDialog(false)}>Cancel</Button>
          <Button onClick={handleDeleteUser} color="error" variant="contained">
            Delete
          </Button>
        </DialogActions>
      </Dialog>

      {/* Reset API Key Dialog */}
      <Dialog
        open={openResetKeyDialog}
        onClose={() => setOpenResetKeyDialog(false)}
      >
        <DialogTitle>Reset API Key</DialogTitle>
        <DialogContent>
          {resetApiKey ? (
            <Box>
              <Typography variant="body1" sx={{ mb: 2 }}>
                New API key for user {selectedUser?.username}:
              </Typography>
              <Paper sx={{ p: 2, bgcolor: "background.default", mb: 2 }}>
                <Typography
                  sx={{ wordBreak: "break-all", fontFamily: "monospace" }}
                >
                  {resetApiKey}
                </Typography>
              </Paper>
              <Typography color="warning.main" variant="body2">
                Please copy this key now. You won't be able to see it again!
              </Typography>
            </Box>
          ) : (
            <Box>
              <Typography>
                Are you sure you want to reset the API key for user:
                {selectedUser && (
                  <Box
                    component="span"
                    sx={{ fontWeight: "bold", display: "block", mt: 1 }}
                  >
                    {selectedUser.username}
                  </Box>
                )}
              </Typography>
              <Typography color="warning.main" variant="body2" sx={{ mt: 2 }}>
                This action cannot be undone. The current API key will be
                invalidated.
              </Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenResetKeyDialog(false)}>
            {resetApiKey ? "Close" : "Cancel"}
          </Button>
          {!resetApiKey && (
            <Button
              onClick={handleResetKey}
              color="warning"
              variant="contained"
            >
              Reset Key
            </Button>
          )}
        </DialogActions>
      </Dialog>
    </Box>
  );
}
