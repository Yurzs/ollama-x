import React, { useState, useEffect, useCallback } from "react";
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
  Collapse,
  Chip,
  Grid,
  LinearProgress,
  List,
  ListItem,
  Divider,
  Tabs,
  Tab,
  Switch,
  FormControlLabel,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";
import RefreshIcon from "@mui/icons-material/Refresh";
import AddIcon from "@mui/icons-material/Add";
import CloudDownloadIcon from "@mui/icons-material/CloudDownload";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import MemoryIcon from "@mui/icons-material/Memory";
import toast from "react-hot-toast";
import { AdminService, ServerService } from "../client";
import type { APIServer, OllamaModel } from "../client";
import { ServerStatusIcon } from "../components/ServerStatusIcon";
import { 
  PieChart, 
  Pie, 
  ResponsiveContainer, 
  Cell, 
  Legend,
  Tooltip as RechartsTooltip
} from "recharts";

// Layer progress tracking interface
interface LayerProgress {
  digest: string;
  status: string;
  total: number;
  completed: number;
  percent: number;
}

interface MemoryDataEntry {
  name: string;
  vram: number;
  ram: number;
  fullName: string;
}

const isServerActive = (lastAliveTime: string): boolean => {
  if (!lastAliveTime || lastAliveTime === "1970-01-01T00:00:00") return false;
  const lastAlive = new Date(lastAliveTime);
  const now = new Date();
  const diffInSeconds = (now.getTime() - lastAlive.getTime()) / 1000;
  return diffInSeconds < 20; // Server is considered active if last alive within 20 seconds
};

