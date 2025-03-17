import { Box, Grid, Paper, Typography } from "@mui/material";
import { useQuery } from "@tanstack/react-query";
import { ServerService } from "../client";
import { LoadingState } from "../components/LoadingState";

export function Dashboard() {
  const {
    data: servers,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["servers"],
    queryFn: () => ServerService.getServers(),
  });

  if (isLoading) {
    return <LoadingState message="Loading dashboard..." />;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Available Models
            </Typography>
            {error ? (
              <Typography color="error">
                Failed to load models. Please try again later.
              </Typography>
            ) : servers && servers.length > 0 ? (
              servers.flatMap((server) =>
                server.models.map((model) => (
                  <Paper
                    key={`${server._id}-${model.name}`}
                    sx={{
                      p: 2,
                      mb: 2,
                      "&:last-child": { mb: 0 },
                      bgcolor: "background.default",
                    }}
                  >
                    <Typography variant="subtitle1" fontWeight="bold">
                      {model.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Size: {(model.size / (1024 * 1024)).toFixed(2)} MB
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Server: {server.url}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Last Modified:{" "}
                      {new Date(model.modified_at).toLocaleDateString()}
                    </Typography>
                  </Paper>
                ))
              )
            ) : (
              <Typography color="text.secondary">
                No models available. Please install some models to get started.
              </Typography>
            )}
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              System Status
            </Typography>
            <Typography variant="body1" paragraph>
              Service: <span style={{ color: "#4caf50" }}>●</span> Active
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Version: 1.0.0
            </Typography>
            {servers && servers.length > 0 && (
              <>
                <Typography variant="body1" sx={{ mt: 2 }}>
                  Connected Servers: {servers.length}
                </Typography>
                {servers.map((server) => (
                  <Typography
                    key={server._id}
                    variant="body2"
                    color="text.secondary"
                  >
                    • {server.url} - Last alive:{" "}
                    {new Date(server.last_alive).toLocaleString()}
                  </Typography>
                ))}
              </>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}
