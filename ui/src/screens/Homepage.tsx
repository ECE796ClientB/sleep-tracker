import { useState } from "react";
import { Typography, Box, Button, Stack, TextField } from "@mui/material";
import { Link, useNavigate } from "react-router-dom";

function Homepage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = () => {
    // Redirect to dashboard page and pass the username and password values
    console.log("Username is: " + username);
    navigate("/dashboard", { state: { username, password } });
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
        Login to Sleep Tracker
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
