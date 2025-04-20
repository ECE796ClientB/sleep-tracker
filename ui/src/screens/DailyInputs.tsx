import { Box, Typography, Slider, Button, Stack } from "@mui/material";
import InputField from "../components/Fields/InputField";

function DailyInputs() {
  return (
    <Box sx={{ maxWidth: 600, mx: "auto", padding: 3 }}>
      <Typography variant="h3" gutterBottom>
        Daily Values
      </Typography>
        <Stack spacing={3}>
          <InputField
            id="caffeine"
            label="Caffeine Intake (cups of coffee)"
            type="number"
          />
          <InputField
            id="exercise"
            label="Exercise (hours spent today)"
            type="number"
          />

          <Typography variant="h6">Stress Level:</Typography>
          <Slider
            defaultValue={50}
            valueLabelDisplay="auto"
            step={1}
            marks
            min={0}
            max={100}
          />
        </Stack>
        <Button
          variant="contained"
          color="primary"
          type="submit"
          sx={{ marginTop: 3 }}
        >
          Submit
        </Button>
    </Box>
  );
}

export default DailyInputs;
