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
  Chip,
  Avatar,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormGroup,
  FormControlLabel,
  Switch,
  Snackbar,
  Alert,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";
import RefreshIcon from "@mui/icons-material/Refresh";
import AddIcon from "@mui/icons-material/Add";
import LinkIcon from "@mui/icons-material/Link";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import toast from "react-hot-toast";
import { ContinueService } from "../client";
import type { ContinueDevProject, CreateProjectRequest } from "../client";

export function Projects() {
  const [projects, setProjects] = useState<ContinueDevProject[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedProject, setSelectedProject] =
    useState<ContinueDevProject | null>(null);

  // Form states
  const [newProjectName, setNewProjectName] = useState("");
  const [openCreateDialog, setOpenCreateDialog] = useState(false);
  const [openDetailsDialog, setOpenDetailsDialog] = useState(false);
  const [copiedInviteLink, setCopiedInviteLink] = useState(false);
  const [defaultModel, setDefaultModel] = useState("llama2");

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await ContinueService.getAllProjectsContinueAllGet();
      if (Array.isArray(response)) {
        setProjects(response);
      }
    } catch (err: any) {
      const message = err.message || "Failed to fetch projects";
      setError(message);
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateProject = async () => {
    if (!newProjectName) return;

    try {
      // Basic project config
      const newProjectData: CreateProjectRequest = {
        admin: "", // Will be set by backend based on current user
        name: newProjectName,
        config: {
          models: [
            {
              provider: "ollama",
              model: defaultModel,
              title: `Ollama (${defaultModel})`,
            },
          ],
          contextProviders: [
            { name: "code" },
            { name: "codebase" },
            { name: "search" },
          ],
          customCommands: [],
          allowAnonymousTelemetry: false,
          requestOptions: {
            timeout: 60,
            verifySSL: true,
          },
        },
      };

      await ContinueService.createProjectContinueCreatePost(newProjectData);
      toast.success(`Project "${newProjectName}" created successfully`);
      setOpenCreateDialog(false);
      setNewProjectName("");
      fetchProjects();
    } catch (err: any) {
      toast.error(err.message || "Failed to create project");
    }
  };

  const handleResetInviteId = async (projectId: string) => {
    try {
      await ContinueService.resetInviteIdContinueResetInviteIdPost({
        project_id: projectId,
      });
      toast.success("Invite link reset successfully");
      fetchProjects();

      // Update selected project if it's currently being viewed
      if (selectedProject && selectedProject._id === projectId) {
        const updatedProject = await ContinueService.getProjectContinueOneGet({
          project_name: selectedProject.name,
        });
        if ("_id" in updatedProject) {
          setSelectedProject(updatedProject);
        }
      }
    } catch (err: any) {
      toast.error(err.message || "Failed to reset invite link");
    }
  };

  const openProjectDetails = async (project: ContinueDevProject) => {
    try {
      const response = await ContinueService.getProjectContinueOneGet({
        project_name: project.name,
      });
      if ("_id" in response) {
        setSelectedProject(response);
        setOpenDetailsDialog(true);
      }
    } catch (err: any) {
      toast.error(err.message || "Failed to load project details");
    }
  };

  const copyInviteLink = (projectId: string, inviteId: string) => {
    const inviteLink = `${window.location.origin}/api/continue/join/${inviteId}`;
    navigator.clipboard.writeText(inviteLink);
    setCopiedInviteLink(true);
    setTimeout(() => setCopiedInviteLink(false), 3000);
  };

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: "flex", justifyContent: "space-between", mb: 3 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          ContinueDev Projects
        </Typography>
        <Box>
          <Button
            startIcon={<RefreshIcon />}
            onClick={fetchProjects}
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
            Create Project
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
                <TableCell>Name</TableCell>
                <TableCell>Admin</TableCell>
                <TableCell>Models</TableCell>
                <TableCell>Users</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {projects.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={5} align="center">
                    No projects found
                  </TableCell>
                </TableRow>
              ) : (
                projects.map((project) => (
                  <TableRow key={project._id}>
                    <TableCell>{project.name}</TableCell>
                    <TableCell>{project.admin}</TableCell>
                    <TableCell>
                      {project.config.models &&
                        project.config.models.map((model, index) => (
                          <Chip
                            key={index}
                            label={`${model.title || model.model}`}
                            size="small"
                            sx={{ mr: 0.5, mb: 0.5 }}
                          />
                        ))}
                    </TableCell>
                    <TableCell>
                      <Avatar
                        sx={{
                          width: 30,
                          height: 30,
                          fontSize: "0.875rem",
                          bgcolor: "primary.main",
                        }}
                      >
                        {project.users.length}
                      </Avatar>
                    </TableCell>
                    <TableCell>
                      <Tooltip title="View Details">
                        <IconButton
                          color="primary"
                          onClick={() => openProjectDetails(project)}
                          sx={{ mr: 0.5 }}
                        >
                          <EditIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Copy Invite Link">
                        <IconButton
                          color="primary"
                          onClick={() =>
                            copyInviteLink(project._id, project.invite_id)
                          }
                          sx={{ mr: 0.5 }}
                        >
                          <ContentCopyIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Reset Invite Link">
                        <IconButton
                          color="primary"
                          onClick={() => handleResetInviteId(project._id)}
                        >
                          <LinkIcon />
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

      {/* Create Project Dialog */}
      <Dialog
        open={openCreateDialog}
        onClose={() => setOpenCreateDialog(false)}
      >
        <DialogTitle>Create New Project</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Project Name"
            fullWidth
            variant="outlined"
            value={newProjectName}
            onChange={(e) => setNewProjectName(e.target.value)}
            sx={{ mb: 2, mt: 1 }}
          />

          <FormControl fullWidth margin="dense">
            <InputLabel>Default Model</InputLabel>
            <Select
              value={defaultModel}
              label="Default Model"
              onChange={(e) => setDefaultModel(e.target.value)}
            >
              <MenuItem value="llama2">Llama 2</MenuItem>
              <MenuItem value="llama2:13b">Llama 2 (13B)</MenuItem>
              <MenuItem value="mistral">Mistral</MenuItem>
              <MenuItem value="codellama">CodeLlama</MenuItem>
              <MenuItem value="gemma:2b">Gemma (2B)</MenuItem>
              <MenuItem value="gemma:7b">Gemma (7B)</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenCreateDialog(false)}>Cancel</Button>
          <Button
            onClick={handleCreateProject}
            variant="contained"
            disabled={!newProjectName}
          >
            Create
          </Button>
        </DialogActions>
      </Dialog>

      {/* Project Details Dialog */}
      <Dialog
        open={openDetailsDialog}
        onClose={() => setOpenDetailsDialog(false)}
        fullWidth
        maxWidth="md"
      >
        {selectedProject && (
          <>
            <DialogTitle>Project: {selectedProject.name}</DialogTitle>
            <DialogContent>
              <Box sx={{ mb: 3 }}>
                <Typography
                  variant="subtitle1"
                  sx={{ fontWeight: "bold", mb: 1 }}
                >
                  Project Details
                </Typography>
                <Typography>
                  <strong>Admin:</strong> {selectedProject.admin}
                </Typography>
                <Typography>
                  <strong>ID:</strong> {selectedProject._id}
                </Typography>
                <Typography sx={{ display: "flex", alignItems: "center" }}>
                  <strong>Invite Link:</strong>
                  <Box
                    component="span"
                    sx={{ ml: 1, display: "flex", alignItems: "center" }}
                  >
                    <IconButton
                      size="small"
                      onClick={() =>
                        copyInviteLink(
                          selectedProject._id,
                          selectedProject.invite_id
                        )
                      }
                    >
                      <ContentCopyIcon fontSize="small" />
                    </IconButton>
                    <Button
                      size="small"
                      startIcon={<LinkIcon />}
                      onClick={() => handleResetInviteId(selectedProject._id)}
                      sx={{ ml: 1 }}
                    >
                      Reset Link
                    </Button>
                  </Box>
                </Typography>
              </Box>

              <Typography
                variant="subtitle1"
                sx={{ fontWeight: "bold", mb: 1 }}
              >
                Models
              </Typography>
              <Box sx={{ mb: 3, display: "flex", flexWrap: "wrap", gap: 1 }}>
                {selectedProject.config.models?.map((model, index) => (
                  <Chip
                    key={index}
                    label={`${model.title || model.model}`}
                    color="primary"
                    variant="outlined"
                  />
                ))}
              </Box>

              <Typography
                variant="subtitle1"
                sx={{ fontWeight: "bold", mb: 1 }}
              >
                Context Providers
              </Typography>
              <Box sx={{ mb: 3, display: "flex", flexWrap: "wrap", gap: 1 }}>
                {selectedProject.config.contextProviders?.map(
                  (provider, index) => (
                    <Chip
                      key={index}
                      label={provider.name}
                      color="secondary"
                      variant="outlined"
                    />
                  )
                )}
              </Box>

              <Typography
                variant="subtitle1"
                sx={{ fontWeight: "bold", mb: 1 }}
              >
                Settings
              </Typography>
              <FormGroup>
                <FormControlLabel
                  control={
                    <Switch
                      checked={selectedProject.config.allowAnonymousTelemetry}
                      disabled={true}
                    />
                  }
                  label="Allow Anonymous Telemetry"
                />
              </FormGroup>
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setOpenDetailsDialog(false)}>Close</Button>
            </DialogActions>
          </>
        )}
      </Dialog>

      {/* Snackbar for copied link notification */}
      <Snackbar
        open={copiedInviteLink}
        autoHideDuration={3000}
        onClose={() => setCopiedInviteLink(false)}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      >
        <Alert severity="success" sx={{ width: "100%" }}>
          Invite link copied to clipboard!
        </Alert>
      </Snackbar>
    </Box>
  );
}
