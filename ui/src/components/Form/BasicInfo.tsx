import { Typography, Box, Stack } from "@mui/material";
import InputField from "../Fields/InputField";

function BasicInfo() {
  return (
    <Box>
      <Typography variant="h3" gutterBottom>
        Basic Information
      </Typography>

      <Stack spacing={2}>
        <InputField id="name" label="Name" />
        <InputField id="age" label="Age" type="number" />
        <InputField id="gender" label="Gender" />
        <InputField id="height" label="Height (cm)" type="number" />
        <InputField id="weight" label="Weight (kg)" type="number" />
        <InputField id="bedtime" label="Typical bedtime" type="time" />
        <InputField
          id="wakeup_time"
          label="Typical wakeup time"
          type="time"
        />
        <InputField
          id="avg_sleep"
          label="Average hours of sleep per night"
          type="number"
        />
      </Stack>
    </Box>
  );
}

export default BasicInfo;
