import { useState } from "react";
import {
  Box,
  Paper,
  TextField,
  Button,
  Typography,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  CircularProgress,
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import { useQuery } from "@tanstack/react-query";
import toast from "react-hot-toast";
import { OllamaService } from "../client";
import type { OllamaModel } from "../client";
import type {
  ChatRequest,
  ChatResponse,
} from "../client/services/OllamaService";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [selectedModel, setSelectedModel] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);

  // Fetch available models using OllamaService
  const { data: modelsData, isLoading: modelsLoading } = useQuery({
    queryKey: ["models"],
    queryFn: async () => {
      const response = await fetch("/ollama/models");
      if (!response.ok) {
        throw new Error("Failed to fetch models");
      }
      return await response.json();
    },
  });

  // Extract models from the response
  const models = modelsData?.models || [];

  const handleSend = async () => {
    if (!input.trim() || !selectedModel) return;
    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);
    try {
      const chatRequest: ChatRequest = {
        model: selectedModel,
        messages: messages.concat(userMessage),
        stream: false,
        options: {
          temperature: 0.7,
        },
      };
      const response = await OllamaService.ollamaChat(chatRequest);
      const assistantMessage: Message = {
        role: "assistant",
        content: response.message?.content || response.response || "",
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Chat error:", error);
      toast.error("Failed to send message");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box
      sx={{
        height: "calc(100vh - 100px)",
        display: "flex",
        flexDirection: "column",
        gap: 2,
      }}
    >
      <Box sx={{ mb: 2 }}>
        <FormControl fullWidth>
          <InputLabel>Select Model</InputLabel>
          <Select
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            label="Select Model"
          >
            {modelsLoading ? (
              <MenuItem disabled>Loading models...</MenuItem>
            ) : (
              models?.map((model) => (
                <MenuItem key={model.name} value={model.name}>
                  {model.name}
                </MenuItem>
              ))
            )}
          </Select>
        </FormControl>
      </Box>
      <Paper
        sx={{
          flex: 1,
          mb: 2,
          p: 2,
          overflowY: "auto",
          bgcolor: "background.default",
        }}
      >
        {messages.map((message, index) => (
          <Box
            key={index}
            sx={{
              mb: 2,
              p: 1,
              bgcolor:
                message.role === "user" ? "primary.dark" : "background.paper",
              borderRadius: 1,
            }}
          >
            <Typography
              variant="body1"
              sx={{
                whiteSpace: "pre-wrap",
              }}
            >
              {message.content}
            </Typography>
          </Box>
        ))}
      </Paper>
      <Box sx={{ display: "flex", gap: 1 }}>
        <TextField
          fullWidth
          multiline
          maxRows={4}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          disabled={isLoading || !selectedModel}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
        />
        <Button
          variant="contained"
          onClick={handleSend}
          disabled={isLoading || !input.trim() || !selectedModel}
          sx={{ minWidth: 100 }}
        >
          {isLoading ? <CircularProgress size={24} /> : <SendIcon />}
        </Button>
      </Box>
    </Box>
  );
}
