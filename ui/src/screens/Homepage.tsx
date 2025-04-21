import { useState } from "react";
import { Typography, Box, Button, Stack, TextField } from "@mui/material";
import { Link, useNavigate } from "react-router-dom";

function Homepage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    // Attempt to login with backend
    const params = new URLSearchParams({
      username: username,
      password: password,
    });

    try {
      // Execute GET
      const response = await fetch(
        `https://sleep-tracker-backend.up.railway.app/login?${params}`
      );

      // Process Response
      // Make sure a patient ID was returned
      const data = await response.json();
      if (data.patientId != 0) {
        // Redirect to dashboard page and pass the Patient ID
        console.log("Successfully Logged in: " + username);
        navigate("/dashboard", { state: { patientId: data.patientId } });
      } else {
        console.log("Could not login: " + username);
      }
    } catch (err) {
      console.error("Error:", err);
    }
  };

  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      height="100vh"
    >
      <Typography variant="h2" gutterBottom>
        Nova Sleep Tracker
      </Typography>

      <Stack
        spacing={3}
        direction="column"
        alignItems="center"
        width="300px"
      >
        <TextField
          label="Username"
          variant="outlined"
          fullWidth
          className="textField"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <TextField
          label="Password"
          type="password"
          variant="outlined"
          fullWidth
          className="textField"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <Button
          variant="contained"
          color="primary"
          size="large"
          fullWidth
          className="button"
          onClick={handleLogin}
        >
          Login
        </Button>
        <Button
          variant="outlined"
          color="secondary"
          component={Link}
          to="/create-profile"
          size="large"
          fullWidth
          className="button"
        >
          Create Profile
        </Button>
      </Stack>
    </Box>
  );
}

export default Homepage;
