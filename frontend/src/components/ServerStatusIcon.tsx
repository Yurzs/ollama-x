import React from "react";
import { Box } from "@mui/material";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import ErrorIcon from "@mui/icons-material/Error";
import { green, red } from "@mui/material/colors";

interface ServerStatusIconProps {
  lastAliveTime: string;
  active: boolean;
}

export const ServerStatusIcon: React.FC<ServerStatusIconProps> = ({
  lastAliveTime,
  active,
}) => {
  return (
    <Box>
      {active ? (
        <CheckCircleIcon sx={{ color: green[500] }} />
      ) : (
        <ErrorIcon sx={{ color: red[500] }} />
      )}
    </Box>
  );
};
