import { Typography, Stack, Box } from "@mui/material";
import CheckboxField from "../Fields/CheckboxField.tsx";

function SleepGoals() {
  return (
    <Box>
      <Typography variant="h3" gutterBottom>
        Sleep Goals
      </Typography>

      <Stack spacing={3} direction="column">
        <CheckboxField id="goal_duration" label="Improve sleep duration" />
        <CheckboxField id="goal_quality" label="Improve sleep quality" />
        <CheckboxField
          id="goal_wakeups"
          label="Reduce wakeups during the night"
        />
        <CheckboxField
          id="goal_rest"
          label="Feel more rested during the day"
        />
      </Stack>
    </Box>
  );
}

export default SleepGoals;
