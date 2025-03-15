import { Box, Grid, Paper, Typography, CircularProgress } from "@mui/material";
import { useQuery } from "@tanstack/react-query";
import api from "../utils/api";

interface ModelInfo {
  name: string;
  size: number;
  modified: string;
  // Add other properties as needed based on the API response
}

export function Dashboard() {
  const {
    data: modelInfo,
    isLoading,
    error,
  } = useQuery<ModelInfo[]>({
    queryKey: ["modelInfo"],
    queryFn: async () => {
      const response = await api.get("/ollama/tags");
      return response.data;
    },
  });

  if (isLoading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="200px"
      >
        <CircularProgress />
      </Box>
    );
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
            ) : modelInfo && modelInfo.length > 0 ? (
              modelInfo.map((model) => (
                <Paper
                  key={model.name}
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
                    Last Modified:{" "}
                    {new Date(model.modified).toLocaleDateString()}
                  </Typography>
                </Paper>
              ))
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
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}
