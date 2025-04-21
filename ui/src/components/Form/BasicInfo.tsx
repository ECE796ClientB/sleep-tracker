import { Typography, Box, Stack } from "@mui/material";
import InputField from "../Fields/InputField";

function BasicInfo() {
  return (
    <Box>
      <Typography variant="h3" gutterBottom>
        Basic Information
      </Typography>

      <Stack spacing={2}>
        <InputField id="firstName" label="First name" />
        <InputField id="lastName" label="Last name" />
        <InputField id="age" label="Age" type="number" />
        <InputField id="gender" label="Gender" />
        <InputField id="height" label="Height (cm)" type="number" />
        <InputField id="weight" label="Weight (kg)" type="number" />
      </Stack>
    </Box>
  );
}

export default BasicInfo;
