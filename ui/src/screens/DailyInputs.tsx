import { Box, Typography, Slider, Button, Stack } from "@mui/material";
import React, { useState } from 'react';
import InputField from "../components/Fields/InputField";

function DailyInputs() {

  const [cups, setCups] = useState('');
  const [hours, setHours] = useState('');

  const handleClick = () => {
    console.log("Button clicked!");
    

  };

  return (
    <Box sx={{ maxWidth: 600, mx: "auto", padding: 3 }}>
      <Typography variant="h3" gutterBottom>
        Daily Values
      </Typography>
        <Stack spacing={3}>
          <TextField
            id="caffeine"
            label="Caffeine Intake (cups of coffee)"
            type="number"
            variant="outlined"
            fullWidth
            className="textField"
            value={cups}
            onChange={(e) => setCups(e.target.value)}
          />
          <TextField
            id="exercise"
            label="Exercise (hours spent today)"
            type="number"
            variant="outlined"
            fullWidth
            className="textField"
            value={hours}
            onChange={(e) => setHours(e.target.value)}
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
          onClick={handleClick}
        >
          Submit
        </Button>
    </Box>
  );
}

export default DailyInputs;