export function Servers() {
  const [servers, setServers] = useState<APIServer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [openRows, setOpenRows] = useState<Record<string, boolean>>({});
  const [loadingModels, setLoadingModels] = useState<Record<string, boolean>>(
    {}
  );
  const [activeTab, setActiveTab] = useState<Record<string, number>>({});

  // Auto-refresh state
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [lastRefreshTime, setLastRefreshTime] = useState<Date | null>(null);

  // Dialog states
  const [openCreateDialog, setOpenCreateDialog] = useState(false);
  const [openEditDialog, setOpenEditDialog] = useState(false);
  const [openDeleteDialog, setOpenDeleteDialog] = useState(false);
  const [openPullModelDialog, setOpenPullModelDialog] = useState(false);
  const [openDeleteModelDialog, setOpenDeleteModelDialog] = useState(false);

  // Form states
  const [serverUrl, setServerUrl] = useState("");
  const [modelName, setModelName] = useState("");
  const [selectedServer, setSelectedServer] = useState<APIServer | null>(null);
  const [selectedModel, setSelectedModel] = useState<OllamaModel | null>(null);
  const [isPulling, setIsPulling] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  // Download progress state
  const [downloadProgress, setDownloadProgress] = useState<{
    status: string;
    completed: number;
    total: number;
    percent: number;
  } | null>(null);
  const [layersProgress, setLayersProgress] = useState<
    Record<string, LayerProgress>
  >({});
  const [currentStatus, setCurrentStatus] = useState<string>("");

  const fetchServers = useCallback(async (showLoading = true) => {
    if (showLoading) {
      setLoading(true);
    }
    setError("");
    try {
      const response = await ServerService.getServers();
      if (Array.isArray(response)) {
        setServers(response);
        setLastRefreshTime(new Date());
      }
    } catch (err: any) {
      const errorMessage = err.message || "Failed to fetch servers";
      setError(errorMessage);
      if (showLoading) {
        toast.error(errorMessage);
      }
    } finally {
      if (showLoading) {
        setLoading(false);
      }
    }
  }, []);

  useEffect(() => {
    fetchServers();
  }, [fetchServers]);

  useEffect(() => {
    let intervalId: ReturnType<typeof setTimeout> | null = null;

    if (autoRefresh) {
      intervalId = setInterval(() => {
        fetchServers(false);
      }, 5000);
    }

    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [autoRefresh, fetchServers]);

  const fetchServerModels = async (serverId: string) => {
    if (loadingModels[serverId]) return;

    setLoadingModels((prev) => ({ ...prev, [serverId]: true }));
    try {
      const response =
        await ServerService.serverModelsServerServerIdModelListGet(serverId);
      setServers((prevServers) =>
        prevServers.map((server) =>
          server._id === serverId
            ? {
                ...server,
                models: response.models || [],
              }
            : server
        )
      );
    } catch (err: any) {
      toast.error(`Failed to fetch models: ${err.message || "Unknown error"}`);
    } finally {
      setLoadingModels((prev) => ({ ...prev, [serverId]: false }));
    }
  };

  const handleCreateServer = async () => {
    try {
      const response = await AdminService.createServerServerCreatePost(
        serverUrl
      );
      if ("_id" in response) {
        toast.success("Server created successfully");
        setOpenCreateDialog(false);
        setServerUrl("");
        fetchServers();
      }
    } catch (err: any) {
      toast.error(err.message || "Failed to create server");
    }
  };

  const handleUpdateServer = async () => {
    if (!selectedServer) return;

    try {
      await ServerService.updateServerServerUpdatePost(
        selectedServer._id,
        serverUrl
      );
      toast.success("Server updated successfully");
      setOpenEditDialog(false);
      setSelectedServer(null);
      setServerUrl("");
      fetchServers();
    } catch (err: any) {
      toast.error(err.message || "Failed to update server");
    }
  };

  const handleDeleteServer = async () => {
    if (!selectedServer) return;

    try {
      await AdminService.deleteServerServerDeleteDelete(selectedServer._id);
      toast.success("Server deleted successfully");
      setOpenDeleteDialog(false);
      setSelectedServer(null);
      fetchServers();
    } catch (err: any) {
      toast.error(err.message || "Failed to delete server");
    }
  };

  const handlePullModel = async () => {
    if (!selectedServer || !modelName) return;

    setIsPulling(true);
    setDownloadProgress(null);
    setLayersProgress({});
    setCurrentStatus("Initializing...");

    try {
      const response =
        await ServerService.serverPullModelServerServerIdModelPullPost(
          selectedServer._id,
          modelName,
          true
        );

      toast.success(`Successfully pulled model ${modelName} to server`);
      setOpenPullModelDialog(false);
      setSelectedServer(null);
      setModelName("");
      setDownloadProgress(null);
      setLayersProgress({});

      // Refetch the models for this server
      await fetchServerModels(selectedServer._id);
    } catch (err: any) {
      toast.error(err.message || `Failed to pull model ${modelName}`);
    } finally {
      setIsPulling(false);
    }
  };

  const handleDeleteModel = async () => {
    if (!selectedServer || !selectedModel) return;

    setIsDeleting(true);
    try {
      await ServerService.serverDeleteModelServerServerIdModelDeleteDelete(
        selectedServer._id,
        selectedModel.name
      );
      toast.success(`Model ${selectedModel.name} deleted successfully`);
      setOpenDeleteModelDialog(false);
      setSelectedModel(null);

      // Refetch the models for this server
      await fetchServerModels(selectedServer._id);
    } catch (err: any) {
      toast.error(
        err.message || `Failed to delete model ${selectedModel.name}`
      );
    } finally {
      setIsDeleting(false);
    }
  };

  // Helper functions
  const openEdit = (server: APIServer) => {
    setSelectedServer(server);
    setServerUrl(server.url);
    setOpenEditDialog(true);
  };

  const openDelete = (server: APIServer) => {
    setSelectedServer(server);
    setOpenDeleteDialog(true);
  };

  const openPullModel = (server: APIServer) => {
    setSelectedServer(server);
    setOpenPullModelDialog(true);
  };

  const openDeleteModel = (server: APIServer, model: OllamaModel) => {
    setSelectedServer(server);
    setSelectedModel(model);
    setOpenDeleteModelDialog(true);
  };

  const toggleRow = async (server: APIServer) => {
    const isCurrentlyOpen = openRows[server._id] || false;
    setOpenRows((prev) => ({
      ...prev,
      [server._id]: !isCurrentlyOpen,
    }));

    if (!activeTab[server._id]) {
      setActiveTab((prev) => ({
        ...prev,
        [server._id]: 0,
      }));
    }

    if (!isCurrentlyOpen && (!server.models || server.models.length === 0)) {
      await fetchServerModels(server._id);
    }
  };

  const handleTabChange = (serverId: string, newValue: number) => {
    setActiveTab((prev) => ({
      ...prev,
      [serverId]: newValue,
    }));
  };

  const formatDateTime = (dateTimeString: string) => {
    if (!dateTimeString || dateTimeString === "1970-01-01T00:00:00")
      return "Never";
    return new Date(dateTimeString).toLocaleString();
  };

  const formatBytes = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB", "TB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  const formatVRam = (vram: number | undefined) => {
    if (!vram) return "Unknown";
    return `${(vram / 1024).toFixed(2)} GB`;
  };

  const formatDownloadSize = (bytes: number | undefined) => {
    if (!bytes) return "0 MB";
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  const formatRefreshTime = (date: Date | null) => {
    if (!date) return "Never";
    return date.toLocaleTimeString(); // Shows only time part
  };

  // Prepare data for the RAM/VRAM usage pie charts
  const prepareMemoryData = (
    runningModels: OllamaModel[]
  ): MemoryDataEntry[] => {
    return runningModels.map((model) => {
      const vramSize = model.vram || 0;
      const totalSize = model.size || 0;
      const ramSize = Math.max(0, totalSize - vramSize); // Ensure RAM size is not negative

      return {
        name:
          model.name.length > 15
            ? `${model.name.substring(0, 15)}...`
            : model.name,
        vram: vramSize,
        ram: ramSize,
        fullName: model.name,
      };
    });
  };

  const COLORS = [
    "#0088FE",
    "#00C49F",
    "#FFBB28",
    "#FF8042",
    "#8884d8",
    "#82ca9d",
  ];

  const label = (props: PieLabelRenderProps) => {
    const { name, value } = props;
    return `${name} (${formatBytes(value as number)})`;
  };

  const isServerActive = (lastAliveTime: string): boolean => {
    if (!lastAliveTime || lastAliveTime === "1970-01-01T00:00:00") return false;
    const lastAlive = new Date(lastAliveTime);
    const now = new Date();
    const diffInSeconds = (now.getTime() - lastAlive.getTime()) / 1000;
    return diffInSeconds < 20; // Server is considered active if last alive within 20 seconds
  };

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: "flex", justifyContent: "space-between", mb: 3 }}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            Servers
          </Typography>
          {lastRefreshTime && (
            <Typography variant="caption" color="text.secondary">
              Last refreshed: {formatRefreshTime(lastRefreshTime)}
            </Typography>
          )}
        </Box>
        <Box sx={{ display: "flex", alignItems: "center" }}>
          <FormControlLabel
            control={
              <Switch
                checked={autoRefresh}
                onChange={(e) => setAutoRefresh(e.target.checked)}
                color="primary"
              />
            }
            label="Auto-refresh"
            sx={{ mr: 2 }}
          />
          <Button
            startIcon={<RefreshIcon />}
            onClick={() => fetchServers(true)}
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
            Add Server
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
                <TableCell width="40px"></TableCell>
                <TableCell>URL</TableCell>
                <TableCell>Last Update</TableCell>
                <TableCell>Last Alive</TableCell>
                <TableCell>Models</TableCell>
                <TableCell>Running Models</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {servers.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={7} align="center">
                    No servers found
                  </TableCell>
                </TableRow>
              ) : (
                servers.map((server) => (
                  <React.Fragment key={server._id}>
                    <TableRow>
                      <TableCell>
                        <IconButton
                          size="small"
                          onClick={() => toggleRow(server)}
                        >
                          {openRows[server._id] ? (
                            <KeyboardArrowUpIcon />
                          ) : (
                            <KeyboardArrowDownIcon />
                          )}
                        </IconButton>
                      </TableCell>
                      <TableCell>
                        <Box
                          sx={{ display: "flex", alignItems: "center", gap: 1 }}
                        >
                          <ServerStatusIcon
                            lastAliveTime={server.last_alive}
                            active={isServerActive(server.last_alive)}
                          />
                          {server.url}
                        </Box>
                      </TableCell>
                      <TableCell>
                        {formatDateTime(server.last_update)}
                      </TableCell>
                      <TableCell>{formatDateTime(server.last_alive)}</TableCell>
                      <TableCell>{server.models?.length || 0}</TableCell>
                      <TableCell>
                        {server.running_models?.length || 0}
                      </TableCell>
                      <TableCell>
                        <Tooltip title="Edit server">
                          <IconButton
                            color="primary"
                            onClick={() => openEdit(server)}
                            sx={{ mr: 0.5 }}
                          >
                            <EditIcon />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="Delete server">
                          <IconButton
                            color="error"
                            onClick={() => openDelete(server)}
                          >
                            <DeleteIcon />
                          </IconButton>
                        </Tooltip>
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell style={{ padding: 0 }} colSpan={7}>
                        <Collapse
                          in={openRows[server._id]}
                          timeout="auto"
                          unmountOnExit
                        >
                          <Box sx={{ p: 2 }}>
                            <Tabs
                              value={activeTab[server._id] || 0}
                              onChange={(_event, newValue) =>
                                handleTabChange(server._id, newValue)
                              }
                              sx={{
                                borderBottom: 1,
                                borderColor: "divider",
                                mb: 2,
                              }}
                            >
                              <Tab label="Models" />
                              <Tab
                                label="Resource Usage"
                                icon={<MemoryIcon />}
                                iconPosition="start"
                              />
                            </Tabs>

                            {/* Models Tab */}
                            {activeTab[server._id] === 0 && (
                              <Box>
                                <Box
                                  sx={{
                                    display: "flex",
                                    justifyContent: "space-between",
                                    alignItems: "center",
                                    mb: 2,
                                  }}
                                >
                                  <Typography variant="h6" component="div">
                                    Available Models
                                  </Typography>
                                  <Button
                                    variant="contained"
                                    color="primary"
                                    startIcon={<CloudDownloadIcon />}
                                    onClick={() => openPullModel(server)}
                                  >
                                    Pull New Model
                                  </Button>
                                </Box>

                                {loadingModels[server._id] ? (
                                  <Box
                                    sx={{
                                      display: "flex",
                                      justifyContent: "center",
                                      py: 4,
                                    }}
                                  >
                                    <CircularProgress size={40} />
                                  </Box>
                                ) : (
                                  <Grid container spacing={2}>
                                    {server.models &&
                                    server.models.length > 0 ? (
                                      server.models.map((model, index) => (
                                        <Grid
                                          item
                                          xs={12}
                                          sm={6}
                                          md={4}
                                          key={model.digest || index}
                                        >
                                          <Paper
                                            sx={{
                                              p: 2,
                                              height: "100%",
                                              display: "flex",
                                              flexDirection: "column",
                                            }}
                                          >
                                            <Box
                                              sx={{
                                                display: "flex",
                                                justifyContent: "space-between",
                                                alignItems: "flex-start",
                                                mb: 1,
                                              }}
                                            >
                                              <Typography
                                                variant="h6"
                                                gutterBottom
                                              >
                                                {model.name}
                                                {server.running_models?.some(
                                                  (rm) => rm.name === model.name
                                                ) && (
                                                  <Chip
                                                    label="Running"
                                                    color="success"
                                                    size="small"
                                                    sx={{ ml: 1 }}
                                                  />
                                                )}
                                              </Typography>
                                              <IconButton
                                                color="error"
                                                size="small"
                                                onClick={() =>
                                                  openDeleteModel(server, model)
                                                }
                                              >
                                                <DeleteIcon fontSize="small" />
                                              </IconButton>
                                            </Box>
                                            <Box sx={{ mb: 1 }}>
                                              <Typography
                                                variant="body2"
                                                color="text.secondary"
                                              >
                                                Family:{" "}
                                                {model.details?.family ||
                                                  "Unknown"}
                                              </Typography>
                                              <Typography
                                                variant="body2"
                                                color="text.secondary"
                                              >
                                                Format:{" "}
                                                {model.details?.format ||
                                                  "Unknown"}
                                              </Typography>
                                              <Typography
                                                variant="body2"
                                                color="text.secondary"
                                              >
                                                Parameters:{" "}
                                                {model.details
                                                  ?.parameter_size || "Unknown"}
                                              </Typography>
                                              <Typography
                                                variant="body2"
                                                color="text.secondary"
                                              >
                                                Quantization:{" "}
                                                {model.details
                                                  ?.quantization_level ||
                                                  "Unknown"}
                                              </Typography>
                                              <Typography
                                                variant="body2"
                                                color="text.secondary"
                                              >
                                                Size: {formatBytes(model.size)}
                                              </Typography>
                                              <Typography
                                                variant="body2"
                                                color="text.secondary"
                                              >
                                                Modified:{" "}
                                                {formatDateTime(
                                                  model.modified_at
                                                )}
                                              </Typography>
                                            </Box>
                                          </Paper>
                                        </Grid>
                                      ))
                                    ) : (
                                      <Grid item xs={12}>
                                        <Typography>
                                          No models available
                                        </Typography>
                                      </Grid>
                                    )}
                                  </Grid>
                                )}
                              </Box>
                            )}

                            {/* Resource Usage Tab */}
                            {activeTab[server._id] === 1 && (
                              <Box>
                                <Grid container spacing={3}>
                                  <Grid item xs={12} md={6}>
                                    <Typography
                                      variant="h6"
                                      component="div"
                                      gutterBottom
                                    >
                                      VRAM Usage by Running Models
                                    </Typography>
                                    {server.running_models &&
                                    server.running_models.length > 0 ? (
                                      <Box sx={{ height: 400 }}>
                                        <ResponsiveContainer
                                          width="100%"
                                          height="100%"
                                        >
                                          <PieChart>
                                            <Pie
                                              data={prepareMemoryData(
                                                server.running_models
                                              )}
                                              dataKey="vram"
                                              nameKey="name"
                                              cx="50%"
                                              cy="50%"
                                              outerRadius={150}
                                              label={label}
                                            >
                                              {prepareMemoryData(
                                                server.running_models
                                              ).map((_entry, index) => (
                                                <Cell
                                                  key={`cell-${index}`}
                                                  fill={
                                                    COLORS[
                                                      index % COLORS.length
                                                    ]
                                                  }
                                                />
                                              ))}
                                            </Pie>
                                            <RechartsTooltip
                                              formatter={(
                                                value:
                                                  | string
                                                  | number
                                                  | (string | number)[]
                                              ) => [
                                                formatBytes(value as number),
                                              ]}
                                              labelFormatter={(
                                                label: string | number
                                              ) => {
                                                const dataItem =
                                                  prepareMemoryData(
                                                    server.running_models
                                                  ).find(
                                                    (item) =>
                                                      item.name === label
                                                  );
                                                return (
                                                  dataItem?.fullName ||
                                                  String(label)
                                                );
                                              }}
                                            />
                                            <Legend />
                                          </PieChart>
                                        </ResponsiveContainer>
                                      </Box>
                                    ) : (
                                      <Box
                                        sx={{
                                          display: "flex",
                                          justifyContent: "center",
                                          py: 4,
                                        }}
                                      >
                                        <Typography>
                                          No running models to display
                                        </Typography>
                                      </Box>
                                    )}
                                  </Grid>

                                  <Grid item xs={12} md={6}>
                                    <Typography
                                      variant="h6"
                                      component="div"
                                      gutterBottom
                                    >
                                      RAM Usage by Running Models
                                    </Typography>
                                    {server.running_models &&
                                    server.running_models.length > 0 ? (
                                      <Box sx={{ height: 400 }}>
                                        <ResponsiveContainer
                                          width="100%"
                                          height="100%"
                                        >
                                          <PieChart>
                                            <Pie
                                              data={prepareMemoryData(
                                                server.running_models
                                              )}
                                              dataKey="ram"
                                              nameKey="name"
                                              cx="50%"
                                              cy="50%"
                                              outerRadius={150}
                                              label={label}
                                            >
                                              {prepareMemoryData(
                                                server.running_models
                                              ).map((_entry, index) => (
                                                <Cell
                                                  key={`cell-${index}`}
                                                  fill={
                                                    COLORS[
                                                      index % COLORS.length
                                                    ]
                                                  }
                                                />
                                              ))}
                                            </Pie>
                                            <RechartsTooltip
                                              formatter={(
                                                value:
                                                  | string
                                                  | number
                                                  | (string | number)[]
                                              ) => [
                                                formatBytes(value as number),
                                              ]}
                                              labelFormatter={(
                                                label: string | number
                                              ) => {
                                                const dataItem =
                                                  prepareMemoryData(
                                                    server.running_models
                                                  ).find(
                                                    (item) =>
                                                      item.name === label
                                                  );
                                                return (
                                                  dataItem?.fullName ||
                                                  String(label)
                                                );
                                              }}
                                            />
                                            <Legend />
                                          </PieChart>
                                        </ResponsiveContainer>
                                      </Box>
                                    ) : (
                                      <Box
                                        sx={{
                                          display: "flex",
                                          justifyContent: "center",
                                          py: 4,
                                        }}
                                      >
                                        <Typography>
                                          No running models to display
                                        </Typography>
                                      </Box>
                                    )}
                                  </Grid>
                                </Grid>

                                <Box sx={{ mt: 4 }}>
                                  <Typography
                                    variant="h6"
                                    component="div"
                                    gutterBottom
                                  >
                                    Running Models Details
                                  </Typography>

                                  {server.running_models &&
                                  server.running_models.length > 0 ? (
                                    <TableContainer
                                      component={Paper}
                                      sx={{ mt: 2 }}
                                    >
                                      <Table size="small">
                                        <TableHead>
                                          <TableRow>
                                            <TableCell>Model Name</TableCell>
                                            <TableCell>Parameters</TableCell>
                                            <TableCell>Quantization</TableCell>
                                            <TableCell>VRAM Usage</TableCell>
                                            <TableCell>Disk Size</TableCell>
                                          </TableRow>
                                        </TableHead>
                                        <TableBody>
                                          {server.running_models.map(
                                            (model) => (
                                              <TableRow key={model.digest}>
                                                <TableCell>
                                                  {model.name}
                                                </TableCell>
                                                <TableCell>
                                                  {model.details
                                                    ?.parameter_size ||
                                                    "Unknown"}
                                                </TableCell>
                                                <TableCell>
                                                  {model.details
                                                    ?.quantization_level ||
                                                    "Unknown"}
                                                </TableCell>
                                                <TableCell>
                                                  {formatVRam(model.vram)}
                                                </TableCell>
                                                <TableCell>
                                                  {formatBytes(model.size)}
                                                </TableCell>
                                              </TableRow>
                                            )
                                          )}
                                        </TableBody>
                                      </Table>
                                    </TableContainer>
                                  ) : (
                                    <Typography>
                                      No running models to display
                                    </Typography>
                                  )}
                                </Box>
                              </Box>
                            )}
                          </Box>
                        </Collapse>
                      </TableCell>
                    </TableRow>
                  </React.Fragment>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {/* Create Server Dialog */}
      <Dialog
        open={openCreateDialog}
        onClose={() => setOpenCreateDialog(false)}
      >
        <DialogTitle>Add New Server</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Server URL"
            type="url"
            fullWidth
            variant="outlined"
            value={serverUrl}
            onChange={(e) => setServerUrl(e.target.value)}
            placeholder="https://example.com/api"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenCreateDialog(false)}>Cancel</Button>
          <Button
            onClick={handleCreateServer}
            variant="contained"
            disabled={!serverUrl}
          >
            Add
          </Button>
        </DialogActions>
      </Dialog>

      {/* Edit Server Dialog */}
      <Dialog open={openEditDialog} onClose={() => setOpenEditDialog(false)}>
        <DialogTitle>Edit Server</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Server URL"
            type="url"
            fullWidth
            variant="outlined"
            value={serverUrl}
            onChange={(e) => setServerUrl(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenEditDialog(false)}>Cancel</Button>
          <Button
            onClick={handleUpdateServer}
            variant="contained"
            disabled={!serverUrl}
          >
            Update
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete Server Dialog */}
      <Dialog
        open={openDeleteDialog}
        onClose={() => setOpenDeleteDialog(false)}
      >
        <DialogTitle>Delete Server</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete this server?
            {selectedServer && (
              <Box
                component="span"
                sx={{ fontWeight: "bold", display: "block", mt: 1 }}
              >
                {selectedServer.url}
              </Box>
            )}
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDeleteDialog(false)}>Cancel</Button>
          <Button
            onClick={handleDeleteServer}
            color="error"
            variant="contained"
          >
            Delete
          </Button>
        </DialogActions>
      </Dialog>

      {/* Pull Model Dialog */}
      <Dialog
        open={openPullModelDialog}
        onClose={() => !isPulling && setOpenPullModelDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Pull Model to Server</DialogTitle>
        <DialogContent>
          <Typography variant="body2" sx={{ mb: 2 }}>
            Select a model to pull to server:
            {selectedServer && (
              <Box
                component="span"
                sx={{ fontWeight: "bold", display: "block", mt: 1 }}
              >
                {selectedServer.url}
              </Box>
            )}
          </Typography>
          <TextField
            autoFocus
            margin="dense"
            label="Model Name"
            fullWidth
            variant="outlined"
            value={modelName}
            onChange={(e) => setModelName(e.target.value)}
            placeholder="e.g., llama2:13b"
            disabled={isPulling}
            sx={{ mb: 3 }}
          />

          {isPulling && (
            <Box sx={{ mt: 3 }}>
              <Typography variant="body1" fontWeight="bold" gutterBottom>
                Status: {currentStatus}
              </Typography>

              {/* Overall download progress */}
              {downloadProgress && downloadProgress.total > 0 && (
                <Box sx={{ mt: 2, mb: 3 }}>
                  <Box
                    sx={{
                      display: "flex",
                      justifyContent: "space-between",
                      mb: 1,
                    }}
                  >
                    <Typography variant="body2" fontWeight="medium">
                      Overall Progress:
                    </Typography>
                    <Typography variant="body2">
                      {downloadProgress.percent}% (
                      {formatDownloadSize(downloadProgress.completed)} /{" "}
                      {formatDownloadSize(downloadProgress.total)})
                    </Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={downloadProgress.percent}
                    sx={{ height: 8, borderRadius: 1 }}
                  />
                </Box>
              )}

              {/* Layer by layer progress */}
              {Object.keys(layersProgress).length > 0 && (
                <Box sx={{ mt: 3 }}>
                  <Typography variant="body2" fontWeight="medium" gutterBottom>
                    Layer Details:
                  </Typography>
                  <List
                    sx={{
                      maxHeight: "300px",
                      overflow: "auto",
                      bgcolor: "background.paper",
                      borderRadius: 1,
                      border: "1px solid",
                      borderColor: "divider",
                    }}
                  >
                    {Object.values(layersProgress).map((layer, index) => (
                      <React.Fragment key={layer.digest}>
                        <ListItem sx={{ display: "block", py: 1 }}>
                          <Box
                            sx={{
                              display: "flex",
                              justifyContent: "space-between",
                              mb: 1,
                            }}
                          >
                            <Typography
                              variant="body2"
                              color="text.secondary"
                              sx={{
                                maxWidth: "70%",
                                overflow: "hidden",
                                textOverflow: "ellipsis",
                              }}
                            >
                              {layer.digest.substring(0, 12)}...
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              {layer.percent}%
                            </Typography>
                          </Box>
                          <LinearProgress
                            variant="determinate"
                            value={layer.percent}
                            sx={{ height: 4 }}
                          />
                          <Typography
                            variant="caption"
                            color="text.secondary"
                            sx={{ display: "block", mt: 0.5 }}
                          >
                            {formatDownloadSize(layer.completed)} /{" "}
                            {formatDownloadSize(layer.total)}
                          </Typography>
                        </ListItem>
                        {index < Object.values(layersProgress).length - 1 && (
                          <Divider />
                        )}
                      </React.Fragment>
                    ))}
                  </List>
                </Box>
              )}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button
            onClick={() => setOpenPullModelDialog(false)}
            disabled={isPulling}
          >
            Cancel
          </Button>
          <Button
            onClick={handlePullModel}
            variant="contained"
            disabled={!modelName || isPulling}
            startIcon={
              isPulling ? (
                <CircularProgress size={16} color="inherit" />
              ) : undefined
            }
          >
            {isPulling ? "Pulling..." : "Pull Model"}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete Model Dialog */}
      <Dialog
        open={openDeleteModelDialog}
        onClose={() => !isDeleting && setOpenDeleteModelDialog(false)}
      >
        <DialogTitle>Delete Model</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete this model?
            {selectedModel && (
              <Box
                component="span"
                sx={{ fontWeight: "bold", display: "block", mt: 1 }}
              >
                {selectedModel.name}
              </Box>
            )}
            {selectedServer && (
              <Box component="span" sx={{ display: "block", mt: 1 }}>
                from server: <strong>{selectedServer.url}</strong>
              </Box>
            )}
          </Typography>
          {selectedModel &&
            selectedServer?.running_models?.some(
              (rm) => rm.name === selectedModel.name
            ) && (
              <Box
                sx={{
                  mt: 2,
                  p: 1,
                  bgcolor: "error.main",
                  color: "error.contrastText",
                  borderRadius: 1,
                }}
              >
                <Typography variant="body2">
                  Warning: This model is currently running on the server.
                  Deleting it may affect active operations.
                </Typography>
              </Box>
            )}
        </DialogContent>
        <DialogActions>
          <Button
            onClick={() => setOpenDeleteModelDialog(false)}
            disabled={isDeleting}
          >
            Cancel
          </Button>
          <Button
            onClick={handleDeleteModel}
            color="error"
            variant="contained"
            disabled={isDeleting}
          >
            {isDeleting ? "Deleting..." : "Delete"}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
