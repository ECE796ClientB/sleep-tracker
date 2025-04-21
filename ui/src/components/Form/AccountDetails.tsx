import { Typography, Box, Stack } from "@mui/material";
import InputField from "../Fields/InputField";

function AccountDetails() {
  return (
    <Box>
      <Typography variant="h3" gutterBottom>
        Account Details
      </Typography>

      <Stack spacing={2}>
        <InputField id="username" label="Username" />
        <InputField id="password" label="Password" />
      </Stack>
    </Box>
  );
}

export default AccountDetails;
