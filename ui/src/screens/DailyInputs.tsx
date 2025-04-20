import { Box, Typography, Slider, Button, Stack, TextField } from "@mui/material";
import React, { useState } from 'react';
// import InputField from "../components/Fields/InputField";

function DailyInputs() {

  const [patientId, setPatientId] = useState('');
  const [cups, setCups] = useState('');
  const [hours, setHours] = useState('');

  const handleClick = () => {
    

    // Send POST request to backend
    const payload =
    {
      patientId: patientId,
      cups: cups,
      hours: hours,
      stressLevel: "No stress"
    };
  
    try
    {
      const response = await fetch('https://sleep-tracker-backend.up.railway.app/logDailies', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', // Tells the backend to expect JSON
        },
        body: JSON.stringify(payload),
      });
    }
    catch (err)
    {
      console.error('Error:', err);
    }

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
            defaultValue={4}
            valueLabelDisplay="auto"
            step={1}
            marks
            min={0}
            max={4}
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
